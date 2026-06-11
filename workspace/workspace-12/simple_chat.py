import socket
import threading
import sys
import time

def terima_pesan(port_saya):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Mengikat socket ke semua interface pada port lokal yang ditentukan
        server_socket.bind(('0.0.0.0', port_saya))
        server_socket.listen(1)
        print(f"\n[SERVER] Mendengarkan di port {port_saya}...", file=sys.stderr)
        
        koneksi, alamat_peer = server_socket.accept()
        print(f"\n[SERVER] Terhubung dengan peer: {alamat_peer}", file=sys.stderr)
        
        while True:
            data = koneksi.recv(1024)
            if not data:
                print("\n[SERVER] Peer memutuskan koneksi.", file=sys.stderr)
                break
            print(f"\n[Peer]: {data.decode('utf-8')}")
    except Exception as e:
        print(f"[SERVER] Error: {e}", file=sys.stderr)
    finally:
        server_socket.close()

def kirim_pesan(ip_tujuan, port_tujuan):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[CLIENT] Mencoba terhubung ke {ip_tujuan}:{port_tujuan}...", file=sys.stderr)
    try:
        client_socket.connect((ip_tujuan, port_tujuan))
        print("[CLIENT] Sukses terhubung!", file=sys.stderr)
        print("Silakan ketik pesan dan tekan Enter (Ketik 'keluar' untuk berhenti):")
        while True:
            pesan = input()
            if pesan.lower() == 'keluar':
                break
            client_socket.sendall(pesan.encode('utf-8'))
    except Exception as e:
        print(f"[CLIENT] Gagal terhubung atau mengirim pesan: {e}", file=sys.stderr)
    finally:
        client_socket.close()

if __name__ == "__main__":
    print("=== Praktikum Modul 12 Sub 01 ===")
    port_lokal = int(input("Masukkan PORT LOKAL untuk server Anda (contoh: 5001): "))
    
    # Menjalankan fungsi terima_pesan di dalam thread terpisah
    thread_server = threading.Thread(target=terima_pesan, args=(port_lokal,))
    thread_server.daemon = True
    thread_server.start()
    
    time.sleep(1)
    print("\n--- Konfigurasi Hubungan ke Peer Lain ---")
    ip_target = input("Masukkan IP TARGET (Peer tujuan, contoh: localhost): ")
    port_target = int(input("Masukkan PORT TARGET (Port server peer tujuan): "))
    
    # Jalankan pengiriman pesan
    kirim_pesan(ip_target, port_target)
    print("\nProgram Selesai.")