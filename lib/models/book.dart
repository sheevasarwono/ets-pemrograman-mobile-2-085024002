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

  /// Mengecek apakah buku memiliki deskripsi yang valid
  bool get hasDescription =>
      description != null && description!.trim().isNotEmpty;

  /// Mengembalikan deskripsi atau teks pengganti yang informatif saat null
  String get displayDescription =>
      hasDescription ? description! : 'Deskripsi belum tersedia untuk buku ini.';
}
