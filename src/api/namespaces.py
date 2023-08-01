from flask_restx import Namespace

NAMESPACES = {
    "Torip": Namespace(
        "tor_ip", description="endpoint for operations related to tor ips"
    ),
}
