# UTS Praktikum Sistem Terdistribusi - Load Balancing

Repositori ini berisi implementasi Load Balancing menggunakan **Nginx** sebagai reverse proxy dan **FastAPI** (Python) sebagai aplikasi backend. Seluruh infrastruktur dikemas dan dijalankan menggunakan **Podman** dan **Podman Compose**.

## Struktur Direktori

```text
.
├── app/
│   ├── Dockerfile       # Instruksi build untuk container FastAPI
│   └── main.py          # Source code backend FastAPI
├── nginx/
│   ├── Dockerfile       # Instruksi build untuk Nginx
│   └── nginx.conf       # Konfigurasi upstream dan load balancer
└── docker-compose.yml   # File orkestrasi Podman Compose
```

Berikut langkah-langkah yang saya lakukan:

1. **Pembuatan Backend**: Pertama, saya menulis source code aplikasi FastAPI di dalam folder app (main.py). Aplikasi ini saya atur agar mengembalikan respon berupa ID/Nama Server saat diakses, agar perbedaan replikanya terlihat.

2. **Containerization**: Saya membuat file Dockerfile di dalam folder aplikasi tersebut untuk membungkus kode FastAPI saya beserta dependensinya (base image Python) menjadi sebuah image yang siap dijalankan oleh Podman.

3. **Konfigurasi Load Balancer**: Saya membuat folder nginx dan mengisinya dengan file nginx.conf. Di dalamnya, saya menyetel blok upstream agar Nginx bisa bertindak sebagai pembagi beban lalu lintas jaringan (round-robin) ke aplikasi backend saya.

4. **Orkestrasi dengan Compose**: Saya menyatukan semuanya menggunakan file podman-compose.yml. File ini menginstruksikan Podman untuk membangun mesin Nginx (dibuka di port 80) yang saling terhubung dengan aplikasi FastAPI (yang port-nya disembunyikan agar aman).

5. **Eksekusi dan Scaling**: Lewat terminal PowerShell, saya mengetikkan perintah podman compose -f podman-compose.yml up -d --build --scale backend_app=3. Perintah ini menyulap aplikasi saya menjadi 3 container replika FastAPI yang berdiri di belakang 1 Nginx secara otomatis.

![venv](images/Screenshot%202026-05-18%20151242.png)

6. **Testing**: Saat saya menguji dengan mengakses curl http://localhost, tulisan "ID Server" yang muncul selalu berganti-ganti. Ini membuktikan bahwa pembagian beban (load balancing) telah berhasil dilakukan.

![venv](images/Screenshot%202026-05-18%20162932.png)
![venv](images/Screenshot%202026-05-18%20162943.png)
![venv](images/Screenshot%202026-05-18%20162952.png)