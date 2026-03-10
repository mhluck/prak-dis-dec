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
git reset --hard HEAD^
```

---

## 10. Membuat Repository di Organisasi

Repository juga dapat dibuat dalam sebuah **Organization**.

Langkah-langkahnya sama seperti membuat repository biasa, hanya saja pada bagian **Owner** dipilih organisasi yang diinginkan. Setelah repository dibuat, pengelolaannya tetap menggunakan perintah Git yang sama.

---