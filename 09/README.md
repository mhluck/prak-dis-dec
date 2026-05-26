# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 9

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---
## Arsitektur Microservices untuk Sistem Terdistribusi: GraphQL dan gRPC

Microservices adalah salah satu arsitektur yang banyak digunakan pada sistem terdistribusi. Dengan menggunakan arsitektur ini, software terdiri atas frontend yang berisi UI/UX dan merupakan titik interaksi antara pengguna dengan aplikasi. Sisi frontend tersebut kemudian meminta layanan / services dari backend yang berupa service. Untuk saat ini, kebanyakan service tersebut bisa dibuat menggunakan REST API, GraphQL, dan gRPC. Praktikum pada pertemuan ini akan berfokus menggunakan GraphQL dan gRPC dengan memanfaatkan pustaka strawberry dan grpc di Python, serta dijalankan di lingkungan Windows menggunakan perangkat lunak uv untuk manajemen dependensi.

---

### 1. GraphQL

GraphQL adalah spesifikasi query language untuk API di sisi server dan melibatkan mekanisme query khusus dari client ke server. Berbeda dengan REST API yang memiliki endpoint berbeda untuk setiap resource, GraphQL umumnya hanya menggunakan satu endpoint di mana client dapat meminta struktur data yang spesifik secara fleksibel.

#### a. Setup Python dan Virtual Environment

Sama seperti modul sebelumnya, pastikan uv sudah terinstal di Windows.

- Lakukan pinning versi Python ke 3.14.4:

```Bash
uv python pin cpython-3.14.4
```

- Buat virtual environment baru pada direktori proyek dengan perintah:

```Bash
uv venv
```

- Aktivasi environment (Khusus Windows):

```Bash
.\.venv\Scripts\Activate.ps1
```
![venv](images/Screenshot%202026-05-26%20205717.png)

- Buat file requirements.txt

```bash
notepad requirements.txt
```

- isi dengan 
```bash
strawberry-graphql
sqlmodel
gql
aiohttp
grpcio
grpcio-tools
```

- Lakukan instalasi dependensi (pastikan terdapat file requirements.txt yang berisi strawberry-graphql, sqlmodel, dan gql):

```Bash
uv pip install -r requirements.txt
```
![venv](images/Screenshot%202026-05-26%20210208.png)

#### b. Membuat GraphQL Server

- Buat direktori graphql/server. Di dalamnya, pastikan sudah ada file database departemen-sdm.db dari Modul 8.

- Buat file graphql_server.py dan salin kode berikut:

```bash
import typing
import strawberry
from sqlmodel import Field, Session, SQLModel, create_engine, select

@strawberry.type
class Sdm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    npp: str
    nama: str

engine = create_engine("sqlite:///departemen-sdm.db")

def get_sdms():
    # SQLModel select statement
    with Session(engine) as session:
        statement = select(Sdm)
        results = session.exec(statement).all()
        return results

@strawberry.type
class Query:
    sdms: typing.List[Sdm] = strawberry.field(resolver=get_sdms)

schema = strawberry.Schema(query=Query)
```

#### c. Menjalankan Server dan Menguji di Explorer

- Instal Ekstensi CLI Strawberry

```bash
uv pip install "strawberry-graphql[cli]"
```
![venv](images/Screenshot%202026-05-26%20211258.png)

- Di terminal, jalankan server Strawberry dengan perintah:

```Bash
strawberry dev graphql_server
```

- Buka browser dan akses http://localhost:8000/graphql. Pada sisi kiri GraphQL Explorer, masukkan query berikut lalu tekan tombol Play:

```bash
{
  sdms {
    id
    npp
    nama
  }
}
```

![venv](images/Screenshot%202026-05-26%20214233.png)

#### d. Membuat GraphQL Client

- Buat direktori graphql/client dan buat file graphql_client.py.

- Masukkan kode berikut untuk mengakses data GraphQL via script:

```bash
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

async def main():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport)
    
    # Provide a GraphQL query
    query = gql(
        """
        query getSdms {
            sdms {
                id
                npp
                nama
            }
        }
        """
    )
    
    # Execute the query
    async with client as session:
        result = await session.execute(query)
        print(result)

asyncio.run(main())
```

- Jalankan script tersebut melalui terminal baru, biarkan terminal server masih menyala:

```bash
python graphql_client.py
```

![venv](images/Screenshot%202026-05-26%20214835.png)
---

### 2. gRPC (gRPC Remote Procedure Calls)
gRPC adalah mekanisme untuk komunikasi antara dua node menggunakan Protocol Buffers sebagai serialisasi data.

#### a. Definisi Service dan Kompilasi Protobuf

- Buat direktori grpc/server dan buat file bernama service.proto:

```bash
syntax = "proto3";
package mydb;

message SdmRequest {
    int32 id = 1;
}

message SdmResponse {
    int32 id = 1;
    string npp = 2;
    string nama = 3;
}

service SdmService {
    rpc GetSdm (SdmRequest) returns (SdmResponse);
}
```

- Lakukan kompilasi file proto tersebut menggunakan perintah berikut di terminal PowerShell:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```
Perintah ini akan menghasilkan file service_pb2.py dan service_pb2_grpc.py.

![venv](images/Screenshot%202026-05-26%20215157.png)
![venv](images/Screenshot%202026-05-26%20215233.png)

#### b. Membuat dan Menjalankan gRPC Server

- Di direktori yang sama, buat file server.py:

```bash
import grpc
from concurrent import futures
from sqlmodel import Field, Session, SQLModel, create_engine, select
import service_pb2
import service_pb2_grpc

class Sdm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    npp: str
    nama: str

engine = create_engine("sqlite:///departemen-sdm.db")

class SdmServiceServicer(service_pb2_grpc.SdmServiceServicer):
    def GetSdm(self, request, context):
        with Session(engine) as session:
            statement = select(Sdm).where(Sdm.id == request.id)
            results = session.exec(statement)
            sdm_result = results.first()
            
            if sdm_result is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return service_pb2.SdmResponse()
                
            return service_pb2.SdmResponse(
                id=sdm_result.id,
                npp=sdm_result.npp,
                nama=sdm_result.nama,
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SdmServiceServicer_to_server(SdmServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started. Listening on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

- Jalankan server:

```bash
python server.py
```

![venv](images/Screenshot%202026-05-26%20215932.png)

#### c. Membuat dan Menjalankan gRPC Client

- Di direktori grpc/client, copy kedua file hasil kompilasi proto sebelumnya. Lalu buat file client.py:

```bash
import grpc
import service_pb2
import service_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.SdmServiceStub(channel)
        
        # Test 1: ID yang ada
        request = service_pb2.SdmRequest(id=1)
        try:
            response = stub.GetSdm(request)
            print(f"Sdm Name: {response.nama}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} {e.details()}")
            
        # Test 2: ID yang tidak ada
        request_not_found = service_pb2.SdmRequest(id=10000)
        try:
            response = stub.GetSdm(request_not_found)
            print(f"Sdm Name: {response.nama}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run_client()
```

- Jalankan client di tab terminal baru, biarkan terminal server tetap menyala:

```bash
python client.py
```

![venv](images/Screenshot%202026-05-26%20215954.png)

---

### 3. Tugas Praktikum

Berdasarkan instruksi tugas, kita diminta untuk menggunakan tabel SQLite dengan tipe data INT, CHAR, VARCHAR, BOOLEAN, dan FLOAT, kemudian membuat endpoint GraphQL untuk mengambil semua data, dan endpoint gRPC untuk mengambil satu data.

#### A. Persiapan Database (tugas.db)
- Saya membuat tabel Pegawai. File init_db.py dengan isi:

```bash
from sqlmodel import Field, Session, SQLModel, create_engine

class Pegawai(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) # INT
    kode: str = Field(max_length=5)                        # CHAR
    nama: str                                              # VARCHAR
    aktif: bool                                            # BOOLEAN
    gaji: float                                            # FLOAT

engine = create_engine("sqlite:///tugas.db")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Pegawai(kode="A001", nama="Andi", aktif=True, gaji=5000.50))
    session.add(Pegawai(kode="B002", nama="Budi", aktif=False, gaji=4500.75))
    session.add(Pegawai(kode="C003", nama="Citra", aktif=True, gaji=6000.00))
    session.commit()
```

- Jalankan di terminal: 
```bash
python init_db.py
```

#### B. Tugas 1: GraphQL (Mengambil Semua Data)

- File Server: graphql_tugas_server.py

```bash
import typing
import strawberry
from sqlmodel import Field, Session, SQLModel, create_engine, select

@strawberry.type
class Pegawai(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    aktif: bool
    gaji: float

engine = create_engine("sqlite:///tugas.db")

def get_semua_pegawai():
    with Session(engine) as session:
        return session.exec(select(Pegawai)).all()

@strawberry.type
class Query:
    semua_pegawai: typing.List[Pegawai] = strawberry.field(resolver=get_semua_pegawai)

schema = strawberry.Schema(query=Query)
```

- Jalankan servernya:
```bash
strawberry dev graphql_tugas_server
```

![venv](images/Screenshot%202026-05-26%20221934.png)

- File Client: graphql_tugas_client.py

```bash
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

async def main():
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport)
    query = gql("""
        query {
            semuaPegawai {
                id
                kode
                nama
                aktif
                gaji
            }
        }
    """)
    async with client as session:
        result = await session.execute(query)
        print("Data Pegawai:", result)

asyncio.run(main())
```

- Jalankan clientnya:

```bash
strawberry dev graphql_tugas_client
```

![venv](images/Screenshot%202026-05-26%20222559.png)

#### C. Tugas 2: gRPC (Mengambil Satu Data)
- File Proto: tugas.proto

```bash
syntax = "proto3";
package tugasdb;

message PegawaiRequest {
    int32 id = 1;
}

message PegawaiResponse {
    int32 id = 1;
    string kode = 2;
    string nama = 3;
    bool aktif = 4;
    float gaji = 5;
}

service PegawaiService {
    rpc GetPegawai (PegawaiRequest) returns (PegawaiResponse);
}
```
- Kompilasi:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tugas.proto
```

- File Server: grpc_tugas_server.py

```bash
import grpc
from concurrent import futures
from sqlmodel import Field, Session, SQLModel, create_engine, select
import tugas_pb2
import tugas_pb2_grpc

class Pegawai(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    aktif: bool
    gaji: float

engine = create_engine("sqlite:///tugas.db")

class PegawaiServiceServicer(tugas_pb2_grpc.PegawaiServiceServicer):
    def GetPegawai(self, request, context):
        with Session(engine) as session:
            hasil = session.exec(select(Pegawai).where(Pegawai.id == request.id)).first()
            if hasil is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Pegawai tidak ditemukan")
                return tugas_pb2.PegawaiResponse()
            
            return tugas_pb2.PegawaiResponse(
                id=hasil.id, kode=hasil.kode, nama=hasil.nama, aktif=hasil.aktif, gaji=hasil.gaji
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tugas_pb2_grpc.add_PegawaiServiceServicer_to_server(PegawaiServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server Tugas gRPC berjalan...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

- Jalankan servernya:

```bash
python grpc_tugas_server.py
```

![venv](images/Screenshot%202026-05-26%20222951.png)

- File Client: grpc_tugas_client.py

```bash
import grpc
import tugas_pb2
import tugas_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = tugas_pb2_grpc.PegawaiServiceStub(channel)
        
        # Request Pegawai ID = 1
        request = tugas_pb2.PegawaiRequest(id=1)
        try:
            response = stub.GetPegawai(request)
            print(f"Data Ditemukan: {response.nama} (Kode: {response.kode}, Gaji: {response.gaji})")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run_client()
```

- Jalankan clientnya:

```bash
strawberry dev grppc_tugas_client
```

![venv](images/Screenshot%202026-05-26%20223213.png)

---

### Kesimpulan

Praktikum Modul 9 berhasil mengimplementasikan metode komunikasi microservices non-REST, yaitu menggunakan GraphQL dan gRPC. GraphQL dengan library Strawberry menawarkan keunggulan berupa fleksibilitas query di mana client dapat mendikte secara persis field apa saja yang ingin diambil dari database tanpa risiko over-fetching. Sementara itu, gRPC menggunakan Protocol Buffers (.proto) menawarkan performa tinggi dengan serialisasi tipe data biner yang kuat (strongly-typed), sangat cocok untuk komunikasi intenal antar-service backend. Keduanya dapat diimplementasikan di lingkungan Python dengan manajemen dependensi menggunakan uv serta diintegrasikan secara apik dengan SQLModel dan database SQLite.