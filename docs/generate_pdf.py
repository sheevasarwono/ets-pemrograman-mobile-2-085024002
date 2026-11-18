import re
import os

class SimplePDFBuilder:
    def __init__(self, filename="docs/laporan_ets.pdf"):
        self.filename = filename
        self.objects = []
        self.pages = []
        self.current_stream = []
        self.page_width = 595.28  # A4 width in pt
        self.page_height = 841.89 # A4 height in pt
        self.margin_left = 45.0
        self.margin_right = 45.0
        self.margin_top = 50.0
        self.margin_bottom = 50.0
        self.printable_width = self.page_width - self.margin_left - self.margin_right
        self.y = self.page_height - self.margin_top

    def _add_object(self, content):
        self.objects.append(content)
        return len(self.objects)

    def new_page(self):
        if self.current_stream:
            self._finish_page()
        self.current_stream = []
        self.y = self.page_height - self.margin_top
        # Page header
        self._draw_header()

    def _draw_header(self):
        # Small running header
        header_text = "Evaluasi Tengah Semester (ETS) - Pemrograman Mobile 2 | sheva_adrian (085024002)"
        self.current_stream.append("0.4 0.4 0.4 rg")
        self.current_stream.append("BT /F1 8 Tf")
        self.current_stream.append(f"{self.margin_left:.2f} {self.page_height - 30:.2f} Td")
        self.current_stream.append(f"({self._escape(header_text)}) Tj ET")
        # Divider line
        self.current_stream.append("0.8 0.8 0.8 RG 0.5 w")
        self.current_stream.append(f"{self.margin_left:.2f} {self.page_height - 35:.2f} m {self.page_width - self.margin_right:.2f} {self.page_height - 35:.2f} l S")

    def _finish_page(self):
        # Footer page number
        page_num = len(self.pages) + 1
        footer_text = f"Halaman {page_num}"
        self.current_stream.append("0.4 0.4 0.4 rg")
        self.current_stream.append("BT /F1 8 Tf")
        self.current_stream.append(f"{self.page_width / 2.0 - 20:.2f} 30 Td")
        self.current_stream.append(f"({self._escape(footer_text)}) Tj ET")

        stream_bytes = "\n".join(self.current_stream).encode("latin-1", "replace")
        stream_obj = f"<< /Length {len(stream_bytes)} >>\nstream\n" + stream_bytes.decode("latin-1") + "\nendstream"
        stream_id = self._add_object(stream_obj)
        self.pages.append(stream_id)

    def _check_space(self, required_height):
        if self.y - required_height < self.margin_bottom:
            self.new_page()

    def _escape(self, text):
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def add_title(self, text, subtitle=None):
        self._check_space(70)
        self.current_stream.append("0.0 0.2 0.4 rg") # Dark blue
        self.current_stream.append("BT /F2 14 Tf")
        self.current_stream.append(f"{self.margin_left:.2f} {self.y:.2f} Td")
        self.current_stream.append(f"({self._escape(text)}) Tj ET")
        self.y -= 18

        if subtitle:
            self.current_stream.append("0.2 0.2 0.2 rg")
            self.current_stream.append("BT /F2 11 Tf")
            self.current_stream.append(f"{self.margin_left:.2f} {self.y:.2f} Td")
            self.current_stream.append(f"({self._escape(subtitle)}) Tj ET")
            self.y -= 16

        # Line separator
        self.current_stream.append("0.0 0.2 0.4 RG 1.5 w")
        self.current_stream.append(f"{self.margin_left:.2f} {self.y + 4:.2f} m {self.page_width - self.margin_right:.2f} {self.y + 4:.2f} l S")
        self.y -= 12

    def add_section_header(self, text):
        self._check_space(35)
        self.y -= 8
        self.current_stream.append("0.0 0.25 0.5 rg") # Blue header
        self.current_stream.append("BT /F2 11 Tf")
        self.current_stream.append(f"{self.margin_left:.2f} {self.y:.2f} Td")
        self.current_stream.append(f"({self._escape(text)}) Tj ET")
        self.y -= 6
        self.current_stream.append("0.0 0.25 0.5 RG 0.8 w")
        self.current_stream.append(f"{self.margin_left:.2f} {self.y:.2f} m {self.page_width - self.margin_right:.2f} {self.y:.2f} l S")
        self.y -= 14

    def add_subsection(self, text):
        self._check_space(25)
        self.y -= 4
        self.current_stream.append("0.1 0.3 0.5 rg")
        self.current_stream.append("BT /F2 10 Tf")
        self.current_stream.append(f"{self.margin_left:.2f} {self.y:.2f} Td")
        self.current_stream.append(f"({self._escape(text)}) Tj ET")
        self.y -= 14

    def add_paragraph(self, text, indent=0):
        # Word wrap text at approx 95 characters per line
        words = text.split(" ")
        lines = []
        cur_line = []
        cur_len = 0
        max_chars = int((self.printable_width - indent) / 5.2)

        for w in words:
            if cur_len + len(w) + 1 > max_chars:
                lines.append(" ".join(cur_line))
                cur_line = [w]
                cur_len = len(w)
            else:
                cur_line.append(w)
                cur_len += len(w) + 1
        if cur_line:
            lines.append(" ".join(cur_line))

        line_height = 13.0
        self._check_space(len(lines) * line_height + 4)

        self.current_stream.append("0.15 0.15 0.15 rg")
        for line in lines:
            self.current_stream.append("BT /F1 9.5 Tf")
            self.current_stream.append(f"{self.margin_left + indent:.2f} {self.y:.2f} Td")
            self.current_stream.append(f"({self._escape(line)}) Tj ET")
            self.y -= line_height
        self.y -= 4

    def add_bullet(self, title, description):
        text = f"* {title}: {description}" if description else f"* {title}"
        self.add_paragraph(text, indent=12)

    def add_code_block(self, code_text):
        raw_lines = code_text.strip().split("\n")
        line_height = 11.5
        box_height = len(raw_lines) * line_height + 12
        self._check_space(box_height + 10)

        box_y = self.y - box_height
        # Draw light gray background box
        self.current_stream.append("0.96 0.97 0.98 rg") # Light background
        self.current_stream.append(f"{self.margin_left:.2f} {box_y:.2f} {self.printable_width:.2f} {box_height:.2f} re f")
        self.current_stream.append("0.85 0.88 0.9 RG 0.6 w")
        self.current_stream.append(f"{self.margin_left:.2f} {box_y:.2f} {self.printable_width:.2f} {box_height:.2f} re S")

        # Draw left border accent
        self.current_stream.append("0.2 0.4 0.7 RG 2.5 w")
        self.current_stream.append(f"{self.margin_left:.2f} {box_y:.2f} m {self.margin_left:.2f} {box_y + box_height:.2f} l S")

        # Draw code lines
        text_y = self.y - 12
        self.current_stream.append("0.1 0.15 0.2 rg")
        for line in raw_lines:
            # truncate line if too long
            display_line = line[:85]
            self.current_stream.append("BT /F3 8 Tf")
            self.current_stream.append(f"{self.margin_left + 10:.2f} {text_y:.2f} Td")
            self.current_stream.append(f"({self._escape(display_line)}) Tj ET")
            text_y -= line_height

        self.y = box_y - 8

    def add_key_value_box(self, items):
        box_height = len(items) * 14.0 + 12
        self._check_space(box_height + 8)

        box_y = self.y - box_height
        self.current_stream.append("0.95 0.97 1.0 rg") # Soft light blue
        self.current_stream.append(f"{self.margin_left:.2f} {box_y:.2f} {self.printable_width:.2f} {box_height:.2f} re f")
        self.current_stream.append("0.7 0.8 0.95 RG 0.8 w")
        self.current_stream.append(f"{self.margin_left:.2f} {box_y:.2f} {self.printable_width:.2f} {box_height:.2f} re S")

        cur_y = self.y - 14
        for k, v in items:
            self.current_stream.append("0.0 0.2 0.4 rg")
            self.current_stream.append("BT /F2 9 Tf")
            self.current_stream.append(f"{self.margin_left + 12:.2f} {cur_y:.2f} Td")
            self.current_stream.append(f"({self._escape(k)}:) Tj ET")

            self.current_stream.append("0.1 0.1 0.1 rg")
            self.current_stream.append("BT /F1 9 Tf")
            self.current_stream.append(f"{self.margin_left + 140:.2f} {cur_y:.2f} Td")
            self.current_stream.append(f"({self._escape(v)}) Tj ET")
            cur_y -= 14

        self.y = box_y - 10

    def build(self):
        if self.current_stream:
            self._finish_page()

        # Build PDF objects
        # 1: Catalog
        # 2: Pages
        # 3: Font Helvetica
        # 4: Font Helvetica-Bold
        # 5: Font Courier
        # Then page objects, then stream objects

        font1_id = self._add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        font2_id = self._add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        font3_id = self._add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

        page_obj_ids = []
        for stream_id in self.pages:
            p_obj = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.page_width:.2f} {self.page_height:.2f}] "
                f"/Resources << /Font << /F1 {font1_id} 0 R /F2 {font2_id} 0 R /F3 {font3_id} 0 R >> >> "
                f"/Contents {stream_id} 0 R >>"
            )
            p_id = self._add_object(p_obj)
            page_obj_ids.append(p_id)

        # Pages root
        kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
        pages_obj = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>"
        pages_id = self._add_object(pages_obj)

        # Catalog
        catalog_obj = f"<< /Type /Catalog /Pages {pages_id} 0 R >>"
        catalog_id = self._add_object(catalog_obj)

        # Output to file
        with open(self.filename, "wb") as f:
            f.write(b"%PDF-1.4\n")
            offsets = []
            for i, obj in enumerate(self.objects):
                offsets.append(f.tell())
                f.write(f"{i + 1} 0 obj\n{obj}\nendobj\n".encode("latin-1"))

            xref_offset = f.tell()
            f.write(f"xref\n0 {len(self.objects) + 1}\n0000000000 65535 f \n".encode("latin-1"))
            for off in offsets:
                f.write(f"{off:010d} 00000 n \n".encode("latin-1"))

            f.write(f"trailer\n<< /Size {len(self.objects) + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin-1"))


def generate_report():
    pdf = SimplePDFBuilder("docs/laporan_ets.pdf")
    pdf.new_page()

    # Header Box
    pdf.add_title("UNIVERSITAS PAKUAN - SEKOLAH VOKASI", "LAPORAN EVALUASI TENGAH SEMESTER (ETS) GANJIL 2026/2027")
    
    info_items = [
        ("Nama Mahasiswa", "sheva_adrian"),
        ("NPM", "085024002"),
        ("Mata Kuliah", "Pemrograman Mobile 2 (3 SKS)"),
        ("Program Studi", "Manajemen Informatika (Semester 5)"),
        ("Dosen Penguji", "M. Saad Nurul Ishlah, M.Comp."),
        ("Sifat Ujian", "Take-home exam (individu)"),
    ]
    pdf.add_key_value_box(info_items)

    pdf.add_paragraph("PERNYATAAN INTEGRITAS AKADEMIK: Saya menyatakan dengan sesungguhnya bahwa pekerjaan evaluasi ini saya kerjakan secara mandiri dan jujur, mencantumkan seluruh sumber pustaka serta bantuan AI yang digunakan, dan siap mempertanggungjawabkan hasilnya.")

    # Bagian 1
    pdf.add_section_header("1. MODEL DATA DAN NULL SAFETY (Bobot: 15 Poin)")
    pdf.add_subsection("1.1 Konsep Sound Null Safety")
    pdf.add_paragraph("Dart 2.12+ secara default menerapkan Sound Null Safety. Variabel non-nullable dijamin oleh kompilator tidak akan pernah bernilai null pada saat aplikasi dijalankan, sehingga mencegah timbulnya NoSuchMethodError atau runtime null crash.")
    
    pdf.add_subsection("1.2 Perbedaan String vs String? dan Parameter required")
    pdf.add_bullet("String", "Tipe non-nullable yang wajib menampung objek teks nyata dan tidak boleh bernilai null. Digunakan pada atribut wajib (title, author, year).")
    pdf.add_bullet("String?", "Tipe nullable yang diizinkan memegang teks valid atau bernilai null. Digunakan pada atribut description karena bersifat opsional.")
    pdf.add_bullet("required", "Kata kunci pada named parameter konstruktor yang mewajibkan pemanggil mengisi argumen tersebut saat inisialisasi objek.")

    pdf.add_subsection("1.3 Implementasi Kelas Book & Penanganan Deskripsi Null")
    pdf.add_code_block("""class Book {
  final String id, title, author;
  final int year;
  final String? description;

  const Book({required this.id, required this.title, required this.author,
              required this.year, this.description});

  bool get hasDescription => description != null && description!.trim().isNotEmpty;
  String get displayDescription =>
      hasDescription ? description! : 'Deskripsi belum tersedia untuk buku ini.';
}""")
    pdf.add_paragraph("Sedikitnya dibuat 4 objek buku statis di mana buku ke-3 (Algoritma dan Pemrograman) sengaja diset dengan description: null guna memverifikasi fallback UI.")

    # Bagian 2
    pdf.add_section_header("2. TAMPILAN DAN LAYOUT RESPONSIF & ADAPTIF (Bobot: 20 Poin)")
    pdf.add_subsection("2.1 Perbedaan Responsive UI vs Adaptive UI")
    pdf.add_bullet("Responsive UI", "Menyesuaikan tata letak, ukuran, dan proporsi widget berdasarkan ukuran layar fisik (lebar, tinggi, orientasi portrait vs landscape).")
    pdf.add_bullet("Adaptive UI", "Menyesuaikan tampilan dan mekanisme interaksi berdasarkan sistem operasi atau platform (misal dialog Cupertino di iOS vs Material di Android, input mouse/keyboard vs sentuhan).")
    
    pdf.add_subsection("2.2 Penerapan LayoutBuilder dan MediaQuery")
    pdf.add_paragraph("Pada berkas responsive_layout.dart, aplikasi memanfaatkan LayoutBuilder untuk membaca batasan lebar (constraints.maxWidth) dan MediaQuery untuk mendeteksi orientasi:")
    pdf.add_code_block("""return LayoutBuilder(
  builder: (context, constraints) {
    final isWide = constraints.maxWidth >= 650 || (isLandscape && constraints.maxWidth >= 550);
    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(child: OwnerHeader(isWideScreen: isWide)),
        if (isWide)
          SliverGrid(gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2, crossAxisSpacing: 12, mainAxisSpacing: 12, mainAxisExtent: 310),
            delegate: SliverChildBuilderDelegate((_, i) => BookCard(book: books[i]), childCount: books.length))
        else
          SliverList(delegate: SliverChildBuilderDelegate((_, i) => BookCard(book: books[i]), childCount: books.length)),
      ],
    );
  },
);""")
    pdf.add_paragraph("Pada mobile portrait (< 650px), buku ditampilkan dalam daftar vertikal 1-kolom. Pada tablet/layar lebar (>= 650px), tampilan otomatis beralih menjadi grid 2-kolom yang rapi.")

    # Bagian 3
    pdf.add_section_header("3. PENGELOLAAN STATE DENGAN RIVERPOD (Bobot: 25 Poin)")
    pdf.add_subsection("3.1 Aliran Data Antar-Provider Reaktif")
    pdf.add_paragraph("nameProvider menyediakan nama 'sheva_adrian' dan booksProvider menyediakan koleksi buku. infoProvider mengamati keduanya secara reaktif:")
    pdf.add_code_block("""final nameProvider = Provider<String>((ref) => StudentInfo.defaultName);
final npmProvider = Provider<String>((ref) => StudentInfo.defaultNpm);
final booksProvider = Provider<List<Book>>((ref) => _initialBooks);

final infoProvider = Provider<String>((ref) {
  final name = ref.watch(nameProvider);
  final books = ref.watch(booksProvider);
  return 'Nama saya $name, saya memiliki ${books.length} buku.';
});

class ExpandedBooksNotifier extends Notifier<Set<String>> {
  @override Set<String> build() => <String>{};
  void toggle(String id) => state = state.contains(id) ? ({...state}..remove(id)) : ({...state, id});
  bool isExpanded(String id) => state.contains(id);
}
final expandedBookIdsProvider = NotifierProvider<ExpandedBooksNotifier, Set<String>>(ExpandedBooksNotifier.new);""")

    pdf.add_subsection("3.2 Perbedaan Provider, FutureProvider, dan StreamProvider")
    pdf.add_bullet("Provider", "Sinkron. Menyediakan nilai konstan atau hasil kalkulasi komputasi antar-provider tanpa loading state (contoh: infoProvider).")
    pdf.add_bullet("FutureProvider", "Asinkron satu kali. Menghasilkan AsyncValue dengan status loading, data, error. Cocok untuk REST API HTTP sekali panggil.")
    pdf.add_bullet("StreamProvider", "Asinkron berlanjut. Mendengarkan stream data real-time secara berkelanjutan (contoh: WebSocket, chat, atau sensor GPS).")

    # Bagian 4
    pdf.add_section_header("4. ANIMASI SEDERHANA (IMPLICIT ANIMATION) (Bobot: 10 Poin)")
    pdf.add_paragraph("Pada widget BookCard, diterapkan tiga implicit animation saat pengguna menekan tombol lihat/sembunyikan deskripsi:")
    pdf.add_bullet("AnimatedContainer", "Menganimasikan perubahan ukuran kotak, padding internal (EdgeInsets.zero ke EdgeInsets.all(12)), dan background color selama 300ms (Curves.easeInOut).")
    pdf.add_bullet("AnimatedOpacity", "Menganimasikan opasitas teks deskripsi secara halus dari 0.0 (transparan) ke 1.0 (tampak penuh) selama 250ms.")
    pdf.add_bullet("AnimatedRotation", "Menganimasikan perputaran ikon chevron panah sebesar 180 derajat (0.5 putaran) secara mulus.")

    # Bagian 5
    pdf.add_section_header("5. STRUKTUR APLIKASI DAN ANALISIS ARSITEKTUR (Bobot: 15 Poin)")
    pdf.add_paragraph("Kode sumber dipisahkan secara modular mengikuti kaidah arsitektur MVVM:")
    pdf.add_bullet("models/book.dart", "Model murni dan logika domain null safety entitas.")
    pdf.add_bullet("providers/", "Lapisan ViewModel Riverpod yang memproses data dan mempublikasikan state reaktif.")
    pdf.add_bullet("screens/ & widgets/", "Lapisan View yang fokus merender antarmuka dan menangkap interaksi pengguna.")
    pdf.add_paragraph("Manfaat pemisahan ini memudahkan pengujian kode (unit & widget test independen) dan memudahkan pemeliharaan tanpa risiko regresi visual.")

    # Bagian 6
    pdf.add_section_header("6. HASIL PENGUJIAN OTOMATIS & PANDUAN DEMONSTRASI (Bobot: 15 Poin)")
    pdf.add_paragraph("Hasil uji coba otomatis via 'flutter test' (5/5 Lulus 100%):")
    pdf.add_code_block("""00:00 +0: Model Data & Null Safety Tests Book constructor and null description handling
00:00 +1: Riverpod Provider Tests infoProvider correctly combines name and books count
00:00 +2: Riverpod Provider Tests expandedBookIdsProvider toggles book id state correctly
00:00 +3: Widget Integration Tests App renders owner info and books list
00:02 +4: Widget Integration Tests Tapping toggle displays fallback message for null description
00:02 +5: All tests passed!""")
    pdf.add_paragraph("Hasil analisis statis 'flutter analyze': No issues found! (Kompilasi bersih dan bebas error).")

    pdf.add_section_header("KETERANGAN PENGGUNAAN AI & REFERENSI")
    pdf.add_paragraph("Alat AI yang digunakan: Gemini / Antigravity Agent. Membantu struktur arsitektur dasar, penulisan widget test, dan verifikasi null safety. Seluruh kode telah dipahami dan diverifikasi kelulusannya secara mandiri oleh mahasiswa.")
    pdf.add_bullet("Referensi 1", "Dokumentasi Resmi Flutter: https://docs.flutter.dev/")
    pdf.add_bullet("Referensi 2", "Dokumentasi Riverpod: https://riverpod.dev/")
    pdf.add_bullet("Referensi 3", "Dart Sound Null Safety: https://dart.dev/null-safety")
    pdf.add_bullet("Referensi 4", "RPS Pemrograman Mobile 2, SV Universitas Pakuan.")

    pdf.build()
    print("PDF build complete: docs/laporan_ets.pdf")

if __name__ == "__main__":
    generate_report()
