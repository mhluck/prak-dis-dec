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