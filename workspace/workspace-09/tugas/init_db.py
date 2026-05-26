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