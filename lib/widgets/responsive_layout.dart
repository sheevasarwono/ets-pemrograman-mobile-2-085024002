import 'package:flutter/material.dart';
import '../models/book.dart';
import 'book_card.dart';
import 'owner_header.dart';

/// Widget yang mengimplementasikan Responsive Layout menggunakan LayoutBuilder & MediaQuery
class ResponsiveLayout extends StatelessWidget {
  final List<Book> books;

  const ResponsiveLayout({
    super.key,
    required this.books,
  });

  @override
  Widget build(BuildContext context) {
    // Penggunaan MediaQuery untuk mendapatkan dimensi keseluruhan layar
    final mediaQueryData = MediaQuery.of(context);
    final isLandscape = mediaQueryData.orientation == Orientation.landscape;

    // Penggunaan LayoutBuilder untuk merespons batasan ukuran (constraints) secara dinamis
    return LayoutBuilder(
      builder: (context, constraints) {
        // Breakpoint lebar: Jika lebar >= 650 px atau dalam mode landscape dengan lebar cukup
        final isWideScreen = constraints.maxWidth >= 650 || (isLandscape && constraints.maxWidth >= 550);

        return CustomScrollView(
          slivers: [
            // Header Mahasiswa
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: OwnerHeader(isWideScreen: isWideScreen),
              ),
            ),

            // Judul Bagian Daftar Buku
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.only(left: 4, bottom: 8),
                child: Row(
                  children: [
                    const Icon(Icons.menu_book, size: 20),
                    const SizedBox(width: 8),
                    Text(
                      'Daftar Buku Koleksi',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const Spacer(),
                    Text(
                      '${books.length} item',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            color: Colors.grey[600],
                          ),
                    ),
                  ],
                ),
              ),
            ),

            // Tampilan Responsif: Grid 2-Kolom untuk Layar Lebar, List 1-Kolom untuk Mobile
            if (isWideScreen)
              SliverGrid(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  mainAxisExtent: 310,
                ),
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    return BookCard(book: books[index]);
                  },
                  childCount: books.length,
                ),
              )
            else
              SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    return BookCard(book: books[index]);
                  },
                  childCount: books.length,
                ),
              ),

            // Padding bawah ekstra agar nyaman di-scroll
            const SliverToBoxAdapter(
              child: SizedBox(height: 24),
            ),
          ],
        );
      },
    );
  }
}
