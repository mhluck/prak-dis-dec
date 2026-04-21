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
![port 80](images/Screenshot%202026-04-20%20233742.png)
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

### B. Failure Detection

Failure Detection adalah proses untuk menentukan apakah suatu komponen telah gagal . Di bagian ini, buat direktori failure-detection, masuk ke dalamnya, dan buat ketiga skrip berikut.

#### 1. Heartbeat
Protokol heartbeat memantau aktivitas komponen. Jika tidak ada respons dalam waktu tertentu, komponen diasumsikan gagal.

- Buat file check-server.py:

```bash
import socket
import sys

def check_server(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, int(port)))
        if result == 0:
            print("Server up")
        else:
            print("Server down")
        sock.close()
    except Exception:
        print("Server down")

if __name__ == "__main__":
    check_server(sys.argv[1], sys.argv[2])
```

Pengujian:
- Saat server mati (tab powershell 1):
```bash
python check-server.py localhost 44777
```
![server mati](images/Screenshot%202026-04-21%20085056.png)
Maka akan menghasilkan Server down. Kenapa? Karena skrip check-server.py mencoba "mengetuk pintu" di alamat localhost pada port 44777, tetapi tidak ada aplikasi yang merespons ketukan tersebut (port tertutup).

- Saat server nyala (tab powershell 2):
```bash
python dev.py
```
![server nyala](images/Screenshot%202026-04-21%20085110.png)

Tunggu sampai muncul tulisan "Uvicorn running on http://localhost:44777". Ini artinya server sudah standby.

- Kembali ke Tab Powershell tempat check-server.py
Jalankan perintah yang sama persis seperti sebelumnya:
```bash
python check-server.py localhost 44777
```
![cek ulang](images/Screenshot%202026-04-21%20085137.png)

Maka akan menghasilkan Server up. Kenapa? Karena kali ini, saat skrip mengetuk port 44777, aplikasi Blacksheep sedang jalan di Tab membalas sinyal tersebut, sehingga skrip tahu bahwa komponen tersebut masih hidup (heartbeat terdeteksi).

#### 2. Retry Mechanism (Tenacity)
- Buat file check-retry.py:

```bash
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def access_url(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url)
    response.raise_for_status()
    print(f"Successfully accessed {url}")

if __name__ == "__main__":
    try:
        access_url("http://localhost:44777")
    except Exception as e:
        print(f"Failed to access URL after multiple retries: RetryError {e}")
```

Library tenacity digunakan untuk mengulang koneksi jika terjadi kegagalan sementara.

**a. Menginstal Library**

Pastikan sudah berada di dalam direktori **workspace-05/failure-detection** dan virtual environment sudah aktif.
- Aktivasi Virtual Environment dan Instalasi Library:
```bash
.venv\Scripts\activate
uv pip install tenacity requests
```
![isntall tenacity](images/Screenshot%202026-04-21%20092941.png)

**b. Pengujian saat server nyala** 

-  Jalankan server aplikasi (workspace-05\blacksheep_lb):   
```bash
python dev.py
```
![jalankan server](images/Screenshot%202026-04-21%20092954.png)

- Kembali ke tab PowerShell failure-detection
```bash
python check-retry.py
```
![cek retry](images/Screenshot%202026-04-21%20093002.png)

Skrip langsung mencetak Attempting to access... dan segera disusul dengan Successfully accessed... pada percobaan pertama, karena server sedang berjalan dan siap menerima request.


**c. Pengujian saat server mati**

- Kembali ke tab PowerShell Blacksheep dan hentikan dengan CTRL+C.
- Kembali ke tab PowerShell failure-detection
```bash
python check-retry.py
```
![cek retry](images/Screenshot%202026-04-21%20093330.png)

Skrip mencetak Attempting to access..., lalu karena gagal (server mati), ia akan menunggu 2 detik (wait_fixed(2)), dan mencoba lagi. Proses ini akan berulang hingga 5 kali (stop_after_attempt(5)). Setelah percobaan ke-5 gagal, blok except menangkap error dan mencetak pesan kegagalan (Failed to access URL after multiple retries: RetryError...).

#### 3. Circuit Breaker

Pola circuit breaker mencegah kegagalan berantai dengan memblokir panggilan ke layanan yang gagal (status Open), memberi waktu untuk pulih, lalu mencoba lagi (Half-Open), dan kembali normal (Closed) jika berhasil .

- Buat file check-circuit-breaker.py:

```bash
import requests
import pybreaker

breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=5)

@breaker
def fetch_data(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url, timeout=2)
    response.raise_for_status()
    print(f"Successfully accessed {url}")

if __name__ == "__main__":
    try:
        fetch_data("http://localhost:44777")
    except Exception as e:
        print(e)
```

**a. Menginstal Library**

Pastikan sudah berada di dalam direktori **workspace-05/failure-detection** dan virtual environment sudah aktif.
- Aktivasi Virtual Environment dan Instalasi Library:
```bash
.venv\Scripts\activate
pip install pybreaker requests
```
![install ](images/Screenshot%202026-04-21%20100646.png)

**b. Pengujian saat server nyala** 

-  Jalankan server aplikasi (workspace-05\blacksheep_lb):   
```bash
python dev.py
```
![jalankan server](images/Screenshot%202026-04-21%20100715.png)

- Kembali ke tab PowerShell failure-detection
```bash
python check-circuit-breaker.py
```
![cek circuit breaker](images/Screenshot%202026-04-21%20100741.png)

Karena server nyala, maka akan langsung terlihat output sukses.


**c. Pengujian saat server mati**

- Kembali ke tab PowerShell Blacksheep dan hentikan dengan CTRL+C.
- Picuan Kegagalan Pertama hingga Ketiga

Kembali ke tab PowerShell failure-detection dan jalankan skrip pengujian diulangi sebanyak 3 kali:
```bash
python check-circuit-breaker.py
```
![cek 1-3](images/Screenshot%202026-04-21%20100933.png)

Terlihat jeda sekitar 2 detik (timeout) setiap kali dijalankan, lalu muncul error panjang (seperti Connection refused atau Max retries exceeded). Pada tahap ini, circuit breaker masih menghitung jumlah kegagalan.

- Sebelum percobaan keempat saya memodifikasi sedikit file check-circuit-breaker.py:
```bash
import requests
import pybreaker
import time

# Maksimal 3x gagal, lalu sirkuit Terbuka (Open) selama 5 detik
breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=5)

@breaker
def fetch_data(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url, timeout=2)
    response.raise_for_status()
    print(f"Successfully accessed {url}")

if __name__ == "__main__":
    # Kita buat looping 6 kali di dalam script
    for i in range(1, 7):
        print(f"\n--- Percobaan ke-{i} ---")
        try:
            fetch_data("http://localhost:44777")
        except Exception as e:
            # Mengambil pesan error aslinya agar lebih rapi
            print(f"Error: {e}")
        
        # Jeda 1 detik antar percobaan agar mudah diamati
        time.sleep(1)
```

- Memicu Pemutus Sirkuit (Percobaan Keempat)

```bash
python check-circuit-breaker.py
```
![cek 4](images/Screenshot%202026-04-21%20101805.png)

Pada Percobaan 1, 2, dan 3, terlihat error timeout jaringan seperti sebelumnya. Skrip masih mencoba menghubungi server selama 2 detik tiap percobaannya.

Begitu masuk ke Percobaan 4, 5, dan 6, tidak lagi terlihat error timeout yang panjang. Skrip langsung instan mencetak pesan error dari pemutus sirkuit: Error: Failures threshold reached, circuit breaker is open. Ini bukti bahwa circuit breaker telah aktif memblokir akses untuk menghemat resource sistem!

Saat pesan CircuitBreakerError muncul, sistem sedang berada di fase Open. Sistem tidak akan mencoba melakukan koneksi (menghemat resource) selama 5 detik (reset_timeout=5). Jika menunggu lebih dari 5 detik lalu menjalankannya lagi, sistem akan masuk ke fase Half-Open untuk mencoba satu koneksi uji coba. Jika server masih mati, sirkuit akan kembali Open.

---

### Kesimpulan
Praktikum ini mensimulasikan dua aspek krusial dalam sistem terdistribusi: Load Balancing dan Failure Detection.

- Load Balancing: Dengan memanfaatkan Nginx sebagai reverse proxy dan Docker Compose, saya berhasil mendistribusikan traffic masuk secara merata ke dalam beberapa instance aplikasi web (Blacksheep). Ini meningkatkan performa dan ketersediaan layanan (high-availability).
- Failure Detection & Handling: Sistem yang tangguh harus bisa mendeteksi dan menangani kegagalan komponen. Melalui skrip Python, saya mempraktikkan Heartbeat (untuk mengecek status server), Retry Mechanism (untuk mengatasi kegagalan jaringan sementara menggunakan tenacity), dan pola Circuit Breaker (untuk mencegah kegagalan berantai dengan memblokir permintaan secara terstruktur saat layanan down).

Implementasi di Windows menggunakan Docker Desktop dan PowerShell berhasil menjalankan ekosistem ini dengan lancar seperti pada lingkungan Linux aslinya.