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