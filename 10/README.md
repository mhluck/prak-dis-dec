# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 10

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Data Terdistribusi (YugabyteDB)

Data terdistribusi merupakan salah satu strategi yang banyak digunakan untuk mengelola skalabilitas (kemampuan menangani beban data yang membesar) dan high availability (ketersediaan tinggi) dari data. Pada praktikum ini, implementasi data terdistribusi dilakukan menggunakan YugabyteDB, sebuah database SQL terdistribusi berkinerja tinggi. Karena YugabyteDB didesain untuk ekosistem Linux, eksekusi pada lingkungan Windows diimplementasikan dengan memanfaatkan Windows Subsystem for Linux (WSL).

---

### 1. Instalasi YugabyteDB di WSL

#### a. Mengunduh dan Mengekstrak YugabyteDB

- Mengunduh arsip YugabyteDB versi LTS (Long-Term Support) untuk Linux x86 menggunakan perintah wget di terminal WSL.

```bash
wget https://software.yugabyte.com/releases/2025.2.3.0/yugabyte-2025.2.3.0-b149-linux-x86_64.tar.gz
```

![venv](images/Screenshot%202026-06-02%20104032.png)

- Setelah berhasil diunduh, ekstrak file tersebut:

```bash
tar xvfz yugabyte-2025.2.3.0-b149-linux-x86_64.tar.gz
```

![venv](images/Screenshot%202026-06-02%20104139.png)

#### b. Memindahkan Direktori dan Membuat Symlink

- Pindahkan folder hasil ekstraksi ke subdirektori khusus (misalnya ~/software/dbms/) dan buat symbolic link (symlink) agar penamaan foldernya lebih sederhana.

```bash
mkdir -p ~/software/dbms
mv yugabyte-2025.2.3.0 ~/software/dbms/
cd ~/software/dbms
ln -s yugabyte-2025.2.3.0 yugabytedb
```

![venv](images/Screenshot%202026-06-02%20104458.png)

#### c. Konfigurasi Post-Install dan Ulimit

- Masuk ke direktori bin dan jalankan script post-install

```bash
cd ~/software/dbms/yugabytedb/bin
./post_install.sh
```

![venv](images/Screenshot%202026-06-02%20104546.png)

- Selanjutnya, ubah batas limit sistem operasi (ulimit) agar database memiliki izin mengalokasikan cukup memori dan file descriptors. Edit file konfigurasi sistem:

```bash
sudo nano /etc/security/limits.conf
```

![venv](images/Screenshot%202026-06-02%20105330.png)

- Tambahkan konfigurasi ulimit standar YugabyteDB di baris paling bawah sesuai dengan instruksi modul , lalu simpan dan restart WSL.

![venv](images/Screenshot%202026-06-02%20105222.png)

- Restart WSL
Buka aplikasi PowerShell Windows biasa (bukan terminal Ubuntu). Ketik perintah penonaktifan WSL, lalu tunggu beberapa detik, lalu buka kembali terminal Ubuntu/WSL:

```bash
wsl --shutdown
```

![venv](images/Screenshot%202026-06-02%20105644.png)

#### d. Konfigurasi Environment Variables

- Agar perintah yugabyted dapat dipanggil dari direktori mana saja, tambahkan jalurnya (PATH) ke dalam environment variables :

```bash
export PATH="$HOME/software/dbms/yugabytedb/bin:$HOME/software/dbms/yugabytedb/postgres/bin:$HOME/software/dbms/yugabytedb/tools:$PATH"
```

![venv](images/Screenshot%202026-06-02%20110126.png)

### 2. Membuat Klaster Terdistribusi (3 Nodes)

YugabyteDB akan disimulasikan berjalan di atas 3 node yang berbeda, masing-masing menyimpan datanya di direktori terpisah (node1, node2, node3).

#### a. Menjalankan Node 1 (Primary)

```bash
yugabyted start --advertise_address=127.0.0.1 --base_dir=$HOME/var/node1 --cloud_location=aws.us-east-2.us-east-2a
```

![venv](images/Screenshot%202026-06-02%20111649.png)

#### b. Menjalankan Node 2 dan Node 3 (Bergabung ke Node 1)

- Buka tab terminal WSL baru, jalankan Node 2 dengan mengarahkan perintah --join ke Node 1 :

```bash
yugabyted start --advertise_address=127.0.0.2 --base_dir=$HOME/var/node2 --cloud_location=aws.us-east-2.us-east-2b --join=127.0.0.1
```

![venv](images/Screenshot%202026-06-02%20111823.png)

- Lakukan hal yang sama untuk Node 3 :

```bash
yugabyted start --advertise_address=127.0.0.3 --base_dir=$HOME/var/node3 --cloud_location=aws.us-east-2.us-east-2c --join=127.0.0.1
```

![venv](images/Screenshot%202026-06-02%20111929.png)

#### c. Mengatur Data Placement & Verifikasi UI

- Setelah ketiga node aktif, atur penempatan data dengan toleransi kegagalan berbasis zona :

```bash
yugabyted configure data_placement --base_dir=$HOME/var/node1 --fault_tolerance=zone
```

![venv](images/Screenshot%202026-06-02%20112014.png)

Buka browser dan akses http://localhost:15433. Dapat dilihat antarmuka UI YugabyteDB yang mengonfirmasi bahwa 3 nodes (dengan total Replication Factor 3) sudah berjalan dengan status Alive.

![venv](images/Screenshot%202026-06-02%20112111.png)
![venv](images/Screenshot%202026-06-02%20112338.png)


### 3. Sharding Data dan Analisis

YugabyteDB membagi tabel menjadi beberapa bagian yang disebut tablet . Sharding adalah proses mendistribusikan baris-baris tabel ke berbagai tablet dalam klaster secara deterministik berdasarkan primary key . Hal ini memungkinkan akses cepat ke baris data tertentu. Terdapat dua mekanisme utama sharding, yaitu Range Sharding dan Hash Sharding.

![venv](images/Screenshot%202026-05-28%20193103.png)

Pada dasarnya ada 2 mekanisme untuk sharding, yaitu **range sharding** dan **hash sharding**.

Masuk ke dalam YSQL shell untuk melakukan pengujian:

```bash
ysqlsh -h 127.0.0.1 -U yugabyte -d yugabyte
```

![venv](images/Screenshot%202026-06-02%20112454.png)

#### A. Range Sharding

Range sharding secara default akan membentuk hanya 1 tablet untuk 1 tabel.
Pembuatan tabel dan input data:

```bash
CREATE TABLE user_range (id INT, name VARCHAR(50), PRIMARY KEY(id ASC));

INSERT INTO user_range VALUES (1, 'user range 1'), (2, 'user range 2'), (3, 'user range 3'), (4, 'user range 4'), (5, 'user range 5'), (6, 'user range 6');
```

![venv](images/Screenshot%202026-06-02%20112731.png)

Analisis EXPLAIN pada tabel user_range:

```bash
EXPLAIN (ANALYZE, DIST, COSTS OFF) SELECT * FROM user_range;
```

![venv](images/Screenshot%202026-06-02%20112815.png)

```bash
EXPLAIN (ANALYZE, DIST, COSTS OFF) SELECT * FROM user_range WHERE id=1;   
```

![venv](images/Screenshot%202026-06-02%20112848.png)

```bash
EXPLAIN (ANALYZE, DIST, COSTS OFF) SELECT * FROM user_range WHERE id > 2 and id < 6;
```

![venv](images/Screenshot%202026-06-02%20112911.png)

Kesimpulan dari ketiga EXPLAIN di atas:
1. Untuk query * (semua baris): Sistem membaca semua baris data.
2. Untuk query satu baris (id=1): Data yang dibaca persis 1 baris.
3. Untuk query range (id>2 and id<6): Data yang dibaca persis sama dengan jumlah yang sesuai range (tidak membaca semua data dari awal).

Range Sharding dengan SPLIT (Beberapa Tablet):
Jika ingin langsung membagi tabel menjadi beberapa shards (tablets), gunakan SPLIT AT VALUES.

```bash
CREATE TABLE users (
    user_id INT,
    username VARCHAR,
    PRIMARY KEY (user_id ASC)
) SPLIT AT VALUES ((3), (6), (9));

INSERT INTO users VALUES (1, 'user 1'), (2, 'user 2'), (3, 'user 3'), (4, 'user 4'), (5, 'user 5'), (6, 'user 6');
```

![venv](images/Screenshot%202026-06-02%20113116.png)

Tabel users di atas dibagi menjadi 4 tablets (tablet 1: id 1,2,3 | tablet 2: id 4,5,6 | tablet 3: id 7,8,9 | tablet 4: id 10 dst) . Untuk tabel yang di-split ini, waktu eksekusi akan lebih cepat untuk query spesifik.

```bash
EXPLAIN SELECT * FROM users WHERE user_id = 1;
```

![venv](images/Screenshot%202026-06-02%20113158.png)

Saat diuji dengan EXPLAIN SELECT * FROM users WHERE user_id = 1;, terlihat sistem langsung menargetkan tablet yang sesuai sehingga waktu eksekusi (Execution Time) menurun .

#### B. Hash Sharding

Hash sharding mendistribusikan data menggunakan nilai hash, namun tidak sesuai/kurang efisien untuk hasil pembacaan berupa range .
Pembuatan tabel dan input data:

```bash
CREATE TABLE user_hash (id INT, name VARCHAR, PRIMARY KEY(id HASH));

INSERT INTO user_hash VALUES (1, 'user hash 1'), (2, 'user hash 2'), (3, 'user hash 3'), (4, 'user hash 4'), (5, 'user hash 5'), (6, 'user hash 6');
```

![venv](images/Screenshot%202026-06-02%20113258.png)

Analisis EXPLAIN pada tabel user_hash:
```bash
EXPLAIN (ANALYZE, DIST, COSTS OFF) SELECT * FROM user_hash;
```

![venv](images/Screenshot%202026-06-02%20113328.png)

```bash
EXPLAIN (ANALYZE, DIST, COSTS OFF) SELECT * FROM user_hash WHERE id=1;   
```

![venv](images/Screenshot%202026-06-02%20113355.png)

```bash
EXPLAIN (ANALYZE, DIST, COSTS OFF) SELECT * FROM user_hash WHERE id>2 AND id<6;
```

![venv](images/Screenshot%202026-06-02%20113419.png)

Kesimpulan dari ketiga EXPLAIN di atas:

1. Untuk query * (semua baris): Data yang dibaca adalah semua baris, dan permintaan read disebar ke sejumlah tablets yang ada.
2. Untuk query satu baris (id=1): Data yang dibaca persis 1 baris dengan sangat cepat karena hash langsung menunjuk ke tablet yang tepat.
3. Untuk query range (id>2 AND id<6): Sistem membaca keseluruhan baris data (6 baris) yang kemudian difilter (Storage Filter), padahal yang diperlukan hanya 3 baris sesuai range. Ini membuktikan hash sharding tidak efisien untuk query range.


### 4. Shutdown YugabyteDB

Setelah selesai, klaster harus dihentikan secara aman menggunakan perintah stop dengan mendefinisikan lokasi direktorinya secara spesifik :

```bash
yugabyted stop --base_dir=$HOME/var/node1
yugabyted stop --base_dir=$HOME/var/node2
yugabyted stop --base_dir=$HOME/var/node3
```

![venv](images/Screenshot%202026-06-02%20113633.png)

### 5. Yugabyte University Certification (Tugas)

![venv](images)

---

### Kesimpulan

Praktikum Modul 10 ini memberikan pemahaman konkret mengenai bagaimana sebuah Distributed SQL Database (YugabyteDB) bekerja dalam mengelola High Availability dan Skalabilitas data. Pemecahan tabel menjadi tablets melalui teknik Sharding terbukti krusial dalam mendistribusikan beban kerja ke berbagai node. Melalui perbandingan eksekusi SQL, dapat disimpulkan bahwa Range Sharding optimal untuk pencarian data berurutan (rentang/range), sementara Hash Sharding sangat cepat dan merata untuk pencarian berbasis kunci spesifik (titik/point lookup) namun sangat buruk performanya jika digunakan untuk pencarian berbasis rentang.