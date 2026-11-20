from datetime import datetime, timezone
from app import db

def utc_now():
    return datetime.now(timezone.utc)

# 1. Tabel Users (Admin & Security Analyst)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="analyst")  # admin / analyst
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relasi
    assets = db.relationship("Asset", backref="owner", lazy=True)
    reported_incidents = db.relationship("Incident", backref="reporter", lazy=True)
    incident_logs = db.relationship("IncidentLog", backref="analyst", lazy=True)


# 2. Tabel Assets (Server, Aplikasi, Database, dll.)
class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # Web Server, Database, API, Network
    ip_address = db.Column(db.String(45), unique=True, nullable=False)
    criticality = db.Column(db.String(20), nullable=False, default="Medium")  # Low, Medium, High, Critical
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relasi
    vulnerabilities = db.relationship("Vulnerability", backref="asset", lazy=True, cascade="all, delete-orphan")
    incidents = db.relationship("Incident", backref="asset", lazy=True, cascade="all, delete-orphan")


# 3. Tabel Vulnerabilities (Celah keamanan pada aset)
class Vulnerability(db.Model):
    __tablename__ = "vulnerabilities"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    cve_code = db.Column(db.String(30), nullable=True)  # Contoh: CVE-2024-3094
    title = db.Column(db.String(150), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # Low, Medium, High, Critical
    status = db.Column(db.String(20), nullable=False, default="Open")  # Open, In Progress, Patched
    discovered_at = db.Column(db.DateTime, default=utc_now)


# 4. Tabel Incidents (Laporan insiden keamanan)
class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    incident_type = db.Column(db.String(50), nullable=False)  # Brute Force, DDoS, Malware, SQLi, dll.
    severity = db.Column(db.String(20), nullable=False)  # Low, Medium, High, Critical
    status = db.Column(db.String(20), nullable=False, default="Open")  # Open, Investigating, Resolved, Closed
    description = db.Column(db.Text, nullable=True)
    reported_at = db.Column(db.DateTime, default=utc_now)

    # Relasi
    logs = db.relationship("IncidentLog", backref="incident", lazy=True, cascade="all, delete-orphan")


# 5. Tabel IncidentLogs (Kronologi investigasi & tindakan mitigasi)
class IncidentLog(db.Model):
    __tablename__ = "incident_logs"

    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incidents.id"), nullable=False)
    analyst_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action_taken = db.Column(db.Text, nullable=False)
    logged_at = db.Column(db.DateTime, default=utc_now)