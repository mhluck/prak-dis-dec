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