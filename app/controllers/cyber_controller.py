from flask import request
from app import db
from app.models.cyber_models import User, Asset, Vulnerability, Incident, IncidentLog
from app.schemas.cyber_schemas import (
    UserSchema, AssetSchema, VulnerabilitySchema, IncidentSchema, IncidentLogSchema
)
from app.utils.error_handlers import success_response, error_response

user_schema = UserSchema()
users_schema = UserSchema(many=True)

asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)

vuln_schema = VulnerabilitySchema()
vulns_schema = VulnerabilitySchema(many=True)

incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)

log_schema = IncidentLogSchema()
logs_schema = IncidentLogSchema(many=True)


# ================= USERS =================
def get_all_users():
    users = User.query.all()
    return success_response(users_schema.dump(users), "Daftar pengguna berhasil diambil")

def create_user():
    payload = request.get_json(silent=True) or {}
    data = user_schema.load(payload)

    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return success_response(user_schema.dump(new_user), "Pengguna berhasil dibuat", 201)


# ================= ASSETS (Dengan Filter & Pagination) =================
def get_all_assets():
    query = Asset.query

    # Filter berdasarkan criticality & asset_type
    criticality = request.args.get("criticality")
    asset_type = request.args.get("asset_type")
    if criticality:
        query = query.filter(Asset.criticality.ilike(criticality))
    if asset_type:
        query = query.filter(Asset.asset_type.ilike(f"%{asset_type}%"))

    # Pagination
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    meta = {
        "page": paginated.page,
        "limit": paginated.per_page,
        "total_items": paginated.total,
        "total_pages": paginated.pages
    }
    return success_response(assets_schema.dump(paginated.items), "Daftar aset berhasil diambil", 200, meta)

def get_asset_by_id(asset_id):
    asset = db.session.get(Asset, asset_id)
    if not asset:
        return error_response("Aset tidak ditemukan", 404)

    result = asset_schema.dump(asset)
    result["vulnerabilities"] = vulns_schema.dump(asset.vulnerabilities)
    return success_response(result, "Detail aset berhasil diambil")

def create_asset():
    payload = request.get_json(silent=True) or {}
    data = asset_schema.load(payload)

    if not db.session.get(User, data["owner_id"]):
        return error_response("Owner (user_id) tidak ditemukan", 404)

    new_asset = Asset(**data)
    db.session.add(new_asset)
    db.session.commit()
    return success_response(asset_schema.dump(new_asset), "Aset berhasil ditambahkan", 201)

def update_asset(asset_id):
    asset = db.session.get(Asset, asset_id)
    if not asset:
        return error_response("Aset tidak ditemukan", 404)

    payload = request.get_json(silent=True) or {}
    data = asset_schema.load(payload, partial=True)

    for key, value in data.items():
        setattr(asset, key, value)

    db.session.commit()
    return success_response(asset_schema.dump(asset), "Aset berhasil diperbarui")

def delete_asset(asset_id):
    asset = db.session.get(Asset, asset_id)
    if not asset:
        return error_response("Aset tidak ditemukan", 404)

    db.session.delete(asset)
    db.session.commit()
    return success_response(None, "Aset berhasil dihapus")


# ================= VULNERABILITIES =================
def get_all_vulnerabilities():
    query = Vulnerability.query
    status = request.args.get("status")
    severity = request.args.get("severity")

    if status:
        query = query.filter(Vulnerability.status.ilike(status))
    if severity:
        query = query.filter(Vulnerability.severity.ilike(severity))

    vulns = query.all()
    return success_response(vulns_schema.dump(vulns), "Daftar kerentanan berhasil diambil")

def create_vulnerability():
    payload = request.get_json(silent=True) or {}
    data = vuln_schema.load(payload)

    if not db.session.get(Asset, data["asset_id"]):
        return error_response("Aset tidak ditemukan", 404)

    new_vuln = Vulnerability(**data)
    db.session.add(new_vuln)
    db.session.commit()
    return success_response(vuln_schema.dump(new_vuln), "Kerentanan berhasil dicatat", 201)

def update_vulnerability_status(vuln_id):
    vuln = db.session.get(Vulnerability, vuln_id)
    if not vuln:
        return error_response("Data kerentanan tidak ditemukan", 404)

    payload = request.get_json(silent=True) or {}
    data = vuln_schema.load(payload, partial=True)

    if "status" in data:
        vuln.status = data["status"]
    if "severity" in data:
        vuln.severity = data["severity"]

    db.session.commit()
    return success_response(vuln_schema.dump(vuln), "Status kerentanan berhasil diperbarui")


# ================= INCIDENTS & LOGS (Dengan Search, Filter & Sorting) =================
def get_all_incidents():
    query = Incident.query

    # Search berdasarkan judul atau tipe insiden
    search = request.args.get("search")
    status = request.args.get("status")
    severity = request.args.get("severity")
    sort = request.args.get("sort", "desc")

    if search:
        query = query.filter(
            (Incident.title.ilike(f"%{search}%")) |
            (Incident.incident_type.ilike(f"%{search}%"))
        )
    if status:
        query = query.filter(Incident.status.ilike(status))
    if severity:
        query = query.filter(Incident.severity.ilike(severity))

    # Sorting berdasarkan waktu pelaporan
    if sort.lower() == "asc":
        query = query.order_by(Incident.reported_at.asc())
    else:
        query = query.order_by(Incident.reported_at.desc())

    incidents = query.all()
    return success_response(incidents_schema.dump(incidents), "Daftar insiden berhasil diambil")

def create_incident():
    payload = request.get_json(silent=True) or {}
    data = incident_schema.load(payload)

    if not db.session.get(Asset, data["asset_id"]):
        return error_response("Aset target tidak ditemukan", 404)
    if not db.session.get(User, data["reporter_id"]):
        return error_response("Pelapor (user_id) tidak ditemukan", 404)

    new_incident = Incident(**data)
    db.session.add(new_incident)
    db.session.commit()
    return success_response(incident_schema.dump(new_incident), "Laporan insiden berhasil dibuat", 201)

def get_incident_by_id(incident_id):
    incident = db.session.get(Incident, incident_id)
    if not incident:
        return error_response("Laporan insiden tidak ditemukan", 404)

    return success_response(incident_schema.dump(incident), "Detail insiden beserta log berhasil diambil")

def update_incident_status(incident_id):
    incident = db.session.get(Incident, incident_id)
    if not incident:
        return error_response("Laporan insiden tidak ditemukan", 404)

    payload = request.get_json(silent=True) or {}
    data = incident_schema.load(payload, partial=True)

    if "status" not in data:
        return error_response("Field 'status' wajib diisi", 400)

    incident.status = data["status"]
    db.session.commit()
    return success_response(incident_schema.dump(incident), "Status insiden berhasil diperbarui")

def add_incident_log(incident_id):
    incident = db.session.get(Incident, incident_id)
    if not incident:
        return error_response("Laporan insiden tidak ditemukan", 404)

    payload = request.get_json(silent=True) or {}
    data = log_schema.load(payload)

    if not db.session.get(User, data["analyst_id"]):
        return error_response("Analis (user_id) tidak ditemukan", 404)

    new_log = IncidentLog(incident_id=incident_id, **data)
    db.session.add(new_log)
    db.session.commit()
    return success_response(log_schema.dump(new_log), "Log investigasi berhasil ditambahkan", 201)