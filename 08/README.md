# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 8

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---
## Arsitektur Microservices untuk Sistem Terdistribusi
---

Microservices adalah salah satu arsitektur yang banyak digunakan pada sistem terdistribusi. Dengan menggunakan arsitektur ini, software terdiri atas frontend yang berisi UI/UX dan merupakan titik interaksi antara pengguna dengan aplikasi. Sisi frontend tersebut kemudian meminta layanan / services dari backend yang berupa service. Untuk saat ini, kebanyakan service tersebut bisa dibuat menggunakan REST API, GraphQL, dan gRPC. Praktikum pada mata kuliah ini akan menggunakan REST API dengan pustaka FastAPI dan SQLModel untuk ORM dari Python dan dijalankan di lingkungan Windows menggunakan perangkat lunak uv untuk manajemen dependensi dan versi Python.

---

### 1. Microservices

**a. Setup Python dan Virtual Environment**
Materi ini mensyaratkan penggunaan uv. Pastikan uv sudah terinstal di Windows kamu.
- Cek versi Python yang tersedia dengan mengetikkan perintah:

```bash
uv python list
```
- Buat virtual environment baru dengan perintah:
```bash
uv venv
```
Perintah ini akan membuat environment di dalam folder .venv.
- Aktivasi environment (Khusus Windows):
Di dokumen asli yang menggunakan Linux, aktivasinya menggunakan source .venv/bin/activate. Untuk Windows, jalankan perintah ini di terminal VS Code:

```bash
.\.venv\Scripts\Activate.ps1
```

![venv](images/Screenshot%202026-05-13%20084402.png)

**b. Instalasi FastAPI dan SQLModel**

Setelah virtual environment aktif, jalankan perintah berikut untuk menginstal pustaka yang dibutuhkan:

```bash
uv pip install fastapi[standard] sqlmodel
```

Perintah ini akan menginstal FastAPI dan SQLModel beserta dependensinya.

![venv](images/Screenshot%202026-05-13%20084503.png)

**c. Persiapan Database SQLite**

Dokumen mengharuskan adanya SQLite. Jika di Windows belum ada SQLite, maka perlu mengunduh Precompiled Binaries for Windows dari https://sqlite.org/download.html. Ekstrak dan pastikan file sqlite3.exe bisa diakses dari terminal.  Setelah itu, buat database dan masukkan data:

- Di terminal VS Code, jalankan perintah untuk membuat database:

```bash
.\sqlite3 departemen-sdm.db
```
Ini akan membuat file departemen-sdm.db.

- Salin dan tempel (paste) perintah SQL berikut satu per satu ke dalam prompt SQLite (sqlite>) untuk membuat tabel dan mengisi data karyawan : 

```bash
CREATE TABLE sdm (id INTEGER PRIMARY KEY, npp CHAR(6), nama VARCHAR(50));
INSERT INTO sdm (npp, nama) VALUES('112233', 'Karyawan 1');
INSERT INTO sdm (npp, nama) VALUES('223344', 'Karyawan 2');
INSERT INTO sdm (npp, nama) VALUES('334455', 'Karyawan 3');
```

- Verifikasi data dengan perintah:

```bash
SELECT * FROM sdm;
```
- Keluar dari SQLite dengan mengetik .quit atau menekan Ctrl+C.

![venv](images/Screenshot%202026-05-13%20085417.png)

**d. Membuat Source Code Service**

- Di panel Explorer VS Code, buat file baru bernama service.py.
- Salin kode Python berikut ke dalam service.py dan simpan :

```bash
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Sdm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    npp: str
    nama: str

engine = create_engine("sqlite:///departemen-sdm.db")

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.get("/sdm/", response_model=List[Sdm])
def read_sdm(session: Session = Depends(get_session)):
    # SQLModel select statement
    statement = select(Sdm)
    results = session.exec(statement).all()
    return results
```

![venv](images/Screenshot%202026-05-13%20085846.png)

**e. Menjalankan Service**

- Kembali ke terminal VS Code, jalankan server Uvicorn dengan perintah:

```bash
uvicorn service:app --reload
```
Perintah ini akan menjalankan service dan otomatis memuat ulang (reload) jika ada perubahan file.

- Melihat pesan bahwa Uvicorn berjalan di alamat http://127.0.0.1:8000 (atau http://localhost:8000/).

![venv](images/Screenshot%202026-05-13%20090136.png)

**f. Memeriksa Hasil**

Menguji API yang baru dibuat melalui:
- Browser: Buka http://localhost:8000/sdm/.
- Terminal Baru: Buka tab terminal baru di VS Code dan jalankan perintah curl http://localhost:8000/sdm/. 

![venv](images/Screenshot%202026-05-13%20090253.png)
![venv](images/Screenshot%202026-05-13%20090724.png)
---

### 2. Tugas Praktikum
Berdasarkan instruksi tugas, kita diminta untuk membuat tabel baru, mengisinya dengan minimal 3 data, membuat API untuk menampilkannya, dan menjelaskan source code beserta keluarannya.

**A. Source Code (main.py)**
Buat sebuah file bernama main.py di dalam direktori workspace-08 dan masukkan kode berikut. Pada kasus ini, kita membuat tabel Mahasiswa.

```bash
from typing import List, Optional
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 1. Definisi Model (Tabel Mahasiswa)
class Mahasiswa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nim: str = Field(index=True)
    nama: str
    jurusan: str

# 2. Konfigurasi Database SQLite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

# 3. Event Startup untuk inisialisasi tabel
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 4. API Endpoint untuk Menambah Data (POST)
@app.post("/mahasiswa/", response_model=Mahasiswa)
def create_mahasiswa(mhs: Mahasiswa):
    with Session(engine) as session:
        session.add(mhs)
        session.commit()
        session.refresh(mhs)
        return mhs

# 5. API Endpoint untuk Menampilkan Data (GET)
@app.get("/mahasiswa/", response_model=List[Mahasiswa])
def read_mahasiswa():
    with Session(engine) as session:
        mahasiswas = session.exec(select(Mahasiswa)).all()
        return mahasiswas
```

![venv](images/Screenshot%202026-05-13%20090848.png)

**B. Menjalankan Aplikasi**
Jalankan server FastAPI menggunakan perintah berikut di PowerShell:

```bash
uv run fastapi dev main.py
```

Server akan berjalan di alamat http://localhost:8000.

![venv](images/Screenshot%202026-05-13%20091139.png)

**C. Pengujian dan Pengisian Data**
FastAPI secara otomatis menyediakan antarmuka dokumentasi interaktif (Swagger UI). Kita akan menggunakannya untuk mengisi 3 baris data.
- Buka browser dan akses: http://localhost:8000/docs.

![venv](images/Screenshot%202026-05-13%20091224.png)
- Buka menu POST /mahasiswa/, klik Try it out, dan masukkan data JSON berikut satu per satu, lalu klik Execute:

Data 1:

```bash
{
  "nim": "235410085",
  "nama": "Mohammad Luqman Hakim",
  "jurusan": "Informatika"
}
```

![venv](images/Screenshot%202026-05-13%20091544.png)
![venv](images/Screenshot%202026-05-13%20091624.png)

Data 2:

```bash
{
  "nim": "235410086",
  "nama": "Budi Santoso",
  "jurusan": "Sistem Informasi"
}
```

![venv](images/Screenshot%202026-05-13%20091731.png)
![venv](images/Screenshot%202026-05-13%20091742.png)

Data 3:

```bash
{
  "nim": "235410087",
  "nama": "Andi Setiawan",
  "jurusan": "Teknik Komputer"
}
```

![venv](images/Screenshot%202026-05-13%20091827.png)
![venv](images/Screenshot%202026-05-13%20091834.png)


**D. Verifikasi Keluaran API (GET)**
Untuk memastikan API berfungsi dan menampilkan isi tabel, kita dapat mengakses endpoint GET dengan salah satu cara berikut:
- Melalui Browser: Buka alamat http://localhost:8000/mahasiswa/.

![venv](images/Screenshot%202026-05-13%20092106.png)

- Melalui PowerShell (Curl): Buka tab PowerShell baru dan ketikkan:

```bash
curl http://localhost:8000/mahasiswa/
```

![venv](images/Screenshot%202026-05-13%20092141.png)

---

### Kesimpulan
Praktikum ini berhasil mengimplementasikan dasar-dasar arsitektur microservices menggunakan Python. Dengan menggunakan FastAPI dan SQLModel, pembuatan REST API (Create dan Read) yang terintegrasi dengan basis data SQLite dapat dilakukan dengan sangat ringkas dan cepat. Pemisahan endpoint berbasis URL (seperti /mahasiswa/) menunjukkan bagaimana sebuah layanan mandiri (service) dapat menyediakan data terstruktur berupa JSON yang nantinya siap dikonsumsi oleh aplikasi frontend jenis apapun. Manajemen environment menggunakan uv di Windows juga berjalan lancar dalam mengisolasi dependensi aplikasi.