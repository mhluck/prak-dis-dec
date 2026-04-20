# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 5

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---
## Fault Tolerance
---

### A. Load Balancing Aplikasi

Pembahasan tentang load balancing diperlukan agar high-availability dari suatu aplikasi bisa tercapai. Hal ini dilakukan dengan melakukan proses scaling aplikasi menjadi lebih dari satu instance dan mengkonfigurasi proxy load balancer. Pada praktikum di Windows ini, saya menggunakan Docker Desktop dan PowerShell.

#### 1. Persiapan Environment dan Instalasi

Aplikasi web dibangun menggunakan ASGI framework Python bernama Blacksheep.
- Buka PowerShell, buat direktori baru(workspace-05), dan siapkan virtual environment menggunakan uv (atau python -m venv):

```bash
uv venv
.venv\Scripts\activate
```
![venv](images/Screenshot%202026-04-20%20222013.png)

Setelah aktif, install paket yang dibutuhkan:

```bash
uv pip install blacksheep blacksheep-cli
```
![install blacksheep](images/Screenshot%202026-04-20%20222137.png)
![install blacksheep](images/Screenshot%202026-04-20%20222205.png)

#### 2. Pembuatan Aplikasi Web

Gunakan CLI dari Blacksheep untuk membuat scaffolding project.

```bash
blacksheep create
```
![create](images/Screenshot%202026-04-20%20222359.png)

Isi konfigurasi sesuai panduan modul :
- Project name: blacksheep_lb
- Project template: mvc
- Use OpenAPI Documentation? Yes
- Library to read settings: essentials-configuration
- App settings format: TOML

Masuk ke direktori aplikasi dan jalankan untuk menguji

```bash
cd blacksheep_lb
uv pip install -r requirements.txt
python dev.py
```
![menguji](images/Screenshot%202026-04-20%20222945.png)
![run](images/Screenshot%202026-04-20%20225305.png)
![apk](images/Screenshot%202026-04-20%20225314.png)

Aplikasi akan berjalan secara lokal di port 44777 (http://localhost:44777/) . Tekan CTRL+C untuk mematikan server.

#### 3. Konfigurasi Nginx dan Docker Compose

Untuk membuat sistem terdistribusi, saya menyiapkan load balancer menggunakan Nginx dan menggabungkannya di docker-compose.yml

**a. Konfigurasi Nginx**
Kembali ke folder workspace-05, buat folder nginx yang berisi dua file: Dockerfile dan nginx.conf .

- nginx/Dockerfile:
```bash
FROM nginx
#Override the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
```

- nginx/nginx.conf:
```bash
events {
    worker_connections 4096;
}
http {
    # Definisi grup backend
    upstream backend {
        server bs_app:80;
    }
    server {
        listen 80;
        location / {
            proxy_pass http://backend;
        }
    }
}
```

**b. Konfigurasi Docker Compose**
- Buat file docker-compose.yml di folder root (workspace-05) :

```bash
services:
  # aplikasi yang akan di-scale
  bs_app:
    build: ./blacksheep_lb

  # aktifkan nginx dengan menggunakan nginx/Dockerfile
  nginx:
    container_name: nginx
    build: ./nginx
    ports:
      - 80:80
    depends_on:
      - bs_app
```

#### 4. Menjalankan Docker Compose dan Menguji Load Balancer
Saya akan menjalankan aplikasi dan langsung melakukan scale-up menjadi 2 instance.

- Di PowerShell, jalankan:

```bash
docker-compose up --build -d --scale bs_app=2
```
![docker](images/Screenshot%202026-04-20%20231550.png)

- Cek apakah sistem berjalan dengan perintah:

```bash
docker ps
```
![cek](images/Screenshot%202026-04-20%20231706.png)

Disini terlihat tiga kontainer berjalan: 1 Nginx, dan 2 instance bs_app .

**Pengujian Load Balancer:**

1. Buka browser dan akses http://localhost. Halaman Blacksheep akan muncul (di port 80).
2. Lakukan refresh (F5) beberapa kali.
3. Cek log distribusi beban pada masing-masing instance di PowerShell:

```bash
docker logs workspace-05-bs_app-1
docker logs workspace-05-bs_app-2
```
![docker logs](images/Screenshot%202026-04-20%20232000.png)

Penjelasan: Pada log, Disini terlihat request HTTP dibagikan secara bergantian ke bs_app-1 dan bs_app-2. Nginx bertugas me-route permintaan ke instance yang tersedia secara Round-Robin .

Matikan server jika sudah selesai:
```bash
docker-compose down
```
![down](images/Screenshot%202026-04-20%20232113.png)