from flask import Blueprint
from app.utils.security import require_api_key
from app.controllers import cyber_controller as ctrl

api_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Health check endpoint
@api_bp.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok", "service": "CyberGuard REST API v1"}, 200

# Users
api_bp.add_url_rule("/users", view_func=ctrl.get_all_users, methods=["GET"])
api_bp.add_url_rule("/users", view_func=require_api_key(ctrl.create_user), methods=["POST"])

# Assets
api_bp.add_url_rule("/assets", view_func=ctrl.get_all_assets, methods=["GET"])
api_bp.add_url_rule("/assets/<int:asset_id>", view_func=ctrl.get_asset_by_id, methods=["GET"])
api_bp.add_url_rule("/assets", view_func=require_api_key(ctrl.create_asset), methods=["POST"])
api_bp.add_url_rule("/assets/<int:asset_id>", view_func=require_api_key(ctrl.update_asset), methods=["PUT"])
api_bp.add_url_rule("/assets/<int:asset_id>", view_func=require_api_key(ctrl.delete_asset), methods=["DELETE"])

# Vulnerabilities
api_bp.add_url_rule("/vulnerabilities", view_func=ctrl.get_all_vulnerabilities, methods=["GET"])
api_bp.add_url_rule("/vulnerabilities", view_func=require_api_key(ctrl.create_vulnerability), methods=["POST"])
api_bp.add_url_rule("/vulnerabilities/<int:vuln_id>", view_func=require_api_key(ctrl.update_vulnerability_status), methods=["PATCH"])

# Incidents & Incident Logs
api_bp.add_url_rule("/incidents", view_func=ctrl.get_all_incidents, methods=["GET"])
api_bp.add_url_rule("/incidents", view_func=require_api_key(ctrl.create_incident), methods=["POST"])
api_bp.add_url_rule("/incidents/<int:incident_id>", view_func=ctrl.get_incident_by_id, methods=["GET"])
api_bp.add_url_rule("/incidents/<int:incident_id>/status", view_func=require_api_key(ctrl.update_incident_status), methods=["PATCH"])
api_bp.add_url_rule("/incidents/<int:incident_id>/logs", view_func=require_api_key(ctrl.add_incident_log), methods=["POST"])