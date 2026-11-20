from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

def success_response(data=None, message="Success", status_code=200, meta=None):
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    if meta:
        response["meta"] = meta
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    response = {
        "status": "error",
        "message": message
    }
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return error_response(
            message="Validasi input gagal",
            status_code=400,
            errors=err.messages
        )

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        return error_response(
            message="Terjadi konflik integritas data (duplikat atau relasi tidak valid)",
            status_code=409
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return error_response(
            message=err.description,
            status_code=err.code
        )

    @app.errorhandler(Exception)
    def handle_generic_error(err):
        return error_response(
            message="Terjadi kesalahan internal pada server",
            status_code=500
        )