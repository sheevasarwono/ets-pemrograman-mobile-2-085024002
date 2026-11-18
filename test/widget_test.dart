import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:katalog_buku/main.dart';
import 'package:katalog_buku/models/book.dart';
import 'package:katalog_buku/providers/book_provider.dart';
import 'package:katalog_buku/providers/user_provider.dart';

void main() {
  group('Model Data & Null Safety Tests', () {
    test('Book constructor and null description handling', () {
      const bookWithDesc = Book(
        id: '1',
        title: 'Flutter Guide',
        author: 'John Doe',
        year: 2023,
        description: 'Buku panduan Flutter.',
      );

      const bookWithoutDesc = Book(
        id: '2',
        title: 'Dart Basics',
        author: 'Jane Doe',
        year: 2022,
        description: null,
      );

      expect(bookWithDesc.hasDescription, isTrue);
      expect(bookWithDesc.displayDescription, 'Buku panduan Flutter.');

      expect(bookWithoutDesc.hasDescription, isFalse);
      expect(
        bookWithoutDesc.displayDescription,
        'Deskripsi belum tersedia untuk buku ini.',
      );
    });
  });

  group('Riverpod Provider Tests', () {
    test('infoProvider correctly combines name and books count', () {
      final container = ProviderContainer(
        overrides: [
          nameProvider.overrideWithValue('Budi'),
          booksProvider.overrideWithValue([
            const Book(
              id: 'b1',
              title: 'Book A',
              author: 'Author A',
              year: 2020,
            ),
            const Book(
              id: 'b2',
              title: 'Book B',
              author: 'Author B',
              year: 2021,
            ),
          ]),
        ],
      );

      addTearDown(container.dispose);

      final info = container.read(infoProvider);
      expect(info, 'Nama saya Budi, saya memiliki 2 buku.');
    });

    test('expandedBookIdsProvider toggles book id state correctly', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      final notifier = container.read(expandedBookIdsProvider.notifier);

      expect(notifier.isExpanded('book-1'), isFalse);

      notifier.toggle('book-1');
      expect(notifier.isExpanded('book-1'), isTrue);

      notifier.toggle('book-1');
      expect(notifier.isExpanded('book-1'), isFalse);
    });
  });

  group('Widget Integration Tests', () {
    testWidgets('App renders owner info and books list', (tester) async {
      tester.view.physicalSize = const Size(800, 1400);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);

      await tester.pumpWidget(
        const ProviderScope(
          child: MyApp(),
        ),
      );
      await tester.pumpAndSettle();

      // Memastikan AppBar dan judul tampil
      expect(find.text('Katalog Buku Pribadi'), findsOneWidget);

      // Memastikan teks info gabungan dari infoProvider tampil
      expect(find.textContaining('Nama saya'), findsOneWidget);
      expect(find.textContaining('saya memiliki'), findsOneWidget);

      // Memastikan buku pertama tampil
      expect(
        find.text('Clean Architecture: A Craftsman\'s Guide'),
        findsOneWidget,
      );
      expect(find.text('Robert C. Martin'), findsOneWidget);

      // Memastikan buku tanpa deskripsi tampil
      expect(find.text('Algoritma dan Pemrograman'), findsOneWidget);
      expect(find.text('Rinaldi Munir'), findsOneWidget);
    });

    testWidgets('Tapping toggle displays fallback message for null description',
        (tester) async {
      tester.view.physicalSize = const Size(800, 1200);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);

      await tester.pumpWidget(
        const ProviderScope(
          child: MyApp(),
        ),
      );
      await tester.pumpAndSettle();

      // Cari tombol toggle untuk buku 'Algoritma dan Pemrograman' (buku ke-3 dengan index 2)
      final toggleButtons = find.text('Lihat Deskripsi');
      expect(toggleButtons, findsWidgets);

      final thirdButton = toggleButtons.at(2);
      await tester.ensureVisible(thirdButton);
      await tester.pumpAndSettle();

      // Ketuk tombol toggle ketiga (buku tanpa deskripsi)
      await tester.tap(thirdButton);
      await tester.pumpAndSettle();

      // Memverifikasi teks pengganti informatif saat deskripsi null muncul
      expect(
        find.text('Deskripsi belum tersedia untuk buku ini.'),
        findsOneWidget,
      );
    });
  });
}
