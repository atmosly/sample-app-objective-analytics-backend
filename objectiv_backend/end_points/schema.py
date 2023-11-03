"""
Copyright 2021 Objectiv B.V.
"""
import requests

from flask import Response

from objectiv_backend.common.config import get_collector_config
from objectiv_backend.end_points.common import get_json_response


def schema() -> Response:
    """ Endpoint that returns the event schema in our own notation. """
    config = get_collector_config()
    url = f'{config.schema_config.validation_service_url}/schema/latest'
    response = requests.get(url)

    if response.status_code == 200:
        msg = response.text
    else:
        msg = 'schema not available'

    return get_json_response(status=response.status_code, msg=msg)


def json_schema() -> Response:
    """ Endpoint that returns a jsonschema that describes the event schema. """
    msg = 'not implemented'
    return get_json_response(status=200, msg=msg)
