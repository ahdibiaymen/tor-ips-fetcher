import ipaddress


def is_valid_ip(ip):
    """Check if a provided ip is valid"""
    if not ip:
        return False
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def exclude_list(list_main, list_to_exclude):
    """apply set difference between two lists"""
    if not isinstance(list_main, list) and not isinstance(
        list_to_exclude, list
    ):
        raise ValueError("exclude_list parameters need to be lists")
    return list(set(list_main) - set(list_to_exclude))
