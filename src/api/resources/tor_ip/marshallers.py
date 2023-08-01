from flask_restx import fields

from src.api.namespaces import NAMESPACES

torip_ns = NAMESPACES["Torip"]

torip_standard_serializer = torip_ns.model(
    "TorIpStandard",
    {
        "message": fields.String(),
        "status": fields.String(),
    },
)

torip_list_serializer = torip_ns.model(
    "TorIpList",
    {
        "tor_ips": fields.List(fields.String),
    },
)
