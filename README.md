# Termz 🚀

<pre>
████████╗███████╗██████╗ ███╗   ███╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║█████╗  
   ██║   ██╔══╝  ██╔═══╝ ██║╚██╔╝██║██╔══╝  
   ██║   ███████╗██║     ██║ ╚═╝ ██║███████╗
   ╚═╝   ╚══════╝╚═╝     ╚═╝     ╚═╝╚══════╝
</pre>

**Terminal di dalam terminal? Kenapa enggak?**
Shell sandbox buatan anak bangsa! 🇮🇩

## ❓ Apaan nih?

**Termz** itu *bukan* shell beneran kayak `bash` atau `zsh`.

Ini adalah **lingkungan terminal yang disandbox**. Artinya, semua perintah file (kayak `ls`, `cd`, `mkdir`, `rm`) yang lo jalanin cuma berlaku di dalem folder `Termz/home`. Gak bakal bisa ngerusak atau ngacak-ngacak file sistem asli lo.

Aman banget buat ngoprek, ngetes, atau belajar command line tanpa rasa was-was!

## ✨ Fitur Keren

* **100% Sandbox**: Semua aksi file sistem *terkurung* di dalem direktori `Termz/home`.
* **Manajer Paket Bawaan**: Punya `pkg install`, `pkg remove`, `pkg update` sendiri.
* **Repo Paket Fleksibel**: Lo bisa ganti-ganti sumber paket (`trm change repo`), dari repo GitHub default sampe mirror lo sendiri.
* **Perintah Bawaan**: Udah ada perintah dasar kayak `ls`, `cd`, `mkdir`, `rm`, `rm -rf`, `clear`, `exit`.
* **Editor Teks**: Ada perintah `tre` buat ngedit file (numpang pake `nano` dari sistem host lo).
* **Git Siap Pakai**: Bisa `git clone` langsung di dalem sandbox.

## 💻 Cara Maketin (Jalanin)

Proyek ini butuh Python 3.

### 1. Clone Reponya

```bash
git clone https://github.com/muhammadzili/Termz.git
cd Termz
```

### 2. Install Modul yang Dibutuhin
```
pip install -r requirements.txt
```

### 4. Jalanin!
```
python termz.py
```

### Daftar Perintah
#### Nih list perintahnya, lo juga bisa masuk ke termz nya terus ketik help.
```
Available commands:
  --- Navigasi & File ---
  ls [path]              - Tampilkan isi direktori
  cd <dir>               - Pindah direktori (mendukung '..' untuk naik)
  mkdir <dir>            - Buat direktori baru
  rm <file>              - Hapus file
  rm -rf <dir/file>      - Hapus folder atau file secara paksa
  tre <filename>         - Edit file (menggunakan 'nano' host)
  git clone <url> [dir]  - Clone repository dari GitHub
  
  --- Manajemen Paket ---
  trm change repo        - Ganti URL repository paket (interaktif)
  pkg install <name>     - Install package from repo
  pkg remove <name>      - Remove installed package
  pkg update             - Update package list from repo
  pkg upgrade            - Upgrade all installed packages
  trm installed          - Show installed packages
  trm search <keyword>   - Search package in repo
  trm run <command>      - Run a command from installed package
  
  --- Lainnya ---
  clear                  - Clear screen
  exit                   - Exit Termz
  
  Anda juga bisa menjalankan paket terinstall langsung
  dengan mengetik: <package_name> [subcommand]
```

## Lo pengen bikin Package sendiri?
1. Lo bisa bikin paket sendiri buat Termz. Gampang banget!
2. Lo cuma perlu bikin file .json yang isinya info paket dan perintah Python yang mau dijalanin.
3. Liat aja contohnya di repo paket (misalnya art.json atau cowsay-lite.json).
4. Upload file .json lo ke server/repo lo sendiri.
5. Update file index.json di server lo biar ngasih tau Termz soal paket baru lo.
6. Jalanin trm change repo di Termz buat nunjuk ke repo lo, pkg update, dan pkg install nama_paket_lo!
