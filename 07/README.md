# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 7

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---
## Cloud Computing
---

Cloud Computing menggunakan pendekatan XaaS atau sering juga disebut sebagai Everything as a Service. Dengan menggunakan pendekatan ini, provider dari Cloud Computing menyediakan berbagai sumber daya komputasi dan konsumen mendapatkan sumber daya tersebut dalam bentuk layanan. Meskipun saat ini ada banyak XaaS tetapi secara umum biasanya dibagi menjadi 3:
1. SaaS: Software as a Service
2. PaaS: Platform as a Service
3. IaaS: Infrastructure as a Service

---

### Tugas:

#### 1. Contoh Vendor/Komunitas XaaS:
- SaaS (Software as a Service): Google Workspace (Google Docs, Gmail, Drive) atau Microsoft 365.
- PaaS (Platform as a Service): Heroku atau Google App Engine.
- IaaS (Infrastructure as a Service): Amazon Web Services (AWS - Amazon EC2) atau Google Compute Engine (GCE).

#### 2. Uraian Layanan (Service) dari Kategori XaaS:
- SaaS: Vendor menyediakan perangkat lunak (aplikasi) yang sudah jadi dan sepenuhnya dikelola oleh penyedia layanan. Pengguna akhir (end-user) hanya perlu menggunakan aplikasi tersebut melalui web browser tanpa harus memikirkan instalasi, maintenance, atau infrastruktur di belakangnya.
- PaaS: Vendor menyediakan platform dan lingkungan komputasi (sistem operasi, runtime bahasa pemrograman, basis data, web server) yang memungkinkan developer untuk mengembangkan, menjalankan, dan mengelola aplikasi tanpa kerumitan membangun dan memelihara infrastruktur di bawahnya.
- IaaS: Vendor menyewakan sumber daya komputasi mentah secara virtualisasi, seperti server (Virtual Machine), jaringan (networking), dan kapasitas penyimpanan (storage). Pengguna memiliki kontrol penuh terhadap infrastruktur virtual tersebut, termasuk instalasi sistem operasi dan perangkat lunak di dalamnya.

#### 3. Visualisasi Arsitektur XaaS:
Arsitektur XaaS dapat digambarkan sebagai lapisan (stack) di mana kontrol pengguna semakin berkurang dari bawah ke atas:

![venv](images/Screenshot%202026-05-12%20183400.png)
- IaaS (Paling Bawah): Vendor mengelola Networking, Storage, Servers, Virtualization. Pengguna mengelola O/S, Middleware, Runtime, Data, Applications.
- PaaS (Tengah): Vendor mengelola semuanya dari Networking hingga Runtime. Pengguna hanya mengelola Data dan Applications.
- SaaS (Paling Atas): Vendor mengelola semuanya (dari Networking hingga Applications). Pengguna hanya memakai aplikasinya saja.

---

### Containerized App menggunakan Flask

Praktikum ini bertujuan untuk membangun sebuah aplikasi blog sederhana dari tutorial Flask dan mengubahnya menjadi Containerized App (CA) menggunakan Docker. Praktikum ini dieksekusi di OS Windows menggunakan PowerShell.

#### Langkah 1: Persiapan dan Clone Repositori
Buka PowerShell, tentukan lokasi workspace, lalu clone repositori resmi Flask.

```bash
# Melakukan clone repositori tutorial Flask
git clone https://github.com/pallets/flask

# Masuk ke direktori tutorial
cd flask/examples/tutorial
```
![venv](images/Screenshot%202026-05-12%20184602.png)

#### Langkah 2: Menyiapkan Virtual Environment
Buat virtual environment Python dan aktifkan (penyesuaian perintah untuk Windows).

```bash
# Membuat virtual environment bernama .venv
python -m venv .venv

# Mengaktifkan virtual environment di Windows (PowerShell)
.venv\Scripts\activate

# Menginstal dependensi aplikasi tutorial
pip install -e .
```
![venv](images/Screenshot%202026-05-12%20184847.png)
![venv](images/Screenshot%202026-05-12%20184907.png)

#### Langkah 3: Inisialisasi Database dan Uji Coba Lokal
Sebelum di-container, pastikan aplikasi berjalan normal di OS lokal Windows.

```bash
# Inisialisasi basis data SQLite
flask --app flaskr init-db

# Menjalankan aplikasi dalam mode debug
flask --app flaskr run --debug
```
Buka browser dan akses http://127.0.0.1:5000. Jika aplikasi blog berjalan, tekan CTRL+C di PowerShell untuk mematikan server lokal tersebut.

![venv](images/Screenshot%202026-05-12%20185059.png)
![venv](images/Screenshot%202026-05-12%20185130.png)

#### Langkah 4: Membuat Dockerfile
Untuk membuat Containerized App, buat sebuah file baru bernama Dockerfile (tanpa ekstensi .txt) di dalam direktori flask/examples/tutorial.
Gunakan text editor (misalnya VS Code atau Notepad) dan isi file Dockerfile dengan konfigurasi berikut (menggunakan base image Python 3.14 seperti pada modul):

```bash
# Menggunakan base image Python 3.14
FROM python:3.14-rc-slim

# Menentukan direktori kerja di dalam container
WORKDIR /app

# Menyalin seluruh kode tutorial ke dalam container
COPY . /app

# Menginstal dependensi aplikasi
RUN pip install -e .

# Inisialisasi database
RUN flask --app flaskr init-db

# Mengekspos port 5000
EXPOSE 5000

# Perintah utama untuk menjalankan aplikasi saat container di-start
CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0"]
```

![venv](images/Screenshot%202026-05-12%20185500.png)

#### Langkah 5: Membangun (Build) Docker Image
Pastikan Docker Desktop sudah berjalan di Windows. Jalankan perintah docker build pada PowerShell (pastikan masih berada di dalam direktori tutorial yang berisi Dockerfile tadi).

```bash
docker build -t localhost/flaskr:1.0.0 .
```

Tunggu hingga proses download base image dan build selesai. Setelah itu, verifikasi image yang telah dibuat:

```bash
docker image ls
```
![venv](images/Screenshot%202026-05-12%20185741.png)

#### Langkah 6: Menjalankan Containerized App
Jalankan container dari image yang baru saja dibuat dengan memetakan port 5000 di komputer host (Windows) ke port 5000 di container.

```bash
docker run -d -p 5000:5000 --name web_flask localhost/flaskr:1.0.0
```

Untuk memverifikasi:
1. Buka browser dan kunjungi http://localhost:5000/. Aplikasi blog akan muncul dan sepenuhnya berjalan di dalam container Docker secara terisolasi.

![venv](images/Screenshot%202026-05-12%20190202.png)

2. Cek status container yang berjalan di PowerShell:
```bash
docker ps
```

![venv](images/Screenshot%202026-05-12%20190228.png)
![venv](images/Screenshot%202026-05-12%20190212.png)

---

### Kesimpulan

Pada praktikum Modul 7 ini, saya telah memahami konsep XaaS (SaaS, PaaS, IaaS) dalam Cloud Computing dan berhasil mempraktikkan langsung salah satu pilar teknologinya, yaitu Containerized App. Dengan menggunakan Docker, aplikasi web (Flask) beserta seluruh environment, dependensi, dan basis datanya berhasil dibungkus ke dalam sebuah image (localhost/flaskr:1.0.0). Image ini kemudian dapat dijalankan dengan mudah dan konsisten sebagai container di lingkungan apa pun, membuktikan portabilitas tingkat tinggi yang ditawarkan oleh teknologi Cloud Computing.