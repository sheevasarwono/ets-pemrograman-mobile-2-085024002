import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/book.dart';
import 'user_provider.dart';

/// Daftar data awal buku (statis sesuai ketentuan)
const List<Book> _initialBooks = [
  Book(
    id: 'book-1',
    title: 'Clean Architecture: A Craftsman\'s Guide',
    author: 'Robert C. Martin',
    year: 2017,
    description:
        'Panduan mendalam tentang arsitektur perangkat lunak yang modular, terpisah dari framework, dan mudah diuji secara independen.',
  ),
  Book(
    id: 'book-2',
    title: 'Flutter Apprentice: Multiplatform Apps',
    author: 'Raywenderlich Tutorial Team',
    year: 2021,
    description:
        'Buku komprehensif untuk merancang dan membangun aplikasi multiplatform modern dari nol hingga mahir dengan Flutter dan Dart.',
  ),
  Book(
    id: 'book-3',
    title: 'Algoritma dan Pemrograman',
    author: 'Rinaldi Munir',
    year: 2018,
    description: null, // Sesuai ketentuan: sedikitnya satu buku tidak memiliki deskripsi (null)
  ),
  Book(
    id: 'book-4',
    title: 'Refactoring: Improving Code Design',
    author: 'Martin Fowler',
    year: 2018,
    description:
        'Prinsip-prinsip meningkatkan struktur internal kode tanpa mengubah perilaku eksternal, membuat kode lebih mudah dirawat.',
  ),
];

/// Provider untuk menyediakan daftar buku (booksProvider)
final booksProvider = Provider<List<Book>>((ref) {
  return _initialBooks;
});

/// Provider yang menggabungkan nama mahasiswa dan jumlah buku (infoProvider)
/// Aliran data: bergantung pada nameProvider dan booksProvider melalui ref.watch
final infoProvider = Provider<String>((ref) {
  final name = ref.watch(nameProvider);
  final books = ref.watch(booksProvider);
  return 'Nama saya $name, saya memiliki ${books.length} buku.';
});

/// Notifier untuk mengelola state buku mana saja yang sedang ditampilkan deskripsinya
class ExpandedBooksNotifier extends Notifier<Set<String>> {
  @override
  Set<String> build() {
    return <String>{};
  }

  /// Toggle status tampil/sembunyi deskripsi untuk buku tertentu
  void toggle(String bookId) {
    if (state.contains(bookId)) {
      state = {...state}..remove(bookId);
    } else {
      state = {...state, bookId};
    }
  }

  /// Memeriksa apakah buku tertentu sedang dibuka deskripsinya
  bool isExpanded(String bookId) => state.contains(bookId);
}

/// Provider pengelola state ekspansi deskripsi buku
final expandedBookIdsProvider =
    NotifierProvider<ExpandedBooksNotifier, Set<String>>(
  ExpandedBooksNotifier.new,
);

/// Provider penunjang untuk mengetahui apakah buku tertentu diekspansi
final isBookExpandedProvider = Provider.family<bool, String>((ref, bookId) {
  final expandedIds = ref.watch(expandedBookIdsProvider);
  return expandedIds.contains(bookId);
});
