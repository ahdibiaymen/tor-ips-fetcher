import pytest

from src.api.resources.tor_ip.service import TorIpService
from src.default_config import DefaultConfig
from src.models import ExcludedTorIp


def delete_test_inserts(ips):
    if not isinstance(ips, list):
        ips = [ips]
    for ip in ips:
        query = ExcludedTorIp.delete().where(ExcludedTorIp.ip == ip)
        query.execute()


def test_app_healthiness(client):
    response = client.get("", follow_redirects=True)
    assert response.status_code == 200


@pytest.fixture
def create_test_excluded_ips():
    # set up
    ips = ("10.10.123.2", "10.10.123.3")
    for ip in ips:
        TorIpService.exclude_new_ip(ip)
    yield ips
    # tear down
    delete_test_inserts(["10.10.123.2", "10.10.123.3"])


# unallowed endpoint methods
def test_DELETE_torip_endpoint(client):
    response = client.delete(DefaultConfig.PREFIX_PATH + "/tor_ip/")
    assert response.status_code == 405


def test_PATCH_torip_endpoint(client):
    response = client.patch(DefaultConfig.PREFIX_PATH + "/tor_ip/")
    assert response.status_code == 405


def test_PUT_torip_endpoint(client):
    response = client.put(DefaultConfig.PREFIX_PATH + "/tor_ip/")
    assert response.status_code == 405


# bad requests
def test_POST_torip_endpoint_empty(client):
    response = client.post(DefaultConfig.PREFIX_PATH + "/tor_ip/excluded")
    assert response.status_code == 400


def test_POST_torip_endpoint_bad_param(client):
    data = {"ip": "zaejjfapjfsd"}
    response = client.post(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 400


def test_POST_torip_endpoint_bad_param2(client):
    data = {"ip": "10.10.1233.2"}
    response = client.post(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 400


# valid post
def test_POST_torip_endpoint_valid(client):
    data = {"ip": "10.10.123.2"}
    response = client.post(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 201
    delete_test_inserts(data.get("ip"))


# already exists
def test_POST_torip_endpoint_already_exists(client):
    data = {"ip": "10.10.123.2"}
    response = client.post(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 201
    response = client.post(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 409
    delete_test_inserts(data.get("ip"))


def test_GET_torip_endpoint_EXCLUDED(client):
    # inserting data
    data = {"ip": "10.10.123.2"}
    response = client.post(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 201
    data = {"ip": "10.10.123.3"}
    response = client.post(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 201

    # fetching data
    response = client.get(DefaultConfig.PREFIX_PATH + "/tor_ip/excluded")
    assert response.status_code == 200
    assert "tor_ips" in response.json
    assert {"10.10.123.2", "10.10.123.3"}.issubset(
        set(response.json.get("tor_ips"))
    ) is True

    # deleting test instances
    delete_test_inserts(["10.10.123.2", "10.10.123.3"])


def test_DELETE_torip_endpoint_NOT_FOUND(client, create_test_excluded_ips):
    data = {"ip": "10.10.12.3"}
    response = client.delete(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 404


def test_DELETE_torip_endpoint_EXCLUDED_SUCCESS(
    client, create_test_excluded_ips
):
    excluded_ips = create_test_excluded_ips
    # restoring one ip from exclusion
    data = {"ip": excluded_ips[0]}
    response = client.delete(
        DefaultConfig.PREFIX_PATH + "/tor_ip/excluded", query_string=data
    )
    assert response.status_code == 200

    # fetching data
    response = client.get(DefaultConfig.PREFIX_PATH + "/tor_ip/excluded")
    assert response.status_code == 200
    assert "tor_ips" in response.json
    assert excluded_ips[0] not in set(response.json.get("tor_ips"))
