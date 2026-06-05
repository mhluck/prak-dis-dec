# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 11

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Sistem Terdesentralisasi, Blockchain, dan Web 3.0

Praktikum ini membahas pengenalan sistem terdesentralisasi, teknologi blockchain, serta Web 3.0. Sistem terdesentralisasi merupakan arsitektur yang mendelegasikan kontrol ke sekumpulan *node* yang saling terhubung, bukan ke otoritas pusat tunggal. Blockchain adalah salah satu teknologi utama yang digunakan untuk mengimplementasikan sistem terdesentralisasi tersebut. Sementara itu, Web 3.0 adalah visi masa depan internet yang berfokus pada sistem terdesentralisasi, transparansi, dan kontrol penuh pengguna atas data pribadi mereka dengan memanfaatkan teknologi seperti blockchain.

---

### 1. Cara Kerja Blockchain dan Pembuatan Blockchain Sederhana

Suatu blockchain terdiri atas sekumpulan blok data yang saling terhubung dan dikunci menggunakan algoritma hash. 

#### A. Pengujian Hashing (Tugas 1)
Langkah pertama adalah memahami bagaimana *hash* bekerja dengan menggunakan pustaka `hashlib` bawaan Python.

- Membuka terminal PowerShell dan menjalankan Python, lalu memasukkan *script* berikut:

```python
import hashlib
text = "UTDI"
hash_object = hashlib.sha256(text.encode('utf-8'))
hex_dig = hash_object.hexdigest()
print(f"SHA-256 Hash: {hex_dig}")

text2 = "Fakultas Teknologi Informasi"
hash_object2 = hashlib.sha256(text2.encode('utf-8'))
hex_dig2 = hash_object2.hexdigest()
print(f"SHA-256 Hash: {hex_dig2}")
```
![venv](images/Screenshot%202026-06-05%20190752.png)

**Simpulan Proses Hash:**
Berdasarkan script di atas, proses hash mengubah teks input (apapun panjangnya) menjadi sebuah string acak (heksadesimal) dengan panjang yang tetap. Karena menggunakan algoritma SHA-256, outputnya akan selalu berjumlah 64 karakter. Perubahan kecil apapun pada teks input akan menghasilkan nilai hash yang sama sekali berbeda secara deterministik. Selain itu, hash bersifat satu arah (one-way), yang artinya tidak bisa menebak atau mengembalikan teks asli hanya dari melihat nilai hash-nya.

#### B. Implementasi Blockchain Sederhana (Tugas 2)
Mensimulasikan pembuatan blockchain sendiri (UtdiBlockchain) menggunakan Python.

- File CoreBlockchain.py

```python
import hashlib
import time

class CoreBlockchain:
    def __init__(self, idx, data, previous_hash):
        self.idx = idx
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.count_hash()

    def count_hash(self):
        block_contents = (
            str(self.idx) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_contents.encode()).hexdigest()
```

![venv](images/Screenshot%202026-06-05%20191313.png)

- File UtdiBlockchain.py

```python
import CoreBlockchain

class UtdiBlockchain:
    def __init__(self):
        self.chain = []
        self.init_genesis_block()

    def init_genesis_block(self):
        first_block = CoreBlockchain.CoreBlockchain(0, "Blok Genesis / Awal", "0")
        self.chain.append(first_block)

    def add_block(self, new_data):
        last_block = self.chain[-1]
        new_block = CoreBlockchain.CoreBlockchain(
            idx=len(self.chain),
            data=new_data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
```

![venv](images/Screenshot%202026-06-05%20191326.png)

- File blockchain_demo_01.py

```python
import UtdiBlockchain

informatika_blockchain = UtdiBlockchain.UtdiBlockchain()
informatika_blockchain.add_block("Bambang transfer ke Zaky sebesar 5 koin")
informatika_blockchain.add_block("Zaky transfer ke Didik sebesar 10 koin")

for block in informatika_blockchain.chain:
    print(f"Blok #{block.idx}")
    print(f"Data: {block.data}")
    print(f"Hash Sebelumnya: {block.previous_hash}")
    print(f"Hash Sekarang : {block.hash}\n" + "-"*40)
```

![venv](images/Screenshot%202026-06-05%20191337.png)

- Menjalankan simulasi di terminal: python blockchain_demo_01.

![venv](images/Screenshot%202026-06-05%20191734.png)

**Penjelasan Source Code:**
- CoreBlockchain.py: Berfungsi sebagai cetak biru (struktur dasar) dari sebuah blok. Setiap blok menyimpan informasi indeks, waktu (timestamp), data transaksi, angka acak pengaman (nonce), dan yang paling penting: Hash dari blok sebelumnya (previous_hash). Fungsi count_hash akan merangkai semua atribut tersebut menjadi teks panjang lalu menghitung nilai SHA-256 nya.
- UtdiBlockchain.py: Bertugas mengelola rantai (list) dari blok-blok tersebut. Terdapat init_genesis_block yang selalu dieksekusi pertama kali untuk membuat "Blok 0" (Genesis) yang nilai previous_hash-nya adalah "0". Fungsi add_block akan mengambil data transaksi baru, membuat blok baru, dan menguncinya dengan mengambil atribut hash dari blok paling akhir di rantai.
- blockchain_demo_01.py: File eksekusi utama yang membuat instansiasi blockchain dan mengisinya dengan 2 transaksi. Hasil output cetakannya membuktikan bahwa rantai bekerja dengan baik, terlihat dari nilai "Hash Sebelumnya" pada Blok #1 dan Blok #2 yang 100% identik dengan nilai "Hash Sekarang" milik blok persis di atasnya.

### 2. Pengenalan Blockchain Ethereum dan Konfigurasi Wallet
Pada praktikum ini, digunakan jaringan Ethereum (Public Blockchain). Untuk bisa berinteraksi di dalamnya, diperlukan sebuah akun (Wallet), di mana ekstensi peramban standar yang paling populer digunakan adalah MetaMask.

#### A. Instalasi MetaMask
- Mengunjungi situs resmi metamask.io dan memilih unduhan untuk Browser Extension
- Klik tombol Add to Chrome dan setujui permissions yang diminta. 

![venv](images/Screenshot%202026-06-05%20192017.png)

#### B. Setup Wallet dan Recovery Phrase
- Setelah terinstal, buka ekstensi MetaMask.
- Pilih Buat dompet baru dan buat password lokal (minimal 8 karakter).

![venv](images/Screenshot%202026-06-05%20192044.png)
![venv](images/Screenshot%202026-06-05%20192214.png)

- MetaMask akan memberikan Secret Recovery Phrase. Frasa ini sangat krusial dan wajib disimpan di tempat yang aman karena berfungsi sebagai kunci master wallet.

- Setelah divalidasi, wallet berhasil dibuat dan siap digunakan untuk transaksi.

![venv](images/Screenshot%202026-06-05%20192244.png)

#### C. Konfigurasi Testnet (Sepolia) dan Request Token (Faucet)
Untuk keperluan simulasi tanpa uang nyata, maka menggunakan jaringan Testnet bernama Sepolia. 
- Pada menu MetaMask, klik opsi Networks, aktifkan tampilkan jaringan pengujian, lalu pilih Sepolia.

![venv](images/Screenshot%202026-06-05%20193817.png)
![venv](images/Screenshot%202026-06-05%20193828.png)
![venv](images/Screenshot%202026-06-05%20193842.png)

- Buka situs https://faucets.chain.link/ untuk meminta dana simulasi (ETH Testnet). 

![venv](images/Screenshot%202026-06-05%20194015.png)

- Pilih Ethereum Sepolia, hubungkan (Connect) dengan akun MetaMask, dan konfirmasi Signature Request di aplikasi MetaMask. 

![venv](images/Screenshot%202026-06-05%20194217.png)
![venv](images/Screenshot%202026-06-05%20194247.png)

- Klik Get Tokens. Setelah sukses, ETH simulasi akan otomatis masuk ke dalam saldo wallet Sepolia kita. 

![venv](images/Screenshot%202026-06-05%20194451.png)
![venv](images/Screenshot%202026-06-05%20194507.png)
![venv](images/Screenshot%202026-06-05%20194608.png)

---

### Tugas 3
#### 1. Menjelaskan beberapa istilah berikut ini: 
- **DApps (Decentralized Applications)**: Aplikasi digital yang berjalan dan beroperasi pada jaringan peer-to-peer (blockchain) yang terdesentralisasi, bukan di bawah kendali server otoritas pusat tunggal.
- **NFT (Non-Fungible Token)**: Aset digital kriptografi pada blockchain yang memiliki kode identifikasi unik. Karena sifatnya non-fungible, NFT tidak dapat ditukar atau diganti dengan nilai yang persis sama (berbeda dengan Bitcoin/uang kertas), sehingga sering digunakan untuk membuktikan kepemilikan aset digital seperti karya seni.
- **DEX (Decentralized Exchange)**: Platform bursa pertukaran kripto peer-to-peer (P2P) yang memungkinkan pengguna untuk bertransaksi kripto secara langsung satu sama lain melalui Smart Contracts tanpa memerlukan lembaga perantara/broker pihak ketiga.
- **Tokenization**: Proses mengubah hak atau nilai dari sebuah aset (baik aset fisik nyata maupun digital) menjadi sebuah token digital yang diterbitkan dan dicatat di atas blockchain.
- **Stablecoins**: Kelas aset mata uang kripto yang nilainya dipatok (di-pegged) terhadap aset cadangan yang stabil di dunia nyata (seperti Dolar AS, Euro, atau Emas) dengan tujuan meminimalisir volatilitas harga kripto yang ekstrem.

#### 2. Jika anda akan membangun DApps di Ethereum, peranti pengembangan apa yang akan anda gunakan? Jelaskan mengapa anda memilih peranti pengembangan tersebut selengkap mungkin. 
- Saya akan menggunakan kombinasi Remix IDE (untuk tahapan awal/prototyping) dan Hardhat (untuk tahapan development dan deployment skala penuh).
- Alasan Memilih Remix IDE: Sangat cocok untuk menulis, menguji, dan melakukan deploy Smart Contract (menggunakan bahasa Solidity) dengan cepat karena berbasis web browser. Tidak diperlukan instalasi environment di komputer lokal, dan sudah terintegrasi langsung dengan MetaMask untuk deploy ke testnet seperti Sepolia.
- Alasan Memilih Hardhat: Jika proyek DApps sudah semakin kompleks (melibatkan antarmuka frontend React/Next.js dan pengujian otomatis tingkat lanjut), Hardhat adalah framework berbasis Node.js yang paling tangguh. Hardhat menyediakan jaringan Ethereum lokal khusus (Hardhat Network) yang bisa dijalankan secara offline di mesin kita untuk eksperimen tak terbatas. Hardhat juga memiliki fitur canggih seperti console.log() di dalam kode Solidity yang sangat mempermudah proses debugging.

---

### Kesimpulan
Praktikum Modul 11 ini memberikan pemahaman mendasar yang sangat kuat terkait ekosistem Web 3.0. Melalui implementasi menggunakan Python, konsep algoritma Hash (SHA-256) terbukti menjadi fondasi utama yang mengunci dan menghubungkan setiap blok data agar tidak dapat dimanipulasi secara retrospektif (kekebalan data). Di samping itu, pengenalan jaringan publik Ethereum via ekstensi wallet MetaMask serta pemanfaatan jaringan testnet Sepolia memberikan gambaran praktis tentang bagaimana pengembang (developer) membangun, menguji, dan berinteraksi dengan aset digital (kripto dan Smart Contracts) tanpa risiko kehilangan dana nyata.