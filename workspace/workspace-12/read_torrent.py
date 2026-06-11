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