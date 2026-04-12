# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 3

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Sinkronisasi pada Sistem Terdistribusi


---

### A. Sinkronisasi Waktu
Ada 2 protokol yang biasanya digunakan untuk sinkronisasi waktu: NTP (Network Time Protocol) dan PTP (Precision Time Protocol).

Berdasarkan instruksi untuk pengguna Windows, proses sinkronisasi waktu dilakukan menggunakan perangkat lunak NetTime.

1. Proses Instalasi dan Sinkronisasi:
- Mengunduh installer NetTime dari https://www.timesynctool.com/ lalu menginstalnya pada sistem operasi Windows.
- Membuka antarmuka NetTime, masuk ke Settings, lalu mengatur Time Servers untuk mengarah ke NTP server publik (seperti pool.ntp.org atau time.windows.com).

![nettime home](images/Screenshot%202026-04-11%20152103.png)
![nettime setting](images/Screenshot%202026-04-11%20152113.png)

- Mengklik tombol Update Now untuk memaksa klien melakukan sinkronisasi waktu ke NTP server saat itu juga.

![nettime update now](images/Screenshot%202026-04-11%20152142.png)

2. Penjelasan Proses Sinkronisasi:
Proses ini menggunakan protokol NTP/SNTP. Komputer kita (sebagai klien) mengirimkan paket permintaan ke NTP server. Server akan merespons dengan menyertakan timestamp waktu akurat. Perangkat lunak NetTime kemudian menghitung round-trip delay (waktu perjalanan paket bolak-balik di jaringan) dan offset (selisih waktu antara jam internal komputer kita dengan jam server). Berdasarkan perhitungan tersebut, NetTime secara halus menyesuaikan jam internal Windows agar selaras dengan waktu standar global tanpa menyebabkan lompatan waktu (time jump) yang bisa merusak log sistem.



---

###  B. Vector Clock
Vector clock digunakan untuk pengurutan event dalam suatu sistem terdistribusi. Berikut adalah contoh source code untuk vector clock (vclocks.py)

```bash
class VectorClock:
    def __init__(self, num_processes, process_id):
        self.clocks = [0] * num_processes  # Initialize all clocks to zero
        self.process_id = process_id      # The ID of the current process

    def increment(self):
        """Increments the local clock for the current process."""
        self.clocks[self.process_id] += 1

    def send_message(self):
        """Prepares the vector clock for sending with a message."""
        self.increment()  # Increment local clock before sending
        return list(self.clocks) # Return a copy of the current vector clock

    def receive_message(self, received_clocks):
        """Updates the vector clock upon receiving a message."""
        for i in range(len(self.clocks)):
            self.clocks[i] = max(self.clocks[i], received_clocks[i])
        self.increment()  # Increment local clock after receiving and merging

    def __str__(self):
        return f"P{self.process_id}: {self.clocks}"

    def happens_before(self, other_vector_clock):
        """
        Determines if this vector clock happens before another.
        A happens before B if all elements in A are less than or equal to
        the corresponding elements in B, and at least one element in A is
        strictly less than the corresponding element in B.
        """
        if self.clocks == other_vector_clock.clocks:
            return False  # Same clocks, not "happens before"

        all_le = True  # All elements are less than or equal
        any_lt = False # At least one element is strictly less than

        for i in range(len(self.clocks)):
            if self.clocks[i] > other_vector_clock.clocks[i]:
                return False # Not "happens before" if any element is greater

            if self.clocks[i] < other_vector_clock.clocks[i]:
                any_lt = True

        return all_le and any_lt

    def is_concurrent(self, other_vector_clock):
        """
        Determines if two vector clocks are concurrent.
        Two events are concurrent if neither happens before the other.
        """
        return not (self.happens_before(other_vector_clock) or
                    other_vector_clock.happens_before(self))

# Simulate a system with 3 processes
vc0 = VectorClock(num_processes=3, process_id=0)
vc1 = VectorClock(num_processes=3, process_id=1)
vc2 = VectorClock(num_processes=3, process_id=2)

print(vc0)
print(vc1)
print(vc2)

# Process 0 performs a local event
vc0.increment()
print(vc0)

# Process 0 sends a message to Process 1
message_from_p0 = vc0.send_message()
vc1.receive_message(message_from_p0)
print(vc0)
print(vc1)

# Process 2 performs a local event
vc2.increment()
print(vc2)

# Process 1 sends a message to Process 2
message_from_p1 = vc1.send_message()
vc2.receive_message(message_from_p1)
print(vc1)
print(vc2)

# Check causality
print(f"VC0 happens before VC1: {vc0.happens_before(vc1)}")
print(f"VC1 happens before VC0: {vc1.happens_before(vc0)}")
print(f"VC0 is concurrent with VC2: {vc0.is_concurrent(vc2)}")

```

#### 1. Keluaran Program dan Penjelasan Manual

Jika kode vclocks.py diatas dijalankan, program akan menghasilkan keluaran (output) teks di terminal. Berikut adalah hasil keluaran program tersebut beserta perbandingan atau pelacakan (trace) manual menggunakan algoritma Vector Clock:

![output vclocks](images/Screenshot%202026-04-11%20144803.png)

Program ini mensimulasikan pengurutan kejadian pada 3 proses (P0, P1, P2) yang dimulai dari [0, 0, 0]. Aturan utamanya: proses menambah (+1) clock miliknya sebelum sebuah kejadian/mengirim pesan, dan mengambil nilai maksimum (lalu +1) saat menerima pesan.

**Alur Kejadian:**

- **Kejadian Internal P0:** P0 menambah clock-nya menjadi [1, 0, 0].
- **P0 Mengirim ke P1:** P0 menambah clock-nya lagi menjadi [2, 0, 0] dan mengirimnya. P1 menerima pesan, menyinkronkan clock (mengambil nilai maksimum), lalu menambah clock-nya sendiri menjadi [2, 1, 0].
- **Kejadian Internal P2:** P2 menambah clock-nya menjadi [0, 0, 1].
- **P1 Mengirim ke P2:** P1 menambah clock-nya menjadi [2, 2, 0] dan mengirimnya. P2 menyinkronkan clock miliknya [0, 0, 1] dengan clock pesan [2, 2, 0], mengambil nilai maksimum tiap elemen lalu ditambah 1 pada indeksnya. Hasil akhirnya adalah [2, 2, 2].

**Analisis Kausalitas (Happens-Before & Concurrent):**

- **VC0 terjadi sebelum VC1 (True):** Karena semua elemen pada clock akhir VC0 [2, 0, 0] bernilai lebih kecil atau sama dengan elemen VC1 [2, 2, 0].
- **VC1 terjadi sebelum VC0 (False):** Karena elemen VC1 lebih besar, tidak mungkin VC1 mendahului VC0.
- **VC0 berjalan bersamaan / concurrent dengan VC2 (False):** Kejadian disebut concurrent jika keduanya independen. Di sini, nilai VC0 [2, 0, 0] lebih kecil dari VC2 [2, 2, 2], yang membuktikan bahwa VC0 terjadi mendahului VC2 (memiliki hubungan sebab-akibat), sehingga tidak concurrent.

#### 2. Modularisasi Python: Membuat Modul dan Contoh Penggunaan
Agar kode lebih terstruktur dan reusable, saya memisahkan definisi kelas VectorClock ke dalam modul tersendiri, dan memanggilnya dari file eksekusi utama.

- **File 1: vclocks.py (Sebagai Modul Utama)**
File ini hanya berisi definisi logika, tanpa adanya eksekusi simulasi di bawahnya.

```bash
class VectorClock:
    def __init__(self, num_processes, process_id):
        self.clocks = [0] * num_processes  # Initialize all clocks to zero
        self.process_id = process_id      # The ID of the current process

    def increment(self):
        """Increments the local clock for the current process."""
        self.clocks[self.process_id] += 1

    def send_message(self):
        """Prepares the vector clock for sending with a message."""
        self.increment()  # Increment local clock before sending
        return list(self.clocks) # Return a copy of the current vector clock

    def receive_message(self, received_clocks):
        """Updates the vector clock upon receiving a message."""
        for i in range(len(self.clocks)):
            self.clocks[i] = max(self.clocks[i], received_clocks[i])
        self.increment()  # Increment local clock after receiving and merging

    def __str__(self):
        return f"P{self.process_id}: {self.clocks}"

    def happens_before(self, other_vector_clock):
        """
        Determines if this vector clock happens before another.
        A happens before B if all elements in A are less than or equal to
        the corresponding elements in B, and at least one element in A is
        strictly less than the corresponding element in B.
        """
        if self.clocks == other_vector_clock.clocks:
            return False  # Same clocks, not "happens before"

        all_le = True  # All elements are less than or equal
        any_lt = False # At least one element is strictly less than

        for i in range(len(self.clocks)):
            if self.clocks[i] > other_vector_clock.clocks[i]:
                return False # Not "happens before" if any element is greater

            if self.clocks[i] < other_vector_clock.clocks[i]:
                any_lt = True

        return all_le and any_lt

    def is_concurrent(self, other_vector_clock):
        """
        Determines if two vector clocks are concurrent.
        Two events are concurrent if neither happens before the other.
        """
        return not (self.happens_before(other_vector_clock) or
                    other_vector_clock.happens_before(self))
```

- **File 2: main.py (Contoh Cara Menggunakan Modul)**
File ini akan mengimpor kelas VectorClock dari modul di atas untuk menjalankan simulasi atau skenario baru.

```bash
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
```
Jika kode main.py diatas dijalankan, program akan menghasilkan keluaran (output) teks di terminal. Berikut adalah hasil keluaran program tersebut :

![output main](images/Screenshot%202026-04-11%20174730.png)

Dengan memisahkan VectorClock ke dalam modul, saya bisa mengimpor dan menggunakannya dengan mudah jika sewaktu-waktu membutuhkan algoritma ini untuk proyek atau platform terdistribusi lainnya.

---

###  C. Problem Tanpa Sinkronisasi

Pada sistem terdistribusi, ketiadaan sinkronisasi bisa menghasilkan 2 masalah besar yaitu data race / race conditions dan deadlock. Pada program yang menggunakan model asynchronous maupun thread, pola pikir sekuensial tidak bisa digunakan karena penyelesaian satu task dengan task lainnya biasanya tidak bisa diprediksi. Berikut adalah contoh program multithreaded di Python (multithreaded-example.py).

```bash
import threading
import time

def task(name, delay):
    print(f"Task {name} starting...")
    time.sleep(delay)  # Simulates an I/O-bound operation
    print(f"Task {name} finished after {delay}s.")

# 1. Create thread objects
t1 = threading.Thread(target=task, args=("A", 5))
t2 = threading.Thread(target=task, args=("B", 5))
t3 = threading.Thread(target=task, args=("C", 5))
t4 = threading.Thread(target=task, args=("D", 5))
t5 = threading.Thread(target=task, args=("E", 5))

# 2. Start the threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

# 3. Wait for threads to finish before continuing
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

print("All tasks completed.")
```
Jika kode multithreaded-example.py diatas dijalankan, program akan menghasilkan keluaran yang berbeda setiap kali dijalankan. Berikut  hasil keluaran berbeda dari program tersebut :

![example](images/Screenshot%202026-04-11%20175435.png)

Saat skrip ini dieksekusi berulang kali, urutan "Task X finished" seringkali berubah. Hal ini terjadi karena sistem operasi mengatur penjadwalan thread (CPU Scheduling) secara dinamis. Operasi time.sleep(5) mensimulasikan tugas I/O-bound, yang membuat CPU berpindah mengeksekusi thread lain. Urutan penyelesaian sangat bergantung pada seberapa cepat sistem operasi mengalokasikan kembali waktu prosesor (context switching) ketika thread terbangun.

#### 1. Data Race / Race Conditions

- Berikut adalah contoh data race / race conditions di Python (race-conditions-01.py).

```bash
import time
from threading import Thread

balance = 100

def withdraw(amount):
    global balance
    if balance >= amount:
        time.sleep(0.01)
        balance -= amount
        print(f"Mengambil sejumlah Rp {amount}. Saldo: Rp {balance}")

t1 = Thread(target=withdraw, args=(80,))
t2 = Thread(target=withdraw, args=(80,))

t1.start(); t2.start()
t1.join(); t2.join()
```
Outputnya ketika dijalankan:

![data race 01](images/Screenshot%202026-04-12%20105629.png)

Keluaran aplikasi seringkali menghasilkan saldo akhir yang tidak terduga atau salah. Hal ini terjadi karena variabel global balance = 100 diakses dan dimodifikasi oleh t1 dan t2 di saat bersamaan. Ketika t1 sedang di-jeda (time.sleep(0.01)), t2 mengeksekusi pengecekan if balance >= amount: di mana saldonya masih bernilai 100. Akibatnya, keduanya berhasil masuk ke blok pengurangan dan saldo berkurang dua kali menjadi minus, atau tertimpa nilainya secara tidak sinkron.

Jika divisualisasikan akan seperti ini:

![visual data race](images/)

- Berikut contoh program supaya race conditions tersebut tidak terjadi (race-conditions-02.py):

```bash
import time
from threading import Thread
import threading

counter_lock = threading.Lock()
balance = 100

def withdraw(amount):
    global balance
    with counter_lock:
        if balance >= amount:
            time.sleep(0.01)
            balance -= amount
            print(f"Mengambil sejumlah Rp {amount}. Saldo: Rp {balance}")

t1 = Thread(target=withdraw, args=(80,))
t2 = Thread(target=withdraw, args=(80,))

t1.start(); t2.start()
t1.join(); t2.join()
```

Outputnya ketika dijalankan:

![data race 02](images/Screenshot%202026-04-12%20105647.png)

Race conditions tidak terjadi pada skrip ini karena program mengimplementasikan variabel pengunci counter_lock = threading.Lock(). Menggunakan blok with counter_lock:, bagian tersebut menjadi sebuah critical section. Artinya, ketika t1 memasuki blok ini, t2 tidak akan bisa mengeksekusi blok kode yang sama sebelum t1 menyelesaikannya.

#### 2. Deadlock

- Berikut adalah contoh kondisi deadlock di Python (deadlock-01.py).

```bash
import threading
import time

# Create two locks
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_task1():
    with lock_a:
        print("Thread 1: Locked A, waiting for B...")
        time.sleep(1) # Increase chance of deadlock
        with lock_b:
            print("Thread 1: Locked both")

def thread_task2():
    with lock_b:
        print("Thread 2: Locked B, waiting for A...")
        time.sleep(1) # Increase chance of deadlock
        with lock_a:
            print("Thread 2: Locked both")

# Start threads
t1 = threading.Thread(target=thread_task1)
t2 = threading.Thread(target=thread_task2)
t1.start()
t2.start()
t1.join()
t2.join()
```

Outputnya ketika dijalankan:

![deadlock 01](images/Screenshot%202026-04-12%20105749.png)

Program mengalami deadlock dan tertahan selamanya (hang). Prosesnya: Thread 1 sukses mengunci lock_a, sementara di waktu yang hampir bersamaan Thread 2 mengunci lock_b. Setelah sleep 1 detik, Thread 1 mencoba mengunci lock_b (yang sedang ditahan Thread 2), dan Thread 2 mencoba mengunci lock_a (yang sedang ditahan Thread 1). Karena tidak ada yang mau melepas kuncinya (circular wait), keduanya membeku.

Jika divisualisasikan akan seperti ini:

![visual deadlock](images/)

- Berikut contoh program supaya deadlock tersebut tidak terjadi (deadlock-02.py):

```bash
import threading
import time

# Create two shared locks
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread1_task():
    if lock_a.acquire(timeout=5):
        try:
            print("Thread 1: Acquired Lock A")
            time.sleep(1)  # Simulate some work
            print("Thread 1: Waiting for Lock B...")
        finally:
            lock_a.release()
        if lock_b.acquire(timeout=5):
            try:
                print("Thread 1: Acquired Lock B")
            finally:
                lock_b.release()

def thread2_task():
    if lock_b.acquire(timeout=5):
        try:
            print("Thread 2: Acquired Lock B")
            time.sleep(1)  # Simulate some work
            print("Thread 2: Waiting for Lock A...")
        finally:
            lock_b.release()
        if lock_a.acquire(timeout=5):
            try:
                print("Thread 2: Acquired Lock A")
            finally:
                lock_a.release()

t1 = threading.Thread(target=thread1_task)
t2 = threading.Thread(target=thread2_task)

t1.start()
t2.start()
t1.join()
t2.join()
print("Execution Finished")
```

Outputnya ketika dijalankan:

![deadlock 02](images/Screenshot%202026-04-12%20105808.png)


Program berjalan hingga mencetak "Execution Finished" dan deadlock tidak terjadi. Ini dikarenakan algoritma menghindari saling tunggu tanpa batas (infinite wait) dengan menggunakan batasan waktu timeout=5 pada fungsi acquire(). Jika kunci gagal didapatkan dalam waktu 5 detik, operasi diabaikan dan blok finally memaksa release() pada kunci yang sebelumnya sudah dipegang. Ini memutus rantai circular wait.

### D. Algoritma Raft

- Algoritma Raft adalah protokol yang banyak digunakan dalam sistem terdistribusi untuk mengelola replikasi log state machine dan mencapai konsensus siapa yang akan menjadi koordinator (LEADER). Berikut adalah simulasi algoritma Raft menggunakan Python yang diambil dari https://www.c-sharpcorner.com/article/simulate-distributed-consensus-with-the-raft-protocol-simplified-using-python/ (raft.py).

```bash
import random
import time
from enum import Enum
from typing import List, Dict, Optional

class State(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class RaftNode:
    def __init__(self, node_id: int, all_nodes: List[int]):
        self.id = node_id
        self.nodes = all_nodes
        self.state = State.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.log: List[str] = []
        self.commit_index = 0
        self.last_heartbeat = time.time()
        self.election_timeout = self._random_timeout()

    def _random_timeout(self) -> float:
        return time.time() + random.uniform(1.0, 2.0)

    def on_heartbeat(self, term: int):
        if term >= self.current_term:
            self.current_term = term
            self.state = State.FOLLOWER
            self.voted_for = None
            self.last_heartbeat = time.time()
            self.election_timeout = self._random_timeout()

    def start_election(self):
        self.current_term += 1
        self.state = State.CANDIDATE
        self.voted_for = self.id
        votes = 1  # vote for self

        # Simulate requesting votes from others
        for node_id in self.nodes:
            if node_id == self.id:
                continue
            # In real Raft, we'd send RequestVote RPC
            # Here, we simulate: grant vote if term is higher and log is not behind
            votes += 1  # Simplified: assume all grant vote

        if votes > len(self.nodes) // 2:
            self.state = State.LEADER
            print(f"Node {self.id} elected leader in term {self.current_term}")

    def append_entry(self, entry: str):
        if self.state == State.LEADER:
            self.log.append(entry)
            print(f"Leader {self.id} appended: {entry}")
            # In real system, replicate to followers
            self.commit_index = len(self.log) - 1

    def tick(self):
        now = time.time()
        if self.state == State.LEADER:
            # Send heartbeat (simplified)
            pass
        elif now > self.election_timeout:
            self.start_election()
        elif self.state == State.FOLLOWER and now - self.last_heartbeat > 2.0:
            # Missed heartbeats → start election
            self.election_timeout = self._random_timeout()
            self.start_election()


def simulate_raft():
    node_ids = [1, 2, 3]
    nodes = [RaftNode(i, node_ids) for i in node_ids]

    # Simulate time steps
    for step in range(20):
        time.sleep(0.5)
        print(f"\n--- Step {step + 1} ---")

        # Randomly trigger heartbeat from current leader (if any)
        leaders = [n for n in nodes if n.state == State.LEADER]
        if leaders:
            leader = random.choice(leaders)
            for node in nodes:
                if node.id != leader.id:
                    node.on_heartbeat(leader.current_term)
            # Leader appends a command every few steps
            if step % 5 == 0:
                leader.append_entry(f"command-{step}")

        # Each node processes its state
        for node in nodes:
            node.tick()

        # Print status
        for node in nodes:
            print(f"Node {node.id}: {node.state.name} | Term {node.current_term} | Log len {len(node.log)}")


if __name__ == "__main__":
    print(" Simulating Raft Consensus for Drone Swarm Coordination\n")
    simulate_raft()
```
Outputnya ketika dijalankan:

![raft1](images/Screenshot%202026-04-12%20105849.png)
![raft2](images/Screenshot%202026-04-12%20105903.png)
![raft3](images/Screenshot%202026-04-12%20110345.png)

Dari simulasi program, terlihat bahwa seluruh node (Drone 1, 2, dan 3) memulai generasinya (term 0) sebagai FOLLOWER. Karena belum ada detak jantung (heartbeat) dari leader, mereka mencapai batas waktu (election timeout). Node pertama yang timeout-nya habis akan mengubah status menjadi CANDIDATE, menaikkan term (menjadi 1), dan memberikan suaranya untuk dirinya sendiri. Program mensimulasikan persetujuan otomatis dari separuh anggota lainnya (votes > len(self.nodes) // 2). Kandidat yang meraup mayoritas suara resmi dideklarasikan sebagai LEADER. Setelah terpilih, LEADER mengirim sinyal heartbeat secara berkala agar pengikutnya tidak memulai pemilihan baru. Sesekali, LEADER juga mereplikasi/meneruskan (append) perintah ke dalam log.

Jika divisualisasikan akan seperti ini:

![visual raft](images/)

#### Modularisasi Python: Membuat Modul dan Contoh Penggunaan

Skrip dipisahkan menjadi dua berkas agar sistem objek bisa digunakan sebagai modul.

- **File 1: raft-module.py (Sebagai Modul Utama)**

```bash
import random
import time
from enum import Enum
from typing import List, Optional

class State(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class RaftNode:
    def __init__(self, node_id: int, all_nodes: List[int]):
        self.id = node_id
        self.nodes = all_nodes
        self.state = State.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.log: List[str] = []
        self.commit_index = 0
        self.last_heartbeat = time.time()
        self.election_timeout = self._random_timeout()

    def _random_timeout(self) -> float:
        return time.time() + random.uniform(1.0, 2.0)

    def on_heartbeat(self, term: int):
        if term >= self.current_term:
            self.current_term = term
            self.state = State.FOLLOWER
            self.voted_for = None
            self.last_heartbeat = time.time()
            self.election_timeout = self._random_timeout()

    def start_election(self):
        self.current_term += 1
        self.state = State.CANDIDATE
        self.voted_for = self.id
        votes = 1  # vote for self

        # Simulate requesting votes from others
        for node_id in self.nodes:
            if node_id == self.id:
                continue
            votes += 1  # Simplified: assume all grant vote

        if votes > len(self.nodes) // 2:
            self.state = State.LEADER
            print(f"Node {self.id} elected leader in term {self.current_term}")

    def append_entry(self, entry: str):
        if self.state == State.LEADER:
            self.log.append(entry)
            print(f"Leader {self.id} appended: {entry}")
            self.commit_index = len(self.log) - 1

    def tick(self):
        now = time.time()
        if self.state == State.LEADER:
            pass
        elif now > self.election_timeout:
            self.start_election()
        elif self.state == State.FOLLOWER and now - self.last_heartbeat > 2.0:
            self.election_timeout = self._random_timeout()
            self.start_election()
```

- **File 2: raft-main.py (Contoh Simulasi menggunakan Modul)**

```bash
import time
import random
from raft_module import State, RaftNode

def simulate_raft():
    node_ids = [1, 2, 3]
    nodes = [RaftNode(i, node_ids) for i in node_ids]

    # Simulate time steps
    for step in range(20):
        time.sleep(0.5)
        print(f"\n--- Step {step + 1} ---")

        # Randomly trigger heartbeat from current leader (if any)
        leaders = [n for n in nodes if n.state == State.LEADER]
        if leaders:
            leader = random.choice(leaders)
            for node in nodes:
                if node.id != leader.id:
                    node.on_heartbeat(leader.current_term)
            # Leader appends a command every few steps
            if step % 5 == 0:
                leader.append_entry(f"command-{step}")

        # Each node processes its state
        for node in nodes:
            node.tick()

        # Print status
        for node in nodes:
            print(f"Node {node.id}: {node.state.name} | Term {node.current_term} | Log len {len(node.log)}")

if __name__ == "__main__":
    print(" Simulating Raft Consensus for Drone Swarm Coordination\n")
    simulate_raft()
```

Jika kode raft-main.py diatas dijalankan, program akan menghasilkan output berikut:

![raft-1](images/Screenshot%202026-04-12%20113420.png)
![raft-2](images/Screenshot%202026-04-12%20113436.png)
![raft-3](images/Screenshot%202026-04-12%20113450.png)

---

### Kesimpulan

Praktikum minggu ketiga ini membuktikan bahwa mekanisme sinkronisasi mutlak diperlukan dalam sistem terdistribusi untuk menjaga konsistensi data dan urutan eksekusi antar node. Melalui implementasi sinkronisasi waktu berbasis NTP dan pemetaan kausalitas menggunakan Vector Clock, sistem dapat beroperasi dengan acuan riwayat kejadian yang seragam. Ketiadaan sinkronisasi terbukti memicu kegagalan sistem seperti race condition dan deadlock pada proses multithreading, yang efektif diatasi melalui manajemen critical section dengan locking dan timeout. Pada tingkat yang lebih kompleks, penerapan algoritma konsensus seperti Raft menjadi solusi fundamental untuk menjaga sinkronisasi state dan melakukan pemilihan leader secara dinamis, sehingga klaster terdistribusi dapat terus beroperasi secara terkoordinasi dan toleran terhadap kegagalan.