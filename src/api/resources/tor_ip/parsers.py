from flask_restx import inputs, reqparse

torip_parser = reqparse.RequestParser()

torip_parser.add_argument(
    "ip",
    type=inputs.ipv4,
    location="args",
    required=True,
    nullable=False,
)
