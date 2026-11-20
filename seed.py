from app import create_app, db
from app.models.cyber_models import User, Asset, Vulnerability, Incident, IncidentLog

app = create_app()

def seed_database():
    with app.app_context():
        # Bersihkan data lama agar tidak duplikat jika dijalankan ulang
        db.session.query(IncidentLog).delete()
        db.session.query(Incident).delete()
        db.session.query(Vulnerability).delete()
        db.session.query(Asset).delete()
        db.session.query(User).delete()
        db.session.commit()

        # 1. Seed Users
        admin = User(username="admin_sec", email="admin@cyberguard.local", role="admin")
        analyst1 = User(username="raka_soc", email="raka@cyberguard.local", role="analyst")
        analyst2 = User(username="nadia_ir", email="nadia@cyberguard.local", role="analyst")
        db.session.add_all([admin, analyst1, analyst2])
        db.session.commit()

        # 2. Seed Assets
        asset1 = Asset(
            owner_id=admin.id,
            asset_name="Portal Akademik Utama",
            asset_type="Web Server",
            ip_address="192.168.10.11",
            criticality="Critical"
        )
        asset2 = Asset(
            owner_id=admin.id,
            asset_name="Database Mahasiswa",
            asset_type="Database",
            ip_address="192.168.10.25",
            criticality="Critical"
        )
        asset3 = Asset(
            owner_id=analyst1.id,
            asset_name="Mail Gateway Kampus",
            asset_type="Network",
            ip_address="192.168.10.30",
            criticality="High"
        )
        db.session.add_all([asset1, asset2, asset3])
        db.session.commit()

        # 3. Seed Vulnerabilities
        vuln1 = Vulnerability(
            asset_id=asset1.id,
            cve_code="CVE-2024-3094",
            title="Outdated OpenSSL Library on Nginx",
            severity="High",
            status="Open"
        )
        vuln2 = Vulnerability(
            asset_id=asset2.id,
            cve_code="CVE-2023-44487",
            title="HTTP/2 Rapid Reset Vulnerability",
            severity="Critical",
            status="In Progress"
        )
        db.session.add_all([vuln1, vuln2])
        db.session.commit()

        # 4. Seed Incidents
        inc1 = Incident(
            asset_id=asset1.id,
            reporter_id=analyst1.id,
            title="Serangan Brute Force Login Admin",
            incident_type="Brute Force",
            severity="High",
            status="Investigating",
            description="Terdeteksi 1.500 percobaan login gagal dari IP eksternal dalam 5 menit."
        )
        inc2 = Incident(
            asset_id=asset3.id,
            reporter_id=analyst2.id,
            title="Email Phishing Mengatasnamakan Rektorat",
            incident_type="Phishing",
            severity="Medium",
            status="Resolved",
            description="Kampanye email phishing berhasil diblokir pada mail gateway."
        )
        db.session.add_all([inc1, inc2])
        db.session.commit()

        # 5. Seed Incident Logs
        log1 = IncidentLog(
            incident_id=inc1.id,
            analyst_id=analyst1.id,
            action_taken="Memblokir IP sumber serangan pada firewall perimeter."
        )
        log2 = IncidentLog(
            incident_id=inc1.id,
            analyst_id=analyst2.id,
            action_taken="Mengaktifkan rate-limiting pada endpoint /login."
        )
        log3 = IncidentLog(
            incident_id=inc2.id,
            analyst_id=analyst2.id,
            action_taken="Menambahkan domain pengirim ke daftar blacklist SMTP."
        )
        db.session.add_all([log1, log2, log3])
        db.session.commit()

        print("Database berhasil diisi dengan data simulasi CyberGuard!")

if __name__ == "__main__":
    seed_database()