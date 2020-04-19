"""Application error handlers."""
from flask import Blueprint, jsonify
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException

api = Blueprint("errors", __name__, url_prefix="/api/errors")


@api.app_errorhandler(HTTPException)
def handle_http_errors(error):
    status_code = error.code
    response = {
        "error": HTTP_STATUS_CODES[status_code],
        "message": error.description,
    }
    response = jsonify(response)
    response.status_code = status_code
    return response


@api.app_errorhandler(Exception)
def handle_generic_errors(error):
    status_code = 400
    response = {
        "error": type(error).__name__,
        "message": getattr(error, "message", str(error)),
    }
    response = jsonify(response)
    response.status_code = status_code
    return response
