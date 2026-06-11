import hashlib

def hitung_hash_8bit(teks):
    # Menggunakan SHA-1 dan mengambil 2 karakter terakhir untuk representasi 8-bit (0-255)
    sha1 = hashlib.sha1(teks.encode('utf-8')).hexdigest()
    return int(sha1[-2:], 16)

class NodeP2P:
    def __init__(self, nama_node):
        self.nama = nama_node
        self.id = hitung_hash_8bit(nama_node)
        self.penyimpanan_lokal = {}
        print(f"Node '{self.nama}' berhasil dibuat dengan ID: {self.id}")

class LingkaranDHT:
    def __init__(self):
        self.daftar_node = []

    def tambah_node(self, node):
        self.daftar_node.append(node)
        self.daftar_node.sort(key=lambda x: x.id) # Diurutkan membentuk struktur Ring

    def cari_node_terdekat(self, key_data):
        # Algoritma pencarian node terdekat (Successor) dalam konsep Ring Topology
        for node in self.daftar_node:
            if node.id >= key_data:
                return node
        return self.daftar_node[0] # Memutar kembali ke awal ring jika key melewati ID node terbesar

    def simpan_data(self, nama_file, isi_konten):
        key_data = hitung_hash_8bit(nama_file)
        node_target = self.cari_node_terdekat(key_data)
        node_target.penyimpanan_lokal[key_data] = (nama_file, isi_konten)
        print(f"[SIMPAN] File '{nama_file}' (Key ID: {key_data}) disimpan di Node '{node_target.nama}' (Node ID: {node_target.id})")

    def cari_data(self, nama_file):
        key_data = hitung_hash_8bit(nama_file)
        node_target = self.cari_node_terdekat(key_data)
        print(f"\n[PENCARIAN] Mencari file '{nama_file}' dengan Key ID: {key_data}...")
        print(f"[ROUTING] Request diarahkan ke Node terdekat: '{node_target.nama}' (Node ID: {node_target.id})")
        
        if key_data in node_target.penyimpanan_lokal:
            nama, konten = node_target.penyimpanan_lokal[key_data]
            print(f" [SUKSES] Data ditemukan! Isi konten: '{konten}'")
        else:
            print(" [GAGAL] Data tidak ditemukan di jaringan.")

if __name__ == "__main__":
    print("=== Praktikum Modul 12 Teknologi P2P Simulasi DHT ===")
    dht = LingkaranDHT()
    
    node_a = NodeP2P("Node A")
    node_b = NodeP2P("Node B")
    node_c = NodeP2P("Node C")
    
    dht.tambah_node(node_a)
    dht.tambah_node(node_b)
    dht.tambah_node(node_c)
    
    print("\nUrutan Node dalam Lingkaran DHT (Ring):")
    for n in dht.daftar_node:
        print(f" -> Node ID: {n.id} ({n.nama})")
        
    dht.simpan_data("tugas_jaringan.pdf", "Konten: Laporan Praktikum Modul 1")
    dht.simpan_data("foto_makrab.jpg", "Konten: Data biner gambar makrab angkatan")
    dht.simpan_data("source_code.py", "Konten: print('Hello P2P')")
    
    dht.cari_data("tugas_jaringan.pdf")
    dht.cari_data("source_code.py")
    dht.cari_data("praktikum.py")