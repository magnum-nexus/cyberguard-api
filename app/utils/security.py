from functools import wraps
from flask import request, current_app
from app.utils.error_handlers import error_response

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        expected_key = current_app.config.get("API_KEY")

        if not api_key or api_key != expected_key:
            return error_response(
                message="Akses ditolak: X-API-Key tidak valid atau tidak ditemukan",
                status_code=401
            )
        return f(*args, **kwargs)
    return decorated_function