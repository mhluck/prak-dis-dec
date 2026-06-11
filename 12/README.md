# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 12

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Teknologi P2P (Peer-to-Peer)

Praktikum ini membahas mengenai konsep dan implementasi dari teknologi Peer-to-Peer (P2P). Teknologi P2P terdiri atas sekumpulan nodes yang terhubung secara langsung satu sama lain tanpa memerlukan adanya sebuah server pusat bertindak sebagai perantara. Dalam arsitektur ini, setiap node memiliki kedudukan yang setara di mana ia dapat berfungsi sebagai client sekaligus sebagai server (hybrid role). Beberapa contoh implementasi nyata dari pemanfaatan teknologi ini meliputi sistem berbagi berkas (file sharing), aplikasi percakapan (chatting), hingga ekosistem permainan (games).

---

### 1. Koneksi Antar Nodes (Simple Chat)

Koneksi mendasar antar node pada arsitektur P2P diimplementasikan menggunakan pemrograman network socket dan multithreading di Python. Mekanisme ini memungkinkan sebuah program mendengarkan koneksi masuk (listening) sekaligus mengirimkan data ke target lain secara simultan.

#### A. Pembuatan Source Code

- Buat sebuah berkas bernama simple_chat.py, lalu salin kode program berikut:

```python
import socket
import threading
import sys
import time

def terima_pesan(port_saya):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Mengikat socket ke semua interface pada port lokal yang ditentukan
        server_socket.bind(('0.0.0.0', port_saya))
        server_socket.listen(1)
        print(f"\n[SERVER] Mendengarkan di port {port_saya}...", file=sys.stderr)
        
        koneksi, alamat_peer = server_socket.accept()
        print(f"\n[SERVER] Terhubung dengan peer: {alamat_peer}", file=sys.stderr)
        
        while True:
            data = koneksi.recv(1024)
            if not data:
                print("\n[SERVER] Peer memutuskan koneksi.", file=sys.stderr)
                break
            print(f"\n[Peer]: {data.decode('utf-8')}")
    except Exception as e:
        print(f"[SERVER] Error: {e}", file=sys.stderr)
    finally:
        server_socket.close()

def kirim_pesan(ip_tujuan, port_tujuan):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[CLIENT] Mencoba terhubung ke {ip_tujuan}:{port_tujuan}...", file=sys.stderr)
    try:
        client_socket.connect((ip_tujuan, port_tujuan))
        print("[CLIENT] Sukses terhubung!", file=sys.stderr)
        print("Silakan ketik pesan dan tekan Enter (Ketik 'keluar' untuk berhenti):")
        while True:
            pesan = input()
            if pesan.lower() == 'keluar':
                break
            client_socket.sendall(pesan.encode('utf-8'))
    except Exception as e:
        print(f"[CLIENT] Gagal terhubung atau mengirim pesan: {e}", file=sys.stderr)
    finally:
        client_socket.close()

if __name__ == "__main__":
    print("=== Praktikum Modul 12 Sub 01 ===")
    port_lokal = int(input("Masukkan PORT LOKAL untuk server Anda (contoh: 5001): "))
    
    # Menjalankan fungsi terima_pesan di dalam thread terpisah
    thread_server = threading.Thread(target=terima_pesan, args=(port_lokal,))
    thread_server.daemon = True
    thread_server.start()
    
    time.sleep(1)
    print("\n--- Konfigurasi Hubungan ke Peer Lain ---")
    ip_target = input("Masukkan IP TARGET (Peer tujuan, contoh: localhost): ")
    port_target = int(input("Masukkan PORT TARGET (Port server peer tujuan): "))
    
    # Jalankan pengiriman pesan
    kirim_pesan(ip_target, port_target)
    print("\nProgram Selesai.")
```

#### B. Eksekusi Program (Tugas 1)

Untuk mensimulasikan komunikasi antar-node, buka dua terminal PowerShell secara berdampingan di Windows:

- Terminal Node 1: Jalankan python simple_chat.py, set port lokal ke 5001, IP target ke localhost, dan port target ke 5002.

![venv](images/Screenshot%202026-06-11%20204241.png)

- Terminal Node 2: Jalankan python simple_chat.py, set port lokal ke 5002, IP target ke localhost, dan port target ke 5001.

![venv](images/Screenshot%202026-06-11%20204254.png)

#### Analisis Hasil Eksperimen Program simple_chat.py

Berdasarkan eksperimen yang dilakukan pada Terminal 1 dan Terminal 2, terdapat dua skenario jalannya program yang merepresentasikan karakteristik arsitektur network socket TCP pada jaringan P2P:

**1. Analisis Sesi Percobaan 1: Kegagalan Jaringan (Connection Refused)**

Pada percobaaan awal di kedua terminal, muncul pesan kesalahan:
`[WinError 10061] No connection could be made because the target machine actively refused it`.

- Penyebab: Kondisi ini terjadi karena adanya ketidaksinkronan waktu eksekusi (asynchronous timing). Terminal 1 sudah melompat ke tahap Client untuk mencoba menghubungi port `5002` , padahal saat itu Terminal 2 belum dijalankan (belum membuka port server `5002` untuk mendengarkan koneksi).


- Mekanisme Protokol: Protokol TCP menerapkan aturan jabat tangan yang ketat (Three-way Handshake). Jika sebuah node mencoba mengetuk suatu alamat port target yang statusnya belum terbuka atau belum listening, sistem operasi Windows secara aktif akan menolak paket request tersebut demi keamanan, sehingga program langsung terhenti dengan status Program Selesai.



**2. Analisis Sesi Percobaan 2: Keberhasilan Jaringan (Establish Connection)**

Pada percobaan kedua, proses sinkronisasi diperbaiki dengan memastikan kedua server di port `5001` dan `5002` telah sama-sama berada dalam status `[SERVER] Mendengarkan...` sebelum konfigurasi IP dan Port target dimasukkan.

- Proses Hubungan Client: Setelah port target aktif, eksekusi fungsi `client_socket.connect()` menghasilkan status `[CLIENT] Sukses terhubung!`.

- Proses Terima Server: Di sisi lain, background thread server masing-masing node berhasil menangkap sinyal tersebut via `server_socket.accept()`, ditandai dengan munculnya log data biner: `[SERVER] Terhubung dengan peer: ('127.0.0.1', 65343)`. Angka 65343 tersebut merupakan port acak (ephemeral port) yang dialokasikan otomatis oleh sistem operasi untuk jalur komunikasi keluar.

- Aliran Pertukaran Pesan (Data Stream): Terminal 1 mengirimkan pesan `"Hei 5002"` menggunakan fungsi `.sendall()`.

    - Terminal 2 berhasil membaca pesan tersebut lewat fungsi `.recv(1024)` dan mencetaknya di layar berupa tulisan `[Peer]: Hei juga 5001`.

- Terminasi Jaringan: Ketika pengguna mengetik kata kunci `"keluar"`, perulangan while pengiriman pesan akan pecah (break). Socket client ditutup secara aman (`.close()`), yang kemudian memicu server lawan menerima data kosong (`if not data`). Server pun ikut memutus koneksi secara bersih hingga memunculkan status akhir `Program Selesai`.

#### C. Penjelasan Potongan Kode (Tugas 2)

Analisis potongan kode program:
- Membuka port untuk menerima dan mengirim pesan: Pembuatan objek socket menggunakan protokol TCP (socket.SOCK_STREAM) dijalankan oleh baris socket.socket(socket.AF_INET, socket.SOCK_STREAM). Proses pengikatan port lokal memanfaatkan perintah server_socket.bind(('0.0.0.0', port_saya)).
- Menerima pesan: Penanganan pesan masuk berjalan secara asinkron di dalam background thread melalui fungsi terima_pesan. Blok utamanya adalah perintah blocking server_socket.accept() untuk menerima jabat tangan koneksi dan koneksi.recv(1024) untuk membaca aliran biner data dari jaringan yang kemudian dikonversi ke teks lewat fungsi .decode('utf-8').
- Mengirim pesan: Proses input data di terminal diambil melalui fungsi input() yang kemudian dikonversi menjadi biner beralgoritma UTF-8 melalui .encode('utf-8'). Blok biner data dikirimkan secara langsung menuju network buffer tujuan menggunakan perintah client_socket.sendall(...).

---

### 2. DHT (Distributed Hash Table)

DHT merupakan struktur data terdistribusi yang digunakan oleh sistem P2P untuk memetakan pencarian berkas secara desentralisasi tanpa bergantung pada sebuah direktori server pusat.

#### A. Pembuatan Source Code

- Buat sebuah berkas bernama dht.py, lalu masukkan kode berikut:

```python
import hashlib

def hitung_hash_8bit(teks):
    # Menggunakan SHA-1 dan mengambil 2 karakter terakhir untuk representasi 8-bit (0-255)
    sha1 = hashlib.sha1(teks.encode('utf-8')).hexdigest()
    return int(sha1[-2:], 16)

class NodeP2P:
    def __init__(self, nama_node):
        self.nama = nama_node
        self.id = hitung_hash_8bit(nama_node)
        self.penyimpanan_lokal = {}
        print(f"Node '{self.nama}' berhasil dibuat dengan ID: {self.id}")

class LingkaranDHT:
    def __init__(self):
        self.daftar_node = []

    def tambah_node(self, node):
        self.daftar_node.append(node)
        self.daftar_node.sort(key=lambda x: x.id) # Diurutkan membentuk struktur Ring

    def cari_node_terdekat(self, key_data):
        # Algoritma pencarian node terdekat (Successor) dalam konsep Ring Topology
        for node in self.daftar_node:
            if node.id >= key_data:
                return node
        return self.daftar_node[0] # Memutar kembali ke awal ring jika key melewati ID node terbesar

    def simpan_data(self, nama_file, isi_konten):
        key_data = hitung_hash_8bit(nama_file)
        node_target = self.cari_node_terdekat(key_data)
        node_target.penyimpanan_lokal[key_data] = (nama_file, isi_konten)
        print(f"[SIMPAN] File '{nama_file}' (Key ID: {key_data}) disimpan di Node '{node_target.nama}' (Node ID: {node_target.id})")

    def cari_data(self, nama_file):
        key_data = hitung_hash_8bit(nama_file)
        node_target = self.cari_node_terdekat(key_data)
        print(f"\n[PENCARIAN] Mencari file '{nama_file}' dengan Key ID: {key_data}...")
        print(f"[ROUTING] Request diarahkan ke Node terdekat: '{node_target.nama}' (Node ID: {node_target.id})")
        
        if key_data in node_target.penyimpanan_lokal:
            nama, konten = node_target.penyimpanan_lokal[key_data]
            print(f" [SUKSES] Data ditemukan! Isi konten: '{konten}'")
        else:
            print(" [GAGAL] Data tidak ditemukan di jaringan.")

if __name__ == "__main__":
    print("=== Praktikum Modul 12 Teknologi P2P Simulasi DHT ===")
    dht = LingkaranDHT()
    
    node_a = NodeP2P("Node A")
    node_b = NodeP2P("Node B")
    node_c = NodeP2P("Node C")
    
    dht.tambah_node(node_a)
    dht.tambah_node(node_b)
    dht.tambah_node(node_c)
    
    print("\nUrutan Node dalam Lingkaran DHT (Ring):")
    for n in dht.daftar_node:
        print(f" -> Node ID: {n.id} ({n.nama})")
        
    dht.simpan_data("tugas_jaringan.pdf", "Konten: Laporan Praktikum Modul 1")
    dht.simpan_data("foto_makrab.jpg", "Konten: Data biner gambar makrab angkatan")
    dht.simpan_data("source_code.py", "Konten: print('Hello P2P')")
    
    dht.cari_data("tugas_jaringan.pdf")
    dht.cari_data("source_code.py")
    dht.cari_data("praktikum.py")
```

#### B. Eksekusi & Penjelasan Singkat (Tugas 1 & 2)

- Jalankan python dht.py

![venv](images/Screenshot%202026-06-11%20205201.png)

**Penjelasan Singkat Program:**
Program ini mensimulasikan penyimpanan dan pencarian berkas secara terdistribusi menggunakan konsep Consistent Hashing. Cara kerjanya dapat diringkas menjadi tiga langkah:
- Pembentukan Ring: Setiap node diberikan ID unik (A=129, B=217, C=92) dan diurutkan membentuk topologi cincin (Ring).
- Penyimpanan (Routing): Saat menyimpan berkas, sistem menghitung Key ID berkas tersebut dan mengalokasikannya ke node terdekat yang memiliki ID lebih besar atau sama (Successor). Contohnya, berkas dengan Key ID 115 dialokasikan ke Node A (ID 129).
- Pencarian (Lookup): Karena algoritma ini konsisten, pencarian berkas akan selalu menghasilkan rute yang sama. Sistem langsung melompat ke node target (seperti Node A untuk ID 115) dan memeriksa ketersediaan berkas tanpa perlu membebani atau mencari di node lainnya.

#### C. Analisis Mekanisme & Algoritma Routing DHT (Tugas 3)

DHT menggunakan konsep topologi lingkaran logika (Logical Ring Topology). Mekanisme pencariannya tidak memerlukan metode penyiaran data ke seluruh isi jaringan (broadcasting flood), melainkan langsung melompati indeks node berdasarkan hukum kedekatan nilai numerik hash key data.
Algoritma Pencarian (Lookup) Data pada DHT Berdasarkan Program:
- Hashing Parameter: Hitung nilai Hash ID dari nama berkas yang dicari menggunakan fungsi hashing (algoritma SHA-1 yang dipotong menjadi 8-bit) untuk mendapatkan nilai key_data.
- Iterasi Node: Lakukan iterasi pencarian secara berurutan pada daftar node aktif yang sebelumnya telah terurut menaik (Ascending) berdasarkan nilainya untuk membentuk struktur ring.
- Penentuan Successor (Kondisi Utama): Jika selama iterasi ditemukan node yang memiliki nilai node.id $\ge$ key_data, maka putuskan node pertama yang memenuhi kondisi tersebut sebagai tempat penyimpanan target (Successor Node).
- Penanganan Batas (Wrap-around): Jika hasil iterasi telah mencapai ujung daftar dan tidak ada satupun node yang memiliki ID lebih besar atau sama dengan key_data, maka struktur ring akan memutar kembali arah kembalian menuju node dengan ID terkecil pada urutan indeks paling awal (daftar_node[0]).
- Validasi Data: Alihkan request langsung menuju node target yang telah ditentukan pada langkah 3 atau 4. Sistem kemudian memeriksa ketersediaan key di dalam kamus penyimpanan_lokal milik node target tersebut.
- Hasil: Jika data ditemukan, kembalikan isi konten berkas ([SUKSES]). Jika absen, tampilkan pesan bahwa data tidak ada ([GAGAL])

---

### 3. Torrent

Teknologi Torrent bekerja dengan cara memotong berkas berukuran besar menjadi pecahan data kecil (pieces). Berkas berekstensi .torrent bertindak sebagai metadata biner terenkripsi berformat Bencode yang menyimpan sidik jari digital berkas tersebut.

#### A. Pembuatan Source Code yang Fleksibel (Tugas 3)

Sesuai dengan instruksi Tugas 3 pada halaman 10, program pembaca metadata torrent bawaan modul dimodifikasi agar dapat menerima parameter input jalur berkas langsung dari baris perintah (command-line arguments) menggunakan modul sys.

- Menginstal pustaka parser bencode terlebih dahulu melalui perintah: pip install bcoding

![venv](images/Screenshot%202026-06-11%20211017.png)

- Buat sebuah berkas bernama read_torrent.py dan salin kode di bawah ini:

```python
import bcoding
import hashlib
import sys

def baca_metadata_torrent(path_file_torrent):
    print(f"=== ANALISIS METADATA TORRENT: {path_file_torrent} ===")
    try:
        with open(path_file_torrent, 'rb') as f:
            data_torrent = bcoding.bdecode(f)
        
        print(f" [TRACKER URL]: {data_torrent.get('announce')}")
        
        info = data_torrent.get('info')
        if info:
            print(f" [NAMA FILE]  : {info.get('name')}")
            print(f" [UKURAN FILE] : {info.get('length')} bytes")
            print(f" [UKURAN PIECE]: {info.get('piece length')} bytes")
            
            info_bencoded = bcoding.bencode(info)
            info_hash = hashlib.sha1(info_bencoded).hexdigest()
            print(f" [INFO HASH]  : {info_hash}")
            
            jumlah_pieces = len(info.get('pieces')) // 20
            print(f" [TOTAL PIECES]: {jumlah_pieces} potongan")
            
    except FileNotFoundError:
        print("Gagal: File .torrent tidak ditemukan. Pastikan path benar.")
    except Exception as e:
        print(f"Error saat membaca torrent: {e}")

if __name__ == "__main__":
    # Mengambil argumen nama file dari terminal
    if len(sys.argv) < 2:
        print("Cara penggunaan: python read_torrent.py <namafile.torrent>")
    else:
        nama_file_target = sys.argv[1]
        baca_metadata_torrent(nama_file_target)
```

#### B. Pengujian Eksperimen (Tugas 1)

- Unduh salah satu berkas berkuran kecil berekstensi .torrent. Buka browser Windows  dan kunjungi: https://ubuntu.com/download/alternative-downloads, Scroll ke bawah sampai  menemukan bagian BitTorrent, klik salah satu link, misalnya Ubuntu 24.04 LTS Desktop, file bernama ubuntu-24.04.4-desktop-amd64.iso.torrent akan langsung terunduh.

- Jalankan perintah dengan argumen dinamis melalui terminal PowerShell:

```bash
python read_torrent.py ubuntu-24.04.4-desktop-amd64.iso.torrent
```
![venv](images/Screenshot%202026-06-11%20211800.png)

#### C. Analisis Output Program (Tugas 2)

Berdasarkan output saat membaca file ubuntu-24.04.4-desktop-amd64.iso.torrent, program berhasil membedah dan menampilkan data tersebut karena file .torrent pada dasarnya adalah struktur dictionary (kamus data) biner yang dikompresi menggunakan standar format Bencode. Fungsi bcoding.bdecode(f) mengonversi data biner tersebut kembali menjadi objek yang bisa dibaca oleh Python.

Berikut adalah alasan spesifik dari output yang dihasilkan:
1. [TRACKER URL]: Program mencari nilai dari key announce di dalam dictionary Bencode. Hasilnya adalah https://torrent.ubuntu.com/announce. Ini adalah alamat server pusat tempat di mana protokol BitTorrent klien kita akan melapor dan meminta daftar alamat IP pengguna lain (swarm) yang sedang membagikan file Ubuntu tersebut.  
2. [INFO HASH]: Menghasilkan deret karakter 01c13728.... Nilai ini didapat karena program mengambil struktur kamus info secara spesifik, melakukan proses bencode ulang menjadi bentuk biner murni, lalu menghitung sidik jari digitalnya menggunakan algoritma hash SHA-1. Ini menjadi ID unik file ISO Ubuntu tersebut di jaringan global P2P.
3. [TOTAL PIECES]: Menghasilkan 25390 potongan. Logika program di balik angka ini adalah: Data key pieces menyimpan rentetan hash SHA-1 dari seluruh pecahan file. Karena panjang standar satu hash SHA-1 adalah pasti 20 byte, maka total potongannya dihitung dari total panjang data dibagi 20 (menggunakan perintah len(...) // 20). (Pembuktian: 25390 potongan $\times$ ukuran per piece 262144 bytes = 6.655.825.920 bytes, yang nilainya sangat mendekati/setara dengan Ukuran File total).

---

### Kesimpulan

Praktikum Modul 12 memberikan pemahaman mendalam tentang fleksibilitas arsitektur Teknologi P2P (Peer-to-Peer). Melalui implementasi pembuatan program chat P2P, dibuktikan bahwa ketergantungan terhadap server pusat dapat dihilangkan dengan memanfaatkan arsitektur multithreading socket di mana setiap komputer bertindak mandiri sebagai penyedia sekaligus konsumen layanan. Konsep algoritma Distributed Hash Table (DHT) juga membuktikan bahwa pencarian berkas terdistribusi secara topologi lingkaran logika (logical ring topology) dapat berjalan secara efisien dan deterministik berdasarkan kedekatan jarak matematis karakter nilai hash. Terakhir, melalui pembedahan berkas Torrent, diketahui bahwa integritas pengunduhan berkas berukuran raksasa dapat dijamin secara aman menggunakan pemetaan metadata terkompresi berformat Bencode serta proteksi hash validation control.