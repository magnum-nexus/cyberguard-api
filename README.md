# CyberGuard REST API (UTS Pemrograman Web Lanjut)

MVP REST API berbasis **Python Flask**, **SQLAlchemy ORM**, dan arsitektur **MVC** untuk manajemen inventaris aset IT, pencatatan kerentanan (_vulnerability tracking_), serta pelaporan dan investigasi insiden keamanan siber (_cyber incident reporting_).

## Fitur Utama

- **Manajemen Pengguna (`users`)**: Pendaftaran dan daftar Security Analyst / Admin.
- **Manajemen Aset (`assets`)**: CRUD aset digital beserta filter `criticality`, `asset_type`, dan _pagination_.
- **Pelacakan Kerentanan (`vulnerabilities`)**: Pencatatan celah keamanan (CVE) per aset dan pembaruan status mitigasi (`Open`, `In Progress`, `Patched`).
- **Pelaporan Insiden & Log Investigasi (`incidents`, `incident_logs`)**: Pencatatan insiden siber lengkap dengan pencarian (`search`), filter `status`/`severity`, _sorting_, dan kronologi tindakan mitigasi.
- **Validasi & Keamanan Dasar**: Validasi skema menggunakan Marshmallow, format respons JSON terstandar, dan proteksi endpoint tulis menggunakan header `X-API-Key`.

## Instalasi & Konfigurasi Lokal

1. **Clone repository dan masuk ke folder proyek:**
   ```bash
   git clone <https://github.com/magnum-nexus/cyberguard-api>
   cd cyberguard-api
   ```
