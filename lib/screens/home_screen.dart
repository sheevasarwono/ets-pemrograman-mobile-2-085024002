import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/book_provider.dart';
import '../widgets/responsive_layout.dart';

/// Halaman utama katalog buku pribadi (ConsumerWidget)
class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Membaca daftar buku menggunakan ref.watch
    final books = ref.watch(booksProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Row(
          children: [
            Icon(Icons.auto_stories),
            SizedBox(width: 10),
            Text(
              'Katalog Buku Pribadi',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ],
        ),
        elevation: 1,
        actions: [
          // Fitur 1 yang Belum Berfungsi: Tombol Pencarian Buku
          IconButton(
            tooltip: 'Cari Buku (Belum Berfungsi)',
            icon: const Icon(Icons.search),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text(
                    '⚠️ Fitur Pencarian & Filter buku belum berfungsi (Dalam tahap pengembangan).',
                  ),
                  duration: Duration(seconds: 2),
                  behavior: SnackBarBehavior.floating,
                ),
              );
            },
          ),
          // Fitur Berfungsi: Tombol Reset / Collapse All Deskripsi
          IconButton(
            tooltip: 'Tutup Semua Deskripsi',
            icon: const Icon(Icons.unfold_less),
            onPressed: () {
              // Reset state ekspansi Riverpod
              ref.invalidate(expandedBookIdsProvider);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Semua deskripsi buku ditutup.'),
                  duration: Duration(seconds: 1),
                  behavior: SnackBarBehavior.floating,
                ),
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: ResponsiveLayout(books: books),
        ),
      ),
      // Fitur 2 yang Belum Berfungsi: FloatingActionButton Tambah Buku Baru
      floatingActionButton: FloatingActionButton.extended(
        icon: const Icon(Icons.add),
        label: const Text('Tambah Buku'),
        tooltip: 'Tambah Buku Baru (Belum Berfungsi)',
        onPressed: () {
          showDialog(
            context: context,
            builder: (ctx) => AlertDialog(
              title: const Row(
                children: [
                  Icon(Icons.construction, color: Colors.orange),
                  SizedBox(width: 8),
                  Text('Fitur Belum Berfungsi'),
                ],
              ),
              content: const Text(
                'Fitur "Tambah Buku Baru" saat ini belum berfungsi karena belum terhubung ke formulir input dan database lokal. Fitur ini direncanakan untuk tahap pengembangan berikutnya.',
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.of(ctx).pop(),
                  child: const Text('Tutup'),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
