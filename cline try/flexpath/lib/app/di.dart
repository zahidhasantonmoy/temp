import 'package:flexpath/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:flexpath/features/auth/domain/repositories/auth_repository.dart';
import 'package:flexpath/features/auth/presentation/cubit/auth_cubit.dart';
import 'package:flexpath/features/profile/data/repositories/profile_repository_impl.dart';
import 'package:flexpath/features/profile/domain/repositories/profile_repository.dart';
import 'package:flexpath/features/profile/presentation/cubit/profile_cubit.dart';
import 'package:get_it/get_it.dart';

final sl = GetIt.instance;

void init() {
  // Cubits
  sl.registerFactory(() => AuthCubit(authRepository: sl()));
  sl.registerFactory(() => ProfileCubit(profileRepository: sl()));

  // Repositories
  sl.registerLazySingleton<AuthRepository>(() => AuthRepositoryImpl());
  sl.registerLazySingleton<ProfileRepository>(() => ProfileRepositoryImpl());
}
