# VEGA LMS - Backend API

VEGA (Virtual Education & Growth Academy) adalah platform *Learning Management System* (LMS) internal untuk KSM IoT & AI. Repository ini memuat seluruh layanan *backend* (API) yang menyuplai data ke aplikasi *frontend* VEGA. 

Backend VEGA dibangun menggunakan ekosistem Python modern yang berfokus pada kecepatan dan keamanan.

## 🚀 Teknologi Utama

- **[FastAPI](https://fastapi.tiangolo.com/)**: Web framework modern & cepat (high-performance) untuk membangun API dengan Python.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Object Relational Mapper (ORM) untuk menghubungkan aplikasi ke Database.
- **[Alembic](https://alembic.sqlalchemy.org/)**: Tool migrasi database yang digunakan bersama SQLAlchemy.
- **SQLite**: Database default yang sedang digunakan (bisa dipindah ke PostgreSQL untuk *production*).
- **[Uvicorn](https://www.uvicorn.org/)**: ASGI web server untuk menjalankan FastAPI.

## 🛠 Instalasi dan Menjalankan Server

Kamu dapat menjalankan aplikasi backend ini menggunakan dua cara: menggunakan **Docker** (Direkomendasikan) atau menggunakan **Python Environment Local**.

### Cara 1: Menjalankan dengan Docker (Rekomendasi)

Jika kamu ingin menjalankan tanpa pusing memikirkan *dependencies* di komputer lokal, cukup pastikan Docker sudah ter-install.

1. **Build Docker Image**
   ```bash
   docker build -t vega-backend .
   ```
2. **Jalankan Container**
   ```bash
   docker run -p 8000:8000 -v "$PWD/vega.db:/app/vega.db" --env-file .env vega-backend
   ```
   > API dapat diakses di http://localhost:8000. Untuk dokumentasi Swagger API secara interaktif, buka http://localhost:8000/docs.

### Cara 2: Menjalankan dengan Python / Pip secara Lokal

Jika kamu ingin melakukan proses *development* dan ingin menjalankan secara manual:

1. **Buat Virtual Environment (Opsional namun direkomendasikan)**
   ```bash
   python -m venv .venv
   ```
2. **Aktifkan Virtual Environment**
   - **Windows:** `.venv\Scripts\activate`
   - **Mac/Linux:** `source .venv/bin/activate`
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Jalankan Uvicorn Server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   *Note: Flag `--reload` membuat server otomatis restart ketika kamu menyimpan perubahan kode (hanya gunakan di development).*

## 🗄 Migrasi Database (Alembic)

Ketika ada perubahan pada model data di dalam folder `app/models/`, kamu perlu membuat revisi migrasi baru agar struktur database kamu ikut ter-update. 

- **Membuat revisi baru**:
  ```bash
  alembic revision --autogenerate -m "Penjelasan perubahan tabel"
  ```
- **Menjalankan/mengaplikasikan migrasi ke DB**:
  ```bash
  alembic upgrade head
  ```

## 🔐 Environment Variables

Untuk mengatur environment variables, silakan buat file `.env` di folder root `vega-backend` ini jika belum ada. 

## 📖 Dokumentasi Interaktif API (Swagger UI)

FastAPI secara otomatis me-generate dokumentasi OpenAPI interaktif. Sangat mempermudah integrasi ke Frontend.

Saat server menyala, kunjungi:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

Selamat mengembangkan backend VEGA! ✨
