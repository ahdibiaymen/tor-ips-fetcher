import os

import peewee
from dotenv import load_dotenv

from src.api import exceptions
from src.default_config import DefaultConfig
from playhouse.db_url import connect

# load .env configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "../.env"))

# database connection
if DefaultConfig.MODE == "prod":
    pg_db = connect(os.environ.get("DATABASE_URL"))
else:  # dev
    pg_db = peewee.PostgresqlDatabase(
        database=os.environ.get("POSTGRESQL_DB_NAME"),
        user=os.environ.get("POSTGRESQL_DB_USER"),
        password=os.environ.get("POSTGRESQL_DB_PASSWD"),
        host=os.environ.get("POSTGRESQL_DB_HOST"),
        port=os.environ.get("POSTGRESQL_DB_PORT"),
        autorollback=True,
    )
    pg_db.connect(reuse_if_open=True)


class BaseModel(peewee.Model):
    pass


class ExcludedTorIp(BaseModel):
    id = peewee.AutoField()
    ip = peewee.TextField(unique=True, null=False)

    class Meta:
        database = pg_db

    @classmethod
    def insert_new_ip(cls, new_ip):
        """exclude new ip address"""
        try:
            exists = (
                ExcludedTorIp.select()
                .where(ExcludedTorIp.ip == new_ip)
                .first()
            )
            if exists:
                raise exceptions.AlreadyExists(ip=new_ip)

            new_ip = ExcludedTorIp(ip=new_ip)
            new_ip.save()
        except peewee.PeeweeException as e:
            raise exceptions.DBError(table="tor_ip", new_ip=new_ip, reason=e)

    @classmethod
    def get_ip_list(cls):
        """retrieve all excluded ip addresses as a list"""
        query = ExcludedTorIp.select()
        ip_list = [excluded.ip for excluded in query]
        return ip_list

    @classmethod
    def get_one_ip(cls, ip):
        retrieved_ip = (
            ExcludedTorIp.select().where(ExcludedTorIp.ip == ip).first()
        )
        if not retrieved_ip:
            return False
        return retrieved_ip

    @classmethod
    def delete_one_ip(cls, ip):
        try:
            ExcludedTorIp.delete().where(ExcludedTorIp.ip == ip).execute()
        except Exception as e:
            raise exceptions.DBError(table="tor_ip", ip=ip, reason=e)


pg_db.create_tables([ExcludedTorIp])
