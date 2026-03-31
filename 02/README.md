# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 2

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Komunikasi Antar Proses pada Sistem Terdistribusi


Pada praktikum minggu kedua ini saya mempelajari komunikasi antar proses. Proses merupakan hasil dari eksekusi program / aplikasi yang bersifat executable. Proses dikelola oleh sistem operasi dan terdiri atas executable code, data, resources, serta informasi tentang state (stack dan heap). Setiap aplikasi yang dijalankan akan menjadi proses.


---

## 1. Menampilkan Proses pada Windows (Task Manager)

Langkah pertama adalah menampilkan proses yang sedang berjalan pada sistem operasi Windows menggunakan Task Manager.

Langkah-langkah:

1. Tekan tombol **Ctrl + Shift + Esc** untuk membuka Task Manager.
2. Pilih tab **Processes**.
3. Akan ditampilkan daftar proses yang sedang berjalan, baik aplikasi maupun background process.
![Tab Processes](images/Screenshot%202026-03-31%20091023.png)

Contoh tampilan:
- Apps (aplikasi yang sedang dibuka)
- Background processes
- Windows processes

Informasi yang ditampilkan meliputi:
- CPU usage
- Memory usage
- Disk usage
- Network usage

---

## 2. Menjalankan Aplikasi dan Melihat Prosesnya

Pada percobaan ini digunakan aplikasi **WhatsApp**.

Langkah-langkah:

1. Buka aplikasi **WhatsApp** melalui Start Menu.
2. Setelah terbuka, buka kembali **Task Manager**.
3. Pada tab **Processes**, cari aplikasi **WhatsApp** pada bagian **Apps**.
![Tab Processes(WhatsApp)](images/Screenshot%202026-03-31%20091557.png)

Hasil:
- Muncul proses dengan nama **WhatsApp**
- Menandakan aplikasi sedang berjalan di sistem

---

## 3. Mematikan dan Me-restart Proses

### Mematikan Proses (End Task)

Langkah-langkah:

1. Buka **Task Manager**.
2. Pilih aplikasi **WhatsApp** pada tab **Processes**.
3. Klik tombol **End Task**.
![End Task(WhatsApp)](images/Screenshot%202026-03-31%20091727.png)

Hasil:
- Aplikasi langsung tertutup tanpa menggunakan tombol exit
- Proses **WhatsApp** hilang dari daftar

---

### Me-restart Proses

Langkah-langkah:

1. Setelah proses dihentikan, buka kembali aplikasi **WhatsApp** melalui Start Menu.
![Buka WhatsApp)](images/Screenshot%202026-03-31%20091923.png)

Hasil:
- Proses baru muncul kembali di Task Manager
![Task Manager)](images/Screenshot%202026-03-31%20091953.png)

---

## 4. Penjelasan Kegiatan

Pada praktikum ini dilakukan pengamatan terhadap proses yang berjalan pada sistem operasi Windows menggunakan Task Manager. Proses-proses yang aktif ditampilkan pada tab **Processes**, yang memberikan informasi penggunaan sumber daya sistem.

Selanjutnya dilakukan percobaan dengan menjalankan aplikasi Notepad untuk melihat bagaimana sistem membuat proses baru. Setelah itu, proses dihentikan menggunakan fitur **End Task** tanpa menggunakan tombol keluar dari aplikasi.

Dari kegiatan ini dapat disimpulkan bahwa setiap aplikasi yang dijalankan akan direpresentasikan sebagai proses oleh sistem operasi. Proses tersebut dapat dikontrol oleh pengguna, seperti dihentikan maupun dijalankan kembali melalui Task Manager.

---
