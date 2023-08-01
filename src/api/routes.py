from src.api.resources.tor_ip.controller import torip_ns


def register_endpoints_routes(api):
    """ "Routes "namespaces" Registration"""

    api.add_namespace(torip_ns)
