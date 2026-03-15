# Laporan Praktikum Sistem Terdistribusi Dan Terdesentralisasi
## Minggu 1

Nama  : Mohammad Luqman Hakim
NIM   : 235410085
Kelas : Informatika-2  

---

## Dasar Penggunaan Git dan GitHub

Pada praktikum minggu pertama ini saya mempelajari dasar penggunaan Git dan GitHub, mulai dari membuat repository, melakukan clone repository, mengelola perubahan file, menggunakan branch, hingga melakukan kolaborasi menggunakan fork dan pull request.

---

## 1. Membuat Repository di GitHub

Langkah pertama adalah membuat repository baru di GitHub.

Langkah-langkah:

1. Login ke akun GitHub.
2. Klik tombol **+** di pojok kanan atas.
3. Pilih **New repository**.
![Create New Repository menu](images/Screenshot%202026-03-11%20031346.png)
4. Isi nama repository.
![Isian repo baru](images/Screenshot%202026-03-11%20031425.png)
5. Pilih visibilitas repository **Public** atau **Private** (disini saya pilih Private).
![Pilih visibilitas](images/Screenshot%202026-03-11%20031443.png)
6. Klik **Create Repository**.

Setelah repository dibuat, repository dapat diakses melalui URL:

```
https://github.com/mhluck/git-github.git
```

---

## 2. Clone Repository ke Komputer Lokal

Setelah repository dibuat di GitHub, langkah berikutnya adalah menyalin repository tersebut ke komputer lokal menggunakan perintah berikut:

```bash
$ git clone https://github.com/mhluck/git-github.git
Cloning into 'git-github'...
warning: You appear to have cloned an empty repository.
```
**Catatan**: muncul peringatan karena repo yang di clone masih kosong

Masuk ke direktori repository:

```bash
cd git-github
```

---

## 3. Mengubah Nama Branch Menjadi main

Beberapa repository masih menggunakan nama branch **master**, sehingga perlu diubah menjadi **main** menggunakan perintah berikut:

```bash
$ git branch -m main
```

---

## 4. Menambahkan File ke Repository

Langkah selanjutnya adalah membuat atau mengedit file pada repository.

Membuat file README.md:

```bash
vim README.md
```

Saya isi filenya dengan:

```
# My Git & GitHub
```

Melihat status repository:

```bash
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

Menambahkan file ke staging area:

```bash
$ git add -A
```

Commit perubahan:

```bash
$ git commit -m "Add README.md"
[main (root-commit) 205388a] Add README.md
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

Push perubahan ke GitHub:

```bash
$ git push origin main
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 234 bytes | 234.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/mhluck/git-github.git
 * [new branch]      main -> main
```

---

## 5. Mengubah Repository Menggunakan Branch

Untuk menjaga kestabilan branch utama, perubahan biasanya dilakukan pada branch baru.

Membuat branch baru sekaligus langsung berpindah ke branch baru:

```bash
$ git checkout -b edit-readme
Switched to a new branch 'edit-readme'
```

Mengedit isi file README.md:

```
# My new Git & GitHub repo 
```

Melihat perubahan:

```bash
$ git status
On branch edit-readme
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

Menambahkan perubahan:

```bash
$ git add -A
```

Commit perubahan:

```bash
$ git commit -m "Update README"
[edit-readme d0b34d7] Update README
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Kembali ke branch utama:

```bash
$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
```

Push branch ke GitHub:

```bash
$ git push origin edit-readme
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (3/3), 275 bytes | 275.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote: 
remote: Create a pull request for 'edit-readme' on GitHub by visiting:
remote:      https://github.com/mhluck/git-github/pull/new/edit-readme
remote:
To https://github.com/mhluck/git-github.git
 * [new branch]      edit-readme -> edit-readme
```

---

## 6. Membuat Pull Request

Setelah branch berhasil di-push ke GitHub, langkah selanjutnya adalah membuat Pull Request.

Langkah-langkah:

1. Buka repository di GitHub.
2. Klik **Compare & Pull Request**.
![Pilih Compare & Pull Request](images/Screenshot%202026-03-11%20044217.png)
3. Tambahkan deskripsi perubahan.
![Deskripsi](images/Screenshot%202026-03-11%20044320.png)
4. Klik **Create Pull Request**.
5. Jika perubahan sudah sesuai, lakukan **Merge Pull Request**.
![Pilih Merge Pull Request](images/Screenshot%202026-03-11%20044414.png)
---

## 7. Sinkronisasi Repository

Jika terdapat perubahan pada repository di GitHub, repository lokal dapat disinkronkan menggunakan perintah:

```bash
$ git pull
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (1/1), 905 bytes | 452.00 KiB/s, done.
From https://github.com/mhluck/git-github
   205388a..31129dc  main       -> origin/main
Updating 205388a..31129dc
Fast-forward
 README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

---

## 8. Membatalkan Perubahan

Jika terjadi kesalahan pada perubahan yang dilakukan di repository lokal, perubahan dapat dibatalkan menggunakan:

```bash
$ git reset --hard
HEAD is now at 31129dc Merge pull request #1 from mhluck/edit-readme
```

Perintah ini akan mengembalikan repository ke kondisi commit terakhir.

---

## 9. Membatalkan Commit Terakhir

Jika commit terakhir sudah di-push tetapi ternyata salah, maka dapat dibatalkan menggunakan perintah:

```bash
$ git revert HEAD
hint: Waiting for your editor to close the file... 
[main e5ed90a] Revert "mencoba push agar saya bisa mencoba membatalkan commit setelah ini"
 1 file changed, 1 insertion(+), 3 deletions(-)
```

Setelah itu push kembali ke repository:

```bash
$ git push
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 12 threads
Compressing objects: 100% (1/1), done.
Writing objects: 100% (3/3), 327 bytes | 327.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/mhluck/git-github.git
   e1df5b7..e5ed90a  main -> main
```

Jika commit belum di-push ke GitHub, maka dapat dibatalkan menggunakan:

```bash
$ git reset --hard HEAD^
```

---

## 10. Membuat Repository di Organisasi

Repository juga dapat dibuat dalam sebuah **Organization**.

Langkah-langkahnya sama seperti membuat repository biasa, hanya saja pada bagian **Owner** dipilih organisasi yang diinginkan. Setelah repository dibuat, pengelolaannya tetap menggunakan perintah Git yang sama.

---

## 11. Kolaborasi Menggunakan Fork

Untuk berkontribusi pada repository milik orang lain, digunakan fitur **Fork**.

Langkah-langkah:

1. Buka repository yang ingin dikontribusikan.
(disini saya menggunakan repo https://github.com/sandhikagalih/channel-youtube-programming-dan-teknologi-indonesia)
2. Klik tombol **Fork**.
![Klik fork](images/Screenshot%202026-03-16%20053300.png)
3. Sesuaikan nama repo dan deskripsinya dengan keinginan kita.
![Klik create fork](images/Screenshot%202026-03-16%20053704.png)
4. Repository akan disalin ke akun GitHub kita.

---

## 12. Clone Repository Hasil Fork

Clone repository hasil fork ke komputer lokal:

```bash
$ git clone https://github.com/mhluck/Channel-YT-Programming.git
Cloning into 'Channel-YT-Programming'...
remote: Enumerating objects: 92, done.
remote: Counting objects: 100% (92/92), done.
remote: Compressing objects: 100% (45/45), done.
remote: Total 92 (delta 27), reused 72 (delta 19), pack-reused 0 (from 0)
Receiving objects: 100% (92/92), 25.12 KiB | 2.51 MiB/s, done.
Resolving deltas: 100% (27/27), done.
```

Masuk ke direktori repository:

```bash
cd Channel-YT-Programming
```

---

## 13. Menambahkan Remote Upstream

Repository fork perlu dihubungkan dengan repository asli menggunakan remote **upstream**.

Melihat remote repository:

```bash
$ git remote -v
origin  https://github.com/mhluck/Channel-YT-Programming.git (fetch)
origin  https://github.com/mhluck/Channel-YT-Programming.git (push)
```

Menambahkan upstream:

```bash
$ git remote add upstream https://github.com/sandhikagalih/channel-youtube-programming-dan-teknologi-indonesia
```

Cek kembali remote:

```bash
$ git remote -v
origin  https://github.com/mhluck/Channel-YT-Programming.git (fetch)
origin  https://github.com/mhluck/Channel-YT-Programming.git (push)
upstream        https://github.com/sandhikagalih/channel-youtube-programming-dan-teknologi-indonesia (fetch)
upstream        https://github.com/sandhikagalih/channel-youtube-programming-dan-teknologi-indonesia (push)
```

---

## 14. Mengirim Pull Request sebagai Kontributor

Langkah-langkah kontribusi ke repository:

Sinkronisasi repository dengan upstream:

```bash
$ git fetch upstream
From https://github.com/sandhikagalih/channel-youtube-programming-dan-teknologi-indonesia
 * [new branch]      main       -> upstream/main
```

Membuat branch baru:

```bash
$ git checkout -b add-contributor
Switched to a new branch 'add-contributor'
```

Lakukan perubahan:

```bash
...
| Dea Afrizal  | Programming, Fun Coding              | [link](https://www.youtube.com/c/DeaAfrizal)          |
...
```

Menambahkan perubahan (disini saya menambahkan channel YT Dea Afrizal)

```bash
$ git add -A
```

Commit perubahan:

```bash
$ git commit -m "Add contributor & Add channel yt"
[add-contributor c76892c] Add contributor & Add channel yt
 1 file changed, 1 insertion(+)
```

Push branch ke repository fork:

```bash
$ git push origin add-contributor
```

---

## 15. Membuat Pull Request ke Repository Asli

Setelah melakukan push, langkah berikutnya adalah membuat Pull Request.

Langkah-langkah:

1. Buka repository fork di GitHub.
2. Klik **Compare & Pull Request**.
![Klik Compare & Pull Request](images/Screenshot%202026-03-16%20060335.png)
3. Tambahkan deskripsi perubahan.
![Isi deskripsi](images/Screenshot%202026-03-16%20060610.png)
4. Klik **Create Pull Request**.

Pemilik repository akan melakukan review dan melakukan merge jika perubahan disetujui.

---

## 16. Sinkronisasi Setelah Pull Request Diterima

Setelah Pull Request diterima dan di-merge, repository lokal perlu disinkronkan kembali.

Ambil perubahan dari upstream:

```bash
git fetch upstream
```

Merge perubahan:

```bash
git merge upstream/main
```

Push perubahan ke repository fork:

```bash
git push origin main
```

---

## 17. Konflik (Merge Conflict)

Konflik dapat terjadi jika beberapa kontributor mengubah bagian file yang sama.

Jika konflik terjadi, maka perlu dilakukan penyelesaian konflik secara manual dengan cara:

1. Mengedit file yang mengalami konflik.
2. Menyimpan hasil perbaikan.
3. Melakukan commit ulang.
4. Mengirim kembali Pull Request.

---

## Kesimpulan

Pada praktikum minggu pertama ini saya mempelajari dasar penggunaan Git dan GitHub, mulai dari membuat repository, melakukan clone repository, mengelola perubahan menggunakan commit dan branch, hingga melakukan kolaborasi menggunakan fork dan pull request. Dengan Git, proses pengembangan proyek dapat dilakukan secara lebih terstruktur dan memudahkan kolaborasi antar pengembang.