from vclocks import VectorClock

def main():
    print("--- Memulai Simulasi Sistem Terdistribusi ---")
    
    # Inisialisasi 2 proses saja untuk contoh skenario baru
    total_nodes = 2
    node_A = VectorClock(num_processes=total_nodes, process_id=0)
    node_B = VectorClock(num_processes=total_nodes, process_id=1)

    print("Kondisi Awal:")
    print(node_A)
    print(node_B)

    # Node A memproses sebuah tugas (Internal Event)
    print("\nNode A melakukan proses internal...")
    node_A.increment()
    print(node_A)

    # Node A mengirim data ke Node B
    print("\nNode A mengirim pesan ke Node B...")
    msg_data_clock = node_A.send_message()
    node_B.receive_message(msg_data_clock)
    print("Setelah pertukaran pesan:")
    print(node_A)
    print(node_B)

    # Cek relasi antar proses
    print("\nApakah proses A terjadi sebelum B? :", node_A.happens_before(node_B))

if __name__ == "__main__":
    main()