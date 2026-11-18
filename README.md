# Katalog Buku Pribadi (ETS Pemrograman Mobile 2)

Proyek ini dibangun untuk memenuhi **Evaluasi Tengah Semester (ETS) Ganjil Tahun Akademik 2026/2027** pada mata kuliah **Pemrograman Mobile 2**, Program Studi **Manajemen Informatika**, **Sekolah Vokasi Universitas Pakuan**.

---

## 👤 Identitas Mahasiswa
- **Nama**: sheva_adrian
- **NPM**: 085024002
- **Program Studi**: Manajemen Informatika
- **Mata Kuliah**: Pemrograman Mobile 2
- **Dosen Penguji**: M. Saad Nurul Ishlah, M.Comp.

---

## 📱 Deskripsi & Fitur Aplikasi

Aplikasi **Katalog Buku Pribadi** adalah aplikasi mobile berbasis Flutter yang menampilkan identitas pemilik koleksi buku beserta daftar buku koleksinya dengan arsitektur bersih, *state management* modern menggunakan **Riverpod**, serta antarmuka yang responsif dan interaktif.

### Fitur Utama:
1. **Identitas Pemilik & Info Dinamis**:
   - Menampilkan nama dan NPM mahasiswa secara terpusat melalui Riverpod (`nameProvider` & `npmProvider`).
   - Menampilkan ringkasan otomatis: *"Nama saya sheva_adrian, saya memiliki [X] buku."* yang dihasilkan oleh `infoProvider` yang secara reaktif mengamati `nameProvider` dan `booksProvider`.
   - Menampilkan indikator tata letak adaptif/responsif (Mobile List vs Wide Grid).
2. **Koleksi Buku & Null Safety**:
   - Menampilkan daftar buku dengan informasi lengkap: Judul (`title`), Penulis (`author`), dan Tahun Terbit (`year`).
   - Menerapkan fitur **Null Safety** pada properti `description` (`String?`).
   - Menyediakan teks fallback/pengganti yang informatif (*"Deskripsi belum tersedia untuk buku ini."*) saat deskripsi bernilai `null`.
3. **State Management Interaktif (Riverpod)**:
   - State ekspansi deskripsi buku dikelola secara independen menggunakan `NotifierProvider` (`expandedBookIdsProvider`).
   - Setiap kartu buku dapat dibuka atau ditutup deskripsinya tanpa mengganggu state kartu lainnya.
   - Tersedia tombol cepat pada AppBar untuk menutup seluruh deskripsi (*Collapse All*).
4. **Animasi Halus (*Implicit Animation*)**:
   - Menggunakan `AnimatedContainer` untuk transisi ukuran dan dekorasi kartu saat dibuka/ditutup.
   - Menggunakan `AnimatedOpacity` untuk efek pemudaran teks deskripsi (*fade in/out*).
   - Menggunakan `AnimatedRotation` untuk menganimasikan putaran ikon panah toggle ekspansi.
5. **Tata Letak Responsif (*Responsive UI*)**:
   - Menggunakan `LayoutBuilder` dan `MediaQuery` untuk menyesuaikan tampilan:
     - **Mode Mobile / Layar Sempit (< 650px)**: Tampilan vertikal 1-kolom (`SliverList`).
     - **Mode Tablet / Desktop / Layar Lebar (≥ 650px)**: Tampilan grid 2-kolom (`SliverGrid`).

---

## 🛠️ Versi Teknologi & Dependensi

- **Flutter**: Versi 3.x (Dart 3.x)
- **flutter_riverpod**: `^2.6.1`
- **cupertino_icons**: `^1.0.8`

---

## 🚀 Langkah Menjalankan Aplikasi

1. **Clone repository ini**:
   ```bash
   git clone https://github.com/sheevasarwono/ets-pemrograman-mobile-2-085024002.git
   cd ets-pemrograman-mobile-2-085024002
   ```
2. **Unduh dependensi (packages)**:
   ```bash
   flutter pub get
   ```
3. **Jalankan pengujian (*Unit & Widget Tests*)**:
   ```bash
   flutter test
   ```
4. **Jalankan aplikasi**:
   - Menjalankan pada emulator Android / iOS / Chrome:
     ```bash
     flutter run
     ```
   - Menjalankan secara khusus pada Chrome (Web):
     ```bash
     flutter run -d chrome
     ```
   - Menjalankan pada Windows Desktop:
     ```bash
     flutter run -d windows
     ```

---

## 📸 Tangkapan Layar (Screenshots)

| Tampilan Mobile (List View) | Tampilan Tablet / Layar Lebar (Grid View) | Kondisi Interaksi (Deskripsi Dibuka & Null State) |
|:---:|:---:|:---:|
| *(Lampirkan tangkapan layar di sini)* | *(Lampirkan tangkapan layar di sini)* | *(Lampirkan tangkapan layar di sini)* |

> Tangkapan layar juga disertakan secara lengkap di dalam dokumen laporan PDF pada direktori `docs/`.

---

## 🎬 Tautan Video Demonstrasi

- **Link Video Demonstrasi**: `[Tautan Video YouTube Unlisted / Drive Mahasiswa]`  
  *(Pastikan tautan video dapat diakses oleh dosen penguji tanpa pembatasan izin)*

Video demonstrasi mencakup:
1. Demonstrasi aplikasi saat pertama kali dibuka.
2. Demonstrasi interaksi tombol lihat/sembunyikan deskripsi beserta animasi implicit.
3. Demonstrasi penanganan buku yang memiliki deskripsi dan buku dengan deskripsi `null`.
4. Demonstrasi perubahan tata letak responsif saat ukuran layar atau orientasi diubah.
5. Penjelasan singkat mengenai kode sumber utama (Model, Riverpod Provider, Widget, dan MVVM).

---

## ⚠️ Fitur yang Belum Berfungsi

- **Status**: Seluruh fitur yang disyaratkan dalam soal evaluasi telah **100% selesai dan berfungsi dengan baik** (Model Data, Null Safety, Riverpod State, Implicit Animation, Responsive Layout, dan Unit/Widget Testing).

---

## 🏛️ Struktur Arsitektur Proyek

Proyek ini menerapkan pemisahan kode (*separation of concerns*) yang terinspirasi dari pola arsitektur **MVVM (Model-View-ViewModel)**:

```
lib/
├── constants/
│   └── student_info.dart       # Informasi konstanta nama & NPM mahasiswa
├── models/
│   └── book.dart               # Data model & implementasi Null Safety
├── providers/
│   ├── user_provider.dart      # Provider untuk identitas mahasiswa
│   └── book_provider.dart      # State management buku & ekspansi (Riverpod)
├── screens/
│   └── home_screen.dart        # Halaman antarmuka utama (View)
├── widgets/
│   ├── book_card.dart          # Komponen kartu buku & Implicit Animation
│   ├── owner_header.dart       # Komponen header identitas pemilik
│   └── responsive_layout.dart  # Komponen pengatur layout responsif
└── main.dart                   # Entry point aplikasi & ProviderScope
```

---

## 🤖 Keterangan Penggunaan AI

Sesuai instruksi kejujuran akademik:
- **Alat AI yang Digunakan**: Gemini / Antigravity Agent.
- **Bagian yang Dibantu**: Pembuatan struktur awal berkas kode arsitektural Flutter, konfigurasi dependensi `flutter_riverpod`, penulisan uji coba widget (*widget test*), serta penyusunan draf dokumentasi teknis.
- **Cara Memeriksa Hasilnya**: Mahasiswa memeriksa setiap baris kode dengan menjalankan `flutter test`, meninjau logika null safety pada class `Book`, memverifikasi siklus reaktivitas pada `infoProvider` dan `expandedBookIdsProvider`, serta menguji kompilasi dan interaksi UI secara langsung.

---

## 📚 Referensi

1. Dokumentasi Resmi Flutter: https://docs.flutter.dev/
2. Dokumentasi Resmi Riverpod: https://riverpod.dev/
3. Panduan Null Safety Dart: https://dart.dev/null-safety
4. Flutter Responsive & Adaptive Design: https://docs.flutter.dev/ui/layout/responsive-adaptive
5. RPS Pemrograman Mobile 2, Program Studi Manajemen Informatika, Sekolah Vokasi Universitas Pakuan.
