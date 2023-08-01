import bs4
import requests
from flask import current_app

from src.api import exceptions
from src.models import ExcludedTorIp
from src.utils import exclude_list, is_valid_ip


class TorIpService:
    @classmethod
    def exclude_new_ip(cls, ip):
        """EXCLUDE IP ADDRESS FROM RESULTS"""
        if not ip:
            raise exceptions.ValidationError(ip="NULL")
        if not is_valid_ip(ip):
            raise exceptions.ValidationError(ip=ip, reason="INVALID_IP")
        ExcludedTorIp.insert_new_ip(ip)

    @classmethod
    def retrieve_excluded_ip_list(cls):
        """GET ALL EXCLUDED IP ADDRESSES"""
        return ExcludedTorIp.get_ip_list()

    @classmethod
    def create_parser(cls, url):
        """ACCESS URL AND CREATE A PARSER ON HTML CONTENT"""
        if not url:
            raise ValueError("url argument is required")
        try:
            headers = {
                "User-Agent": current_app.config.get("USER_AGENT"),
            }
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise exceptions.BadRemoteURL(url=url, reason=e)

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        return soup

    @classmethod
    def fetch_udger_ips(cls):
        """ "grap ip addresses from UDGER WEBSITE
        (THIS WEBSITE IS SO SLOW ! IN RESPONSE FOR GET REQUESTS !)"""
        soup = cls.create_parser(current_app.config.get("UDGER_URL"))
        ip_list = []

        # Scraping
        iptab_table = soup.find("table", {"id": "iptab"})
        if not iptab_table:
            raise exceptions.RemoteURLContentChanged(
                url="UDGER", reason="IP_TABLE_NOT_FOUND"
            )
        else:
            rows = iptab_table.find_all("tr")
            for row_index in range(1, len(rows)):
                ip = rows[row_index].find_all("td")[1].string
                if is_valid_ip(ip):
                    ip_list.append(ip)
                else:
                    raise exceptions.RemoteURLContentChanged(
                        url="UDGER", reason="IP_LOCATION_CHANGED"
                    )
        return ip_list

    @classmethod
    def fetch_dan_ips(cls):
        """ "grap ip addresses from DAN.MA.UK WEBSITE"""
        soup = cls.create_parser(current_app.config.get("DAN_URL"))
        ip_list = []

        # Scraping
        begin_comment = soup.find(
            text=lambda text: isinstance(text, bs4.Comment)
            and "__BEGIN_TOR_NODE_LIST__" in text
        )
        end_comment = soup.find(
            text=lambda text: isinstance(text, bs4.Comment)
            and "__END_TOR_NODE_LIST__" in text
        )
        if not begin_comment or not end_comment:
            raise exceptions.RemoteURLContentChanged(
                url="DAN.MA", reason="CANNOT_ACCESS_IPS"
            )
        else:
            iter = begin_comment
            while not iter.next_sibling == end_comment:
                row = iter.next_sibling
                if not row.name == "br":
                    ip = row.strip().split("|")[0]
                    if is_valid_ip(ip):
                        ip_list.append(ip)
                iter = iter.next_sibling

            return ip_list

    @classmethod
    def retrieve_torip_list(cls):
        """RETURN TOR IPs with exclusion
        of tor ip saved in database"""
        udger_ips_list = cls.fetch_udger_ips()
        dan_ips_list = cls.fetch_dan_ips()
        tor_ip_list = udger_ips_list + dan_ips_list
        excluded_ips = cls.retrieve_excluded_ip_list()
        return exclude_list(tor_ip_list, excluded_ips)
