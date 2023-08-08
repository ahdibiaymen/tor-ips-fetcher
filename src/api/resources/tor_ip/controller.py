from flask import request
from flask_restx import Resource, abort

from src.api import exceptions
from src.api.namespaces import NAMESPACES
from src.api.resources.tor_ip.marshallers import (
    torip_list_serializer,
    torip_standard_serializer,
)
from src.api.resources.tor_ip.parsers import torip_parser
from src.api.resources.tor_ip.service import TorIpService

torip_ns = NAMESPACES["Torip"]


@torip_ns.route("", "/")
class Torip(Resource):
    """External Tor ips endpoint"""

    @torip_ns.marshal_list_with(torip_list_serializer)
    @torip_ns.response(200, "Success")
    @torip_ns.response(400, "Bad request")
    @torip_ns.response(404, "Remote address is blocking scrappers")
    @torip_ns.response(500, "Internal Server Error")
    def get(self):
        """retrieve external tor ips (UNIQUE) list"""
        try:
            torip_list = TorIpService().retrieve_torip_list()
            return {"tor_ips": torip_list}
        except exceptions.RemoteURLContentChanged as e:
            torip_ns.logger.error(
                "The following Exception occurred while calling this URI:"
                f" '{request.url}' : {e}"
            )
            abort(404, "Remote address is blocking scrappers")
        except (exceptions.BadRemoteURL, Exception) as e:
            torip_ns.logger.error(
                "The following Exception occurred while calling this URI:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal Server Error")


@torip_ns.route("/excluded")
class ToripExcluded(Resource):
    @torip_ns.marshal_with(torip_standard_serializer)
    @torip_ns.expect(torip_parser, validate=True)
    @torip_ns.response(201, "Created")
    @torip_ns.response(400, "Bad request")
    @torip_ns.response(409, "Already exists")
    @torip_ns.response(500, "Internal Server Error")
    def post(self):
        """Add new tor ip to the existing excluded ip addresses"""
        args = torip_parser.parse_args(strict=True)
        try:
            TorIpService().exclude_new_ip(args.get("ip"))
            http_response = {
                "message": "IP_EXCLUDED",
                "status": "success",
            }
            return http_response, 201
        except exceptions.ValidationError:
            abort(400, "BAD_IP_ADDRESS")
        except exceptions.AlreadyExists:
            abort(409, "URL_ALREADY_EXCLUDED")
        except (exceptions.DBError, Exception) as e:
            torip_ns.logger.error(
                "The following Exception occurred while calling this URI:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal Server Error")

    @torip_ns.marshal_with(torip_list_serializer)
    @torip_ns.response(200, "Success")
    @torip_ns.response(400, "Bad request")
    @torip_ns.response(500, "Internal Server Error")
    def get(self):
        """retrieve all excluded ip list"""
        try:
            excluded_torip_list = TorIpService().retrieve_excluded_ip_list()
            return {"tor_ips": excluded_torip_list}
        except (exceptions.DBError, Exception) as e:
            torip_ns.logger.error(
                "The following Exception occurred while calling this URI:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal Server Error")
