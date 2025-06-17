# 🎨 Drawing App Enno

**Drawing App Enno** adalah aplikasi menggambar 2D interaktif berbasis web yang memungkinkan pengguna untuk membuat, memanipulasi, dan mentransformasi berbagai objek geometris langsung di browser.

Aplikasi ini dibangun menggunakan **HTML**, **CSS**, dan **Python**, dengan bantuan pustaka **Brython** untuk menjalankan kode Python di sisi klien (browser).


---

## 🧩 Fitur Utama

### ✏️ Mode Menggambar
- **Bentuk Geometris:** Titik, garis, persegi, lingkaran, dan elips.
- **Kustomisasi:** 
  - Warna objek melalui pemilih warna.
  - Ketebalan garis atau ukuran titik melalui slider.
- **Pratinjau Real-time:** Pratinjau bentuk mengikuti gerakan mouse sebelum finalisasi gambar.

### 🔄 Mode Transformasi
- **Seleksi Objek:** Klik objek di kanvas untuk memilihnya.
- **Transformasi:**
  - **Translasi** (geser objek).
  - **Skala** (perbesar/perkecil).
  - **Rotasi** (0°–360°).
- **Transformasi Akurat:** Semua perubahan berbasis pusat objek untuk hasil natural.

### 🧠 UI/UX Interaktif
- Dua mode utama: **Gambar** dan **Transformasi**.
- Panel kontrol hanya muncul saat diperlukan.
- Panel **Info Objek**: Menampilkan tipe, posisi, ukuran, dan transformasi.
- **Tampilan Koordinat Mouse** secara real-time.
- Desain modern dengan tata letak dua kolom.

### ⚙️ Fitur Utilitas
- **Undo / Redo** aksi menggambar dan transformasi.
- **Hapus Semua Objek** dengan konfirmasi.

---

## 🛠 Teknologi yang Digunakan

- **HTML5** – Struktur dan elemen antarmuka.
- **CSS3** – Styling dan layout modern.
- **Python 3** – Logika aplikasi.
- **Brython** – Menjalankan Python di browser dan berinteraksi dengan DOM.

---

## 🚀 Cara Menjalankan Aplikasi

1. Pastikan ketiga file: `index.html`, `style.css`, dan `main.py` berada dalam satu folder.
2. Tidak memerlukan server atau instalasi tambahan.
3. Buka `index.html` menggunakan browser (Chrome, Firefox, dll).
4. Aplikasi siap digunakan.

---

## 🧭 Cara Menggunakan

### 1. Menggambar Objek
- Aktifkan **Mode Gambar** (default).
- Pilih bentuk, warna, dan ketebalan garis dari panel "Alat Gambar".
- Klik dan seret mouse di kanvas untuk menggambar objek.
- Lepaskan klik untuk menyelesaikan gambar.

### 2. Mentransformasi Objek
- Aktifkan **Mode Transformasi**.
- Klik objek yang sudah ada di kanvas.
- Gunakan panel "Transformasi Objek" dan "Info Objek" untuk mengubah posisi, skala, atau rotasi objek.
- Semua aksi dapat dibatalkan atau diulangi (Undo/Redo).

---

## 📁 Struktur File

| File         | Deskripsi                                                                 |
|--------------|---------------------------------------------------------------------------|
| `index.html` | Struktur halaman dan elemen UI seperti tombol, slider, dan area kanvas.   |
| `style.css`  | Gaya visual (warna, layout, font, dll).                                   |
| `main.py`    | Logika utama: menggambar, transformasi, input pengguna, dan manajemen state.|

---

