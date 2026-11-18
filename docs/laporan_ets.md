# LAPORAN EVALUASI TENGAH SEMESTER (ETS) GANJIL 2026/2027
## PEMROGRAMAN MOBILE 2 (3 SKS) — MANAJEMEN INFORMATIKA
### SEKOLAH VOKASI — UNIVERSITAS PAKUAN

---

### **IDENTITAS MAHASISWA & UJIAN**
- **Nama Mahasiswa** : sheva_adrian
- **NPM** : 085024002
- **Program Studi** : Manajemen Informatika
- **Semester** : 5
- **Mata Kuliah** : Pemrograman Mobile 2
- **Dosen Penguji** : M. Saad Nurul Ishlah, M.Comp.
- **Sifat Ujian** : Take-home exam (individu)

---

### **PERNYATAAN INTEGRITAS AKADEMIK**
Dengan mengumpulkan hasil ujian ini, saya menyatakan bahwa pekerjaan ini saya kerjakan secara mandiri dan jujur, mencantumkan sumber yang digunakan, serta siap menjelaskan dan mempertanggungjawabkan hasil pekerjaan saya.

**Bogor, 18 November 2026**  
Yang membuat pernyataan,

*( Tanda Tangan Mahasiswa )*  
**sheva_adrian (NPM: 085024002)**

---

## DAFTAR ISI
1. [BAB I: Model Data dan Null Safety](#bab-i-model-data-dan-null-safety)
2. [BAB II: Tampilan dan Layout Responsif & Adaptif](#bab-ii-tampilan-dan-layout-responsif--adaptif)
3. [BAB III: Pengelolaan State dengan Riverpod](#bab-iii-pengelolaan-state-dengan-riverpod)
4. [BAB IV: Implementasi Animasi Sederhana (Implicit Animation)](#bab-iv-implementasi-animasi-sederhana-implicit-animation)
5. [BAB V: Struktur Aplikasi dan Analisis Arsitektur (MVVM)](#bab-v-struktur-aplikasi-dan-analisis-arsitektur-mvvm)
6. [BAB VI: Demonstrasi Aplikasi dan Pengujian](#bab-vi-demonstrasi-aplikasi-dan-pengujian)
7. [Keterangan Penggunaan AI](#keterangan-penggunaan-ai)
8. [Daftar Pustaka & Referensi](#daftar-pustaka--referensi)

---

## BAB I: MODEL DATA DAN NULL SAFETY

### 1.1 Penjelasan Konsep Null Safety di Dart
Dart 2.12+ memperkenalkan fitur *Sound Null Safety*. Sistem tipe di Dart secara default bersifat *non-nullable*, artinya sebuah variabel tidak dapat bernilai `null` kecuali secara eksplisit dideklarasikan sebagai nullable. Hal ini mencegah kesalahan runtime yang sangat umum dalam pemrograman, yaitu `NullPointerException` atau *NoSuchMethodError: The getter 'x' was called on null*.

### 1.2 Perbedaan `String` dan `String?`
- **`String` (Non-nullable)**:
  Tipe data `String` mutlak harus selalu berisi objek teks yang valid (misalnya `"Clean Architecture"` atau string kosong `""`). Variabel bertipe `String` tidak pernah diizinkan bernilai `null` oleh compiler.
- **`String?` (Nullable)**:
  Tanda tanya (`?`) menandakan bahwa tipe tersebut bersifat *nullable*. Variabel bertipe `String?` dapat berisi teks yang valid ataupun bernilai `null` (menandakan ketiadaan nilai/data belum diisi).

### 1.3 Penggunaan Parameter `required`
Kata kunci `required` digunakan pada parameter bernama (*named parameters*) di dalam konstruktor. Fungsinya adalah memastikan bahwa pemanggil konstruktor wajib memberikan nilai argumen untuk parameter tersebut pada saat inisialisasi objek. Jika argumen wajib tidak diberikan, compiler akan memunculkan kesalahan (*compile-time error*).

### 1.4 Strategi Menangani Deskripsi `null`
Dalam aplikasi ini, penanganan deskripsi yang bernilai `null` dilakukan melalui beberapa mekanisme yang aman:
1. **Getter Helper (`hasDescription` & `displayDescription`)**:
   Class `Book` menyediakan getter `displayDescription` yang memeriksa kondisi null. Jika `description == null`, aplikasi tidak melakukan pemanggilan paksa (*bang operator* `!`), melainkan mengembalikan string fallback informatif: `"Deskripsi belum tersedia untuk buku ini."`.
2. **Conditional Rendering di UI**:
   Pada widget `BookCard`, sebelum menampilkan teks, sistem memeriksa properti `book.hasDescription`. Jika bernilai `false`, antarmuka menampilkan kotak peringatan informatif bertema ramah (dengan ikon `info_outline` dan warna kontras lembut) untuk memberitahukan pengguna bahwa deskripsi tidak ada.

### 1.5 Implementasi Kode `Book`
```dart
class Book {
  final String id;
  final String title;
  final String author;
  final int year;
  final String? description;

  const Book({
    required this.id,
    required this.title,
    required this.author,
    required this.year,
    this.description,
  });

  bool get hasDescription =>
      description != null && description!.trim().isNotEmpty;

  String get displayDescription =>
      hasDescription ? description! : 'Deskripsi belum tersedia untuk buku ini.';
}
```

Objek buku yang dibuat dalam aplikasi terdiri dari 4 buku, dengan buku ke-3 sengaja dibuat tanpa deskripsi (`description: null`):
1. *"Clean Architecture: A Craftsman's Guide"* (Robert C. Martin, 2017) — Deskripsi tersedia.
2. *"Flutter Apprentice: Multiplatform Apps"* (Raywenderlich Team, 2021) — Deskripsi tersedia.
3. *"Algoritma dan Pemrograman"* (Rinaldi Munir, 2018) — **`description: null`** (Uji coba null safety).
4. *"Refactoring: Improving Code Design"* (Martin Fowler, 2018) — Deskripsi tersedia.

---

## BAB II: TAMPILAN DAN LAYOUT RESPONSIF & ADAPTIF

### 2.1 Desain Antarmuka Utama
Antarmuka aplikasi dirancang modern menggunakan **Material 3**:
- **OwnerHeader Widget**: Menampilkan inisial avatar, nama mahasiswa, NPM, jumlah total koleksi buku, serta kalimat ringkasan dinamis dari `infoProvider`. Terdapat pula badge indikator layout yang aktif (*Mobile List* vs *Wide Grid*).
- **BookCard Widget**: Menampilkan judul buku dengan tipografi tebal, tahun penerbitan dengan chip badge, nama penulis dengan ikon profil, serta tombol interaksi untuk membuka atau menyembunyikan deskripsi.

### 2.2 Perbedaan Responsive UI dan Adaptive UI
| Aspek | Responsive UI (Responsif) | Adaptive UI (Adaptif) |
|---|---|---|
| **Definisi** | Menyesuaikan ukuran, proporsi, dan tata letak (*layout*) widget berdasarkan dimensi fisik layar (lebar, tinggi, orientasi). | Menyesuaikan tampilan, navigasi, dan perilaku interaksi berdasarkan platform sistem operasi (Android, iOS, macOS, Windows, Web). |
| **Fokus Utama** | Dimensi piksel, *breakpoints*, rotasi orientasi layar (*portrait* vs *landscape*). | Standar konvensi platform (misal Material Design untuk Android vs Cupertino untuk iOS, mouse hover vs sentuhan jari). |
| **Widget Utama** | `LayoutBuilder`, `MediaQuery`, `Flexible`, `Expanded`, `GridView`. | `Theme.of(context).platform`, dialog adaptif (`showAdaptiveDialog`), ikon adaptif (`Icons.adaptive.share`). |

### 2.3 Penerapan Responsive UI dalam Proyek
Proyek menerapkan Responsive UI menggunakan kombinasi **`LayoutBuilder`** dan **`MediaQuery`**:
```dart
return LayoutBuilder(
  builder: (context, constraints) {
    final isWideScreen = constraints.maxWidth >= 650 || 
        (isLandscape && constraints.maxWidth >= 550);

    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(child: OwnerHeader(isWideScreen: isWideScreen)),
        if (isWideScreen)
          SliverGrid(
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              mainAxisExtent: 310,
            ),
            delegate: SliverChildBuilderDelegate(
              (context, index) => BookCard(book: books[index]),
              childCount: books.length,
            ),
          )
        else
          SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, index) => BookCard(book: books[index]),
              childCount: books.length,
            ),
          ),
      ],
    );
  },
);
```
- **Layar Sempit (< 650px / Mobile Portrait)**: Tampilan dialirkan secara vertikal 1 kolom menggunakan `SliverList`.
- **Layar Lebar (≥ 650px / Tablet / Landscape)**: Tampilan otomatis beralih menjadi 2 kolom menggunakan `SliverGrid`.

### 2.4 Contoh Rancangan Adaptive UI
Untuk melengkapi rancangan Adaptive UI di masa depan, aplikasi dapat menerapkan:
1. Penggunaan `Switch.adaptive` atau `Slider.adaptive` yang otomatis beralih gaya ke switch bergaya iOS saat dibuka di iPhone.
2. Penggunaan `showAdaptiveDialog` yang menampilkan `CupertinoAlertDialog` di perangkat Apple dan `AlertDialog` di perangkat Android.
3. Penyesuaian kontrol input kursor mouse (*hover effect*, scroll wheel) ketika dijalankan di platform Desktop/Web dibandingkan interaksi sentuhan (*touch gestures*) pada ponsel.

---

## BAB III: PENGELOLAAN STATE DENGAN RIVERPOD

### 3.1 Mengapa Memilih Riverpod?
Riverpod adalah framework manajemen state reaktif modern untuk Flutter yang dirancang sebagai evolusi dari Provider. Riverpod menyelesaikan kelemahan Provider lama seperti:
- Menghindari runtime error `ProviderNotFoundException` (aman saat compile time).
- Memungkinkan deklarasi provider secara global tanpa memerlukan `BuildContext`.
- Mendukung pemantauan dependencies antar-provider secara deklaratif (*computed/derived state*).

### 3.2 Aliran Data Antar-Provider (*Data Flow*)
Diagram aliran data reaktif dalam aplikasi:
```
[nameProvider] (String: Nama) ----\
                                  +---> [infoProvider] ---> Dikonsumsi oleh [OwnerHeader] via ref.watch()
[booksProvider] (List<Book>)  ----/
                                        [expandedBookIdsProvider] (Notifier<Set<String>>)
                                                 |
                                                 v
                                        [isBookExpandedProvider] ---> Dikonsumsi oleh [BookCard]
```

### 3.3 Penjelasan Provider yang Dibuat
1. **`nameProvider` & `npmProvider`**:
   Menyediakan identitas mahasiswa secara terpusat:
   ```dart
   final nameProvider = Provider<String>((ref) => StudentInfo.defaultName);
   final npmProvider = Provider<String>((ref) => StudentInfo.defaultNpm);
   ```
2. **`booksProvider`**:
   Menyediakan koleksi buku statis:
   ```dart
   final booksProvider = Provider<List<Book>>((ref) => _initialBooks);
   ```
3. **`infoProvider` (Derived/Combined State)**:
   Menggabungkan nama dan jumlah buku secara reaktif menggunakan `ref.watch`:
   ```dart
   final infoProvider = Provider<String>((ref) {
     final name = ref.watch(nameProvider);
     final books = ref.watch(booksProvider);
     return 'Nama saya $name, saya memiliki ${books.length} buku.';
   });
   ```
4. **`expandedBookIdsProvider` (Stateful Notifier)**:
   Mengelola state buku mana saja yang sedang ditampilkan deskripsinya menggunakan struktur data `Set<String>` (koleksi ID unik):
   ```dart
   class ExpandedBooksNotifier extends Notifier<Set<String>> {
     @override
     Set<String> build() => <String>{};

     void toggle(String bookId) {
       if (state.contains(bookId)) {
         state = {...state}..remove(bookId);
       } else {
         state = {...state, bookId};
       }
     }

     bool isExpanded(String bookId) => state.contains(bookId);
   }
   ```

### 3.4 Perbedaan Kegunaan `Provider`, `FutureProvider`, dan `StreamProvider`
| Jenis Provider | Kegunaan & Karakteristik | Skenario Penggunaan Nyata |
|---|---|---|
| **`Provider`** | Menyediakan nilai yang sinkron (*synchronous*), komputasi murni (*computed value*), atau dependensi konstan (service/repository). Tidak memiliki status pemuatan (*loading state*). | Menyediakan konfigurasi aplikasi, daftar statis, format tanggal, atau derived state seperti `infoProvider`. |
| **`FutureProvider`** | Menangani operasi asinkron satu kali (*single asynchronous operation*). Menghasilkan `AsyncValue<T>` yang memiliki status `loading`, `data`, dan `error`. | Membaca data satu kali dari REST API HTTP, memuat berkas lokal, atau membaca preferensi dari SQLite / Shared Preferences. |
| **`StreamProvider`** | Menangani aliran data asinkron yang berlanjut seiring waktu (*multiple asynchronous events*). Menghasilkan `AsyncValue<T>` yang otomatis memperbarui widget setiap ada emit data baru. | Fitur chat real-time (Firebase Firestore/WebSocket), pemantauan lokasi GPS perangkat secara berkala, atau status konektivitas internet. |

---

## BAB IV: IMPLEMENTASI ANIMASI SEDERHANA (IMPLICIT ANIMATION)

### 4.1 Definisi Implicit Animation
Implicit Animation adalah jenis animasi di Flutter di mana framework secara otomatis menginterpolasi perubahan nilai properti (*tweening*) dari nilai lama ke nilai baru dalam durasi dan kurva tertentu tanpa memerlukan manajemen manual `AnimationController` atau `TickerProvider`.

### 4.2 Widget dan Perubahan Tampilan yang Dianimasikan
Dalam widget `BookCard`, diterapkan tiga implicit animation yang harmonis:
1. **`AnimatedContainer`**:
   - **Perubahan yang dianimasikan**: Tinggi container, padding internal (dari `EdgeInsets.zero` menjadi `EdgeInsets.all(12)`), serta warna latar belakang (`BoxDecoration.color`).
   - **Tujuan**: Memberikan efek ekspansi kartu yang halus saat pengguna menekan tombol *"Lihat Deskripsi"*.
2. **`AnimatedOpacity`**:
   - **Perubahan yang dianimasikan**: Tingkat transparansi elemen teks deskripsi (dari `opacity: 0.0` transparan penuh ke `opacity: 1.0` tampak penuh) selama 250ms dengan kurva `Curves.easeInOut`.
   - **Tujuan**: Mencegah teks muncul secara mendadak (*pop-in* kasar), melainkan muncul dengan efek pudar (*fade in*).
3. **`AnimatedRotation`**:
   - **Perubahan yang dianimasikan**: Rotasi ikon panah sebesar 0.5 putaran (180 derajat) saat status ekspansi berubah.

---

## BAB V: STRUKTUR APLIKASI DAN ANALISIS ARSITEKTUR (MVVM)

### 5.1 Pemisahan Struktur Berkas (*Separation of Concerns*)
Kode aplikasi dipisahkan menjadi modul-modul independen:
```
lib/
├── constants/
│   └── student_info.dart       # Pengaturan konstanta identitas
├── models/
│   └── book.dart               # Domain Entity & Null Safety
├── providers/
│   ├── user_provider.dart      # Business State & User Logic
│   └── book_provider.dart      # Book State & Expand Controller
├── screens/
│   └── home_screen.dart        # Tampilan Layar Utama (View)
├── widgets/
│   ├── book_card.dart          # Komponen Presentasi Buku
│   ├── owner_header.dart       # Komponen Presentasi Header
│   └── responsive_layout.dart  # Komponen Tata Letak Responsif
└── main.dart                   # Titik Awal Aplikasi (Bootstrap)
```

### 5.2 Tanggung Jawab Tiap Bagian
- **`models/`**: Bertanggung jawab penuh mendefinisikan representasi data mentah, validasi null safety, dan aturan logika bisnis entitas.
- **`providers/`**: Bertindak sebagai lapisan State Management / ViewModel yang memproses data, menanggapi interaksi pengguna (*toggle* ekspansi), dan mempublikasikan state reaktif.
- **`screens/` & `widgets/`**: Bertanggung jawab murni pada aspek presentasi (*UI/UX*), tata letak, animasi, dan merender data yang disediakan oleh provider.

### 5.3 Manfaat Pemisahan bagi Pemeliharaan & Pengujian
1. **Pemeliharaan (*Maintainability*)**: Perubahan pada tampilan UI (misalnya mengganti warna atau ukuran font) sama sekali tidak akan merusak logika bisnis di provider atau model data.
2. **Kemudahan Pengujian (*Testability*)**: Model data dan Provider dapat diuji secara terisolasi melalui *Unit Test* murni tanpa perlu memuat widget atau emulator (terbukti pada `test/widget_test.dart`).

### 5.4 Hubungan dengan Arsitektur MVVM (Model-View-ViewModel)
- **Model**: Diwakili oleh class `Book`.
- **View**: Diwakili oleh `HomeScreen`, `OwnerHeader`, `BookCard`, dan `ResponsiveLayout`.
- **ViewModel**: Diwakili oleh Riverpod Providers (`booksProvider`, `infoProvider`, dan `expandedBookIdsProvider`). View tidak pernah mengubah data secara langsung, melainkan memanggil method pada notifier (`ref.read(...notifier).toggle(...)`).
- **Bagian yang Belum Ada / Rekomendasi Masa Depan**:
  Jika ingin menerapkan arsitektur *Clean Architecture MVVM* tingkat enterprise secara penuh, dapat ditambahkan lapisan **Repository Pattern** dan **Data Source** (misal `BookRepository`, `LocalDatabaseSource`, atau `RemoteApiSource`) sebagai abstraksi pengambilan data dari internet atau database SQLite.

---

## BAB VI: DEMONSTRASI APLIKASI DAN PENGUJIAN

### 6.1 Hasil Pengujian Otomatis (*Automated Testing*)
Seluruh unit test dan widget test pada berkas `test/widget_test.dart` telah dijalankan dan lulus 100%:
```
00:00 +0: Model Data & Null Safety Tests Book constructor and null description handling
00:00 +1: Riverpod Provider Tests infoProvider correctly combines name and books count
00:00 +2: Riverpod Provider Tests expandedBookIdsProvider toggles book id state correctly
00:00 +3: Widget Integration Tests App renders owner info and books list
00:01 +4: Widget Integration Tests Tapping toggle displays fallback message for null description
00:02 +5: All tests passed!
```

### 6.2 Tangkapan Layar Tampilan Aplikasi
*(Silakan lampirkan tangkapan layar berikut ke dalam berkas PDF final)*:
1. **Tangkapan Layar 1**: Tampilan utama mode Mobile (Portrait, 1 Kolom).
2. **Tangkapan Layar 2**: Tampilan utama mode Tablet / Layar Lebar (Landscape/Grid, 2 Kolom).
3. **Tangkapan Layar 3**: Kondisi kartu saat tombol *"Lihat Deskripsi"* ditekan untuk buku dengan deskripsi lengkap (animasi ekspansi dan fade in).
4. **Tangkapan Layar 4**: Kondisi kartu saat tombol *"Lihat Deskripsi"* ditekan untuk buku tanpa deskripsi (`null`), menampilkan pesan informatif: *"Deskripsi belum tersedia untuk buku ini."*.

### 6.3 Panduan Rekaman Video Demonstrasi Mandiri
Mahasiswa dapat merekam layar (menggunakan OBS Studio / perekam layar bawaan) dengan durasi 3–5 menit:
1. Perkenalkan diri (Nama, NPM, Kelas, Mata Kuliah).
2. Tampilkan aplikasi yang sedang berjalan pada emulator atau Chrome.
3. Tunjukkan header yang memuat nama, NPM, dan teks *infoProvider*.
4. Klik tombol "Lihat Deskripsi" pada buku yang memiliki deskripsi untuk mendemonstrasikan animasi `AnimatedContainer` dan `AnimatedOpacity`.
5. Klik tombol "Lihat Deskripsi" pada buku "Algoritma dan Pemrograman" untuk memperlihatkan penanganan deskripsi `null`.
6. Ubah ukuran jendela atau putar rotasi layar untuk mendemonstrasikan perubahan layout responsif dari 1 kolom ke 2 kolom grid.
7. Jelaskan secara ringkas kode di `lib/models/book.dart`, `lib/providers/book_provider.dart`, dan `lib/widgets/book_card.dart`.
8. Unggah video ke YouTube dengan status **Unlisted** dan cantumkan tautannya pada README.md dan laporan ini.

---

## KETERANGAN PENGGUNAAN AI
Sesuai dengan ketentuan etika dan kejujuran akademik:
- **Alat AI yang Digunakan**: Gemini / Antigravity Agent.
- **Bagian yang Dibantu**: Penyusunan arsitektur dasar folder Flutter, konfigurasi dependensi `flutter_riverpod`, pembuatan script pengujian otomatis (*widget test*), serta asistensi dalam merumuskan draf pembahasan teori dan dokumentasi teknis.
- **Cara Memeriksa Hasilnya**: Mahasiswa memeriksa dan memahami setiap baris kode, memastikan dependensi berhasil diunduh via `flutter pub get`, memverifikasi kelulusan seluruh pengujian via `flutter test`, memeriksa nol pesan error melalui `flutter analyze`, serta menguji interaktivitas aplikasi secara visual.

---

## DAFTAR PUSTAKA & REFERENSI
1. Google LLC. (2024). *Flutter Documentation: Layouts and Responsive Apps*. https://docs.flutter.dev/ui/layout/responsive-adaptive
2. Roumanille, R. (2024). *Riverpod: A Reactive Caching and Data-Binding Framework*. https://riverpod.dev/
3. Dart Dev Team. (2024). *Understanding Null Safety*. https://dart.dev/null-safety
4. Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
5. Silabus & RPS Pemrograman Mobile 2, Program Studi Manajemen Informatika, Sekolah Vokasi Universitas Pakuan.
