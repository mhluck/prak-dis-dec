# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 2

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Komunikasi Antar Proses pada Sistem Terdistribusi


Pada praktikum minggu kedua ini saya mempelajari komunikasi antar proses. Proses merupakan hasil dari eksekusi program / aplikasi yang bersifat executable. Proses dikelola oleh sistem operasi dan terdiri atas executable code, data, resources, serta informasi tentang state (stack dan heap). Setiap aplikasi yang dijalankan akan menjadi proses.


---

## I. Proses pada Satu Node

### 1. Menampilkan Proses pada Windows (Task Manager)

Langkah pertama adalah menampilkan proses yang sedang berjalan pada sistem operasi Windows menggunakan Task Manager.

Langkah-langkah:

1. Tekan tombol **Ctrl + Shift + Esc** untuk membuka Task Manager.
2. Pilih tab **Processes**.
3. Akan ditampilkan daftar proses yang sedang berjalan, baik aplikasi maupun background process.
![Tab Processes](images/Screenshot%202026-03-31%20091023.png)

Contoh tampilan:
- Apps (aplikasi yang sedang dibuka)
- Background processes
- Windows processes

Informasi yang ditampilkan meliputi:
- CPU usage
- Memory usage
- Disk usage
- Network usage

---

### 2. Menjalankan Aplikasi dan Melihat Prosesnya

Pada percobaan ini digunakan aplikasi **WhatsApp**.

Langkah-langkah:

1. Buka aplikasi **WhatsApp** melalui Start Menu.
2. Setelah terbuka, buka kembali **Task Manager**.
3. Pada tab **Processes**, cari aplikasi **WhatsApp** pada bagian **Apps**.
![Tab Processes(WhatsApp)](images/Screenshot%202026-03-31%20091557.png)

Hasil:
- Muncul proses dengan nama **WhatsApp**
- Menandakan aplikasi sedang berjalan di sistem

---

### 3. Mematikan dan Me-restart Proses

#### Mematikan Proses (End Task)

Langkah-langkah:

1. Buka **Task Manager**.
2. Pilih aplikasi **WhatsApp** pada tab **Processes**.
3. Klik tombol **End Task**.
![End Task(WhatsApp)](images/Screenshot%202026-03-31%20091727.png)

Hasil:
- Aplikasi langsung tertutup tanpa menggunakan tombol exit
- Proses **WhatsApp** hilang dari daftar

---

#### Me-restart Proses

Langkah-langkah:

1. Setelah proses dihentikan, buka kembali aplikasi **WhatsApp** melalui Start Menu.
![Buka WhatsApp)](images/Screenshot%202026-03-31%20091923.png)

Hasil:
- Proses baru muncul kembali di Task Manager
![Task Manager)](images/Screenshot%202026-03-31%20091953.png)

---

### 4. Penjelasan Kegiatan

Pada praktikum ini dilakukan pengamatan terhadap proses yang berjalan pada sistem operasi Windows menggunakan Task Manager. Proses-proses yang aktif ditampilkan pada tab **Processes**, yang memberikan informasi penggunaan sumber daya sistem.

Selanjutnya dilakukan percobaan dengan menjalankan aplikasi Notepad untuk melihat bagaimana sistem membuat proses baru. Setelah itu, proses dihentikan menggunakan fitur **End Task** tanpa menggunakan tombol keluar dari aplikasi.

Dari kegiatan ini dapat disimpulkan bahwa setiap aplikasi yang dijalankan akan direpresentasikan sebagai proses oleh sistem operasi. Proses tersebut dapat dikontrol oleh pengguna, seperti dihentikan maupun dijalankan kembali melalui Task Manager.

---

## II. Komunikasi Antar Proses pada Sistem Terdistribusi

### 1. Membuat Workspace

Langkah pertama adalah membuat workspace untuk proyek GraphQL.

Langkah-langkah:

Membuat folder workspace:
```bash
mkdir workspace-01
cd workspace-01
```

Hasil:

- Folder workspace-01 berhasil dibuat dan digunakan sebagai direktori kerja.

### 2. Menentukan Versi Python

Pada tahap ini dilakukan pengecekan dan penentuan versi Python yang digunakan.

Langkah-langkah:

Melihat daftar Python yang tersedia:
```bash
uv python list
```
![python list](images/Screenshot%202026-04-02%20024411.png)
Menentukan versi Python:
```bash
uv python pin cpython-3.14.3
```
![pin python](images/Screenshot%202026-04-02%20024531.png)

Hasil:

- Terbentuk file .python-version
- Workspace menggunakan Python versi 3.14.3

### 3. Membuat dan Mengaktifkan Environment

Langkah berikutnya adalah membuat virtual environment.

Langkah-langkah:

Membuat virtual environment:
```bash
uv venv
```
Mengaktifkan environment (Windows):
```bash
.venv\Scripts\activate
```
![Membuat & mengaktifkan virtual environment](images/Screenshot%202026-04-02%20024937.png)

Mengecek Python yang digunakan:
```bash
where python
```

Hasil:

- Python yang aktif berasal dari folder .venv

### 4. Instalasi Package Strawberry GraphQL

Pada tahap ini dilakukan instalasi library yang dibutuhkan.

Langkah-langkah:

Install package:
```bash
uv pip install "strawberry-graphql[cli]"
```
![Install package](images/Screenshot%202026-04-02%20025020.png)

Cek package:
```bash
uv pip list
```
![Cek package](images/Screenshot%202026-04-02%20025036.png)

Hasil:

- Package strawberry-graphql berhasil terinstall

### 5. Membuat File Schema GraphQL

Langkah berikutnya adalah membuat schema GraphQL.

Langkah-langkah:

Membuat file:
```bash
notepad schema.py
```
Isi file schema.py:
```
import typing
import strawberry



def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]



@strawberry.type
class Book:
    title: str
    author: str



@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)



schema = strawberry.Schema(query=Query)
```

Hasil:

- Schema GraphQL berhasil dibuat dengan query books

### 6. Inisialisasi Project dan Instalasi Dependency

Pada tahap ini dilakukan inisialisasi project menggunakan uv untuk mengatasi error saat menambahkan package, karena sebelumnya belum terdapat file konfigurasi project (pyproject.toml).

Langkah-langkah:

Inisialisasi project:
```bash
uv init
```

Hasil:

- Project berhasil diinisialisasi
- File pyproject.toml otomatis dibuat

Install dependency:
```bash
uv add fastapi uvicorn strawberry-graphql
```
![Install dependency](images/Screenshot%202026-04-02%20031834.png)

Hasil:

- Dependency berhasil ditambahkan ke project
- Package yang terinstall antara lain: fastapi, uvicorn, strawberry-graphql, pydantic, annotated-types

Catatan:

Terdapat warning terkait hardlink, namun tidak mempengaruhi proses instalasi (hanya berdampak pada performa).

Membuat file utama aplikasi:
```bash
notepad main.py
```

Isi file main.py:
```
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from schema import schema

app = FastAPI()

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
```


### 7. Menjalankan GraphQL Server

Langkah selanjutnya adalah menjalankan server GraphQL.

Langkah-langkah:

Menjalankan server:
```bash
 uv run uvicorn main:app
```

Hasil:

- Server berjalan pada alamat: http://127.0.0.1:8000/graphql

### 8. Menguji Query GraphQL

Pada tahap ini dilakukan pengujian query melalui browser.

Langkah-langkah:

Buka browser dan akses: http://127.0.0.1:8000/graphql
![Buka browser](images/Screenshot%202026-04-02%20032643.png)

Masukkan query:
```
{
  books {
    title
    author
  }
}
```
Klik tombol Run
![run](images/Screenshot%202026-04-02%20034208.png)

Hasil:

- Data buku tampil dalam format JSON di bagian kanan

### 9. Penjelasan Kegiatan

Pada praktikum ini dilakukan pembuatan server GraphQL menggunakan Python dengan library Strawberry. Proses dimulai dari pembuatan workspace, penentuan versi Python, pembuatan virtual environment, hingga instalasi package yang diperlukan.

Selanjutnya dibuat file schema.py yang berisi definisi tipe data dan query GraphQL. Server kemudian dijalankan dan diuji melalui browser dengan melakukan query untuk mengambil data buku.

Dari kegiatan ini dapat disimpulkan bahwa GraphQL dapat digunakan sebagai media komunikasi antar proses pada sistem terdistribusi, dimana client dapat meminta data dari server secara fleksibel sesuai kebutuhan.

### 10. (Tugas Tambahan) Membuat Client Sederhana

Pada tahap ini dibuat client sederhana menggunakan Python untuk mengakses server GraphQL.

Langkah-langkah:

Membuat file client.py
```bash
notepad client.py
```
Isi file:
```
import requests

url = "http://127.0.0.1:8000/graphql"

query = """
{
  books {
    title
    author
  }
}
"""

response = requests.post(url, json={"query": query})

print(response.json())
```
Install library:
```bash
uv pip install requests
```
![Install library](images/Screenshot%202026-04-02%20034418.png)

Jalankan program:
```bash
python client.py
```
![Jalankan program](images/Screenshot%202026-04-02%20034427.png)

Hasil:

- Data dari server GraphQL berhasil ditampilkan di terminal