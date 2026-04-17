# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 4

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Konsistensi dan Replikasi pada Sistem Terdistribusi

Praktikum ini dieksekusi menggunakan sistem operasi Windows. Oleh karena itu, penggunaan skrip env.sh (alias Bash) yang ada pada modul digantikan dengan eksekusi perintah raw Docker Compose dan Docker CLI melalui PowerShell/Command Prompt.

---

### A. Streaming Replication Menggunakan PostgreSQL

Materi ini mendemonstrasikan cara mengkonfigurasi replikasi streaming (Single-Primary) pada PostgreSQL 18 menggunakan kontainer Docker.

#### 1. Persiapan Direktori dan File (Windows)

Buat sebuah direktori baru streaming-replication, lalu buat dua file berikut di dalamnya. (File env.sh diabaikan karena saya menggunakan Windows).

- **File 1: 00_init.sql**
Berfungsi untuk membuat user replikator dan slot replikasi pada primary server.

```bash
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');
```

- **File 2: docker-compose.yaml**
Konfigurasi infrastruktur untuk Primary dan Replica server.

```bash
x-postgres-common:
  &postgres-common
  image: postgres:18.3-alpine3.23
  user: postgres
  restart: always
  healthcheck:
    test: 'pg_isready -U zuser --dbname=zdb'
    interval: 10s
    timeout: 5s
    retries: 5

services:
  postgres_primary:
    <<: *postgres-common
    ports:
      - 5432:5432
    environment:
      POSTGRES_USER: zuser
      POSTGRES_DB: zdb
      POSTGRES_PASSWORD: zpass
      POSTGRES_HOST_AUTH_METHOD: "scram-sha-256\nhost replication replicator 0.0.0.0/0 md5"
      POSTGRES_INITDB_ARGS: "--auth-host-scram-sha-256"
    command: |
      postgres
      -c wal_level=replica
      -c hot_standby=on
      -c max_wal_senders=10
      -c max_replication_slots=10
      -c hot_standby_feedback=on
    volumes:
      - ./00_init.sql:/docker-entrypoint-initdb.d/00_init.sql

  postgres_replica:
    <<: *postgres-common
    ports:
      - 5433:5432
    environment:
      PGUSER: replicator
      PGPASSWORD: replicator_password
      PGDATA: /var/lib/postgresql/18/docker
    command: |
      bash -c "
      until pg_basebackup --pgdata=/var/lib/postgresql/18/docker -R --slot=replication_slot --host=postgres_primary --port=5432 -X stream; do
        echo 'pg_basebackup failed. Retrying in 5 seconds...'
        sleep 5
      done
      echo 'Backup done, starting replica...'
      chmod 0700 /var/lib/postgresql/18/docker
      postgres
      "
    depends_on:
      - postgres_primary
```

#### 2. Menjalankan dan Menguji Cluster

- **1. Menjalankan Docker Compose**
Buka PowerShell di dalam direktori streaming-replication, lalu jalankan:

```bash
docker-compose up -d
```
Proses pull image selesai dan kontainer berjalan.

![pull image](images/Screenshot%202026-04-16%20090845.png)

Cek statusnya dengan docker ps. Pastikan status keduanya adalah healthy.

![status healty](images/Screenshot%202026-04-18%20011545.png)

- **2. Verifikasi Status Recovery pada Replica**
Masuk ke dalam kontainer replica untuk memastikan ia berjalan sebagai standby server.
```bash
docker exec -it streaming-replication-postgres_replica-1 psql -U zuser -d zdb
```
Jalankan query diagnostik
```bash
SELECT pg_is_in_recovery();
```

![verifikasi](images/Screenshot%202026-04-18%20012513.png)
Hasil: t (True). Ini membuktikan server ini adalah replica yang hanya menerima sinkronisasi data (read-only).
- **3. Pengujian Manipulasi Data (Sinkronisasi)**

Buka tab PowerShell baru, masuk ke kontainer primary:
```bash
PowerShelldocker exec -it streaming-replication-postgres_primary-1 psql -U zuser -d zdb
```
Buat tabel dan masukkan data:
```bash
CREATE TABLE testrep (first INT, second VARCHAR(15));
INSERT INTO testrep (first, second) VALUES (21, 'Test pertama');
INSERT INTO testrep (first, second) VALUES (23, 'Test ke dua');
```
![manipulasi data](images/Screenshot%202026-04-18%20012702.png)
Kembali ke jendela PowerShell yang menjalankan replica (langkah 2), lalu cek tabelnya:
```bash
SELECT * FROM testrep;
```

![cek tabel](images/Screenshot%202026-04-18%20012750.png)
Hasil: Data 21 dan 23 akan muncul di server replica secara otomatis, membuktikan replikasi streaming berjalan sukses .

#### 3. High-Availability (Failover)

Model ini mendukung High Availability. Jika server primary mati akan tetap bisa mempromosikan replica menjadi primary.

- Matikan primary server:
```bash
docker-compose stop postgres_primary
```
![server mati](images/Screenshot%202026-04-18%20015522.png)

- Pada replica server, jalankan fungsi promosi:
```bash
SELECT pg_promote();
```
![replika server](images/Screenshot%202026-04-18%20015650.png)

- Cek kembali status recovery:
```bash
SELECT pg_is_in_recovery();
```
![cek](images/Screenshot%202026-04-18%20015802.png)
Hasil: f (False). Server replica kini telah mengambil alih peran sebagai primary dan dapat melakukan operasi read-write.

- Bersihkan environment:
```bash
PowerShelldocker-compose down
```
![clear env](images/Screenshot%202026-04-18%20015911.png)
### B. Replikasi Master-Master Menggunakan Apache Ignite
Bagian ini mengkonfigurasi kluster Apache Ignite 3.1.0 dengan mode Master-Master, di mana semua node memiliki kemampuan read-write dan saling mereplikasi.

#### 1. Persiapan File
- Buat folder baru bernama ignite-cluster.
- Unduh file docker-compose.yml dari dokumentasi resmi Apache Ignite dan letakkan di folder ini.
- Unduh sql.zip dari tautan resmi, lalu ekstrak ke dalam folder bernama sql di direktori yang sama. Struktur folder Anda akan menjadi:
    - docker-compose.yml
    - sql/ (berisi file schema.sql, tracks.sql, dll)

#### 2. Inisialisasi Cluster (Windows Adaptation)

- Jalankan kluster:
```bash
PowerShelldocker-compose up -d
```
![jalankan cluster](images/Screenshot%202026-04-18%20021654.png)
Ini akan menjalankan 3 node Ignite (Port 10300, 10301, 10302 untuk REST API).

- Jalankan Apache Ignite CLI menggunakan Docker (disesuaikan untuk Windows dengan memetakan volume absolut menggunakan ${PWD}):
```bash
docker run --rm -it --network host -v ${PWD}/sql:/opt/ignite/sql apacheignite/ignite:3.1.0 cli
```
![cli](images/Screenshot%202026-04-18%20021800.png)

- Di dalam prompt CLI Ignite, hubungkan ke node default (Y), lalu inisialisasi kluster:
```bash
cluster init --name ignite3 --metastorage-group node1,node2,node3
```
![node default](images/Screenshot%202026-04-18%20021907.png)
Pastikan muncul pesan Cluster was initialized successfully.

#### 3. Eksekusi SQL dan Verifikasi Replikasi

- Di dalam CLI Ignite yang sama, eksekusi file SQL yang telah di-mount untuk membuat skema dan memuat data sampel. Lakukan secara berurutan :

```bash
sql --file=/opt/ignite/sql/schema.sql
sql --file=/opt/ignite/sql/current_catalog.sql
sql --file=/opt/ignite/sql/media_and_genre.sql
sql --file=/opt/ignite/sql/tracks.sql
sql --file=/opt/ignite/sql/ee_and_cust.sql
sql --file=/opt/ignite/sql/invoices.sql
```
![sql](images/Screenshot%202026-04-18%20022550.png)
![sql](images/Screenshot%202026-04-18%20022604.png)
![sql](images/Screenshot%202026-04-18%20022621.png)

**Verifikasi Data Tersinkronisasi Lintas Node:**
Secara default, kita mengeksekusi SQL di localhost:10300. Sekarang kita akan memeriksa apakah data tersebut direplikasi ke node lain (misalnya 10301 atau 10302).

- Pindah koneksi ke Node 2:
```bash
connect http://localhost:10301
```
![pindah node](images/Screenshot%202026-04-18%20023120.png)

- Jalankan query:
```bash
sql
sql-cli> SELECT * FROM system.tables WHERE schema = 'PUBLIC';
```
![sql](images/Screenshot%202026-04-18%20023803.png)

- Terakhir, matikan kluster dari PowerShell:
```bash
docker-compose down
```
![down](images/Screenshot%202026-04-18%20024213.png)

### Kesimpulan

Praktikum minggu keempat ini berhasil mengimplementasikan dan menguji dua strategi utama dalam mengelola konsistensi dan replikasi pada sistem terdistribusi, yaitu replikasi streaming model Single-Primary menggunakan PostgreSQL dan replikasi Master-Master menggunakan kluster Apache Ignite. Model Single-Primary terbukti efektif untuk skenario High Availability karena kemampuannya mendistribusikan data ke node read-only secara real-time dan kesiapannya melakukan failover saat primary server mengalami kegagalan. Di sisi lain, model Master-Master pada Apache Ignite menawarkan fleksibilitas dan skalabilitas superior di mana setiap node memiliki otoritas penuh untuk operasi baca-tulis, dan data langsung tersinkronisasi secara konsisten ke seluruh kluster, menjadikannya arsitektur yang ideal untuk mendistribusikan beban kerja secara merata sekaligus memastikan toleransi kesalahan yang tinggi. Seluruh simulasi ini dieksekusi dengan efisien di lingkungan Windows berkat kemampuan isolasi dan orkestrasi dari Docker Compose.