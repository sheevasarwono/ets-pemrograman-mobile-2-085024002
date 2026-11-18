import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../constants/student_info.dart';

/// Provider yang menyediakan nama mahasiswa
final nameProvider = Provider<String>((ref) {
  return StudentInfo.defaultName;
});

/// Provider yang menyediakan NPM mahasiswa
final npmProvider = Provider<String>((ref) {
  return StudentInfo.defaultNpm;
});
