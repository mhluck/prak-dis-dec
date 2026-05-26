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