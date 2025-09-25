import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flexpath/features/auth/domain/repositories/auth_repository.dart';

part 'auth_state.dart';

class AuthCubit extends Cubit<AuthState> {
  final AuthRepository _authRepository;

  AuthCubit({required AuthRepository authRepository})
    : _authRepository = authRepository,
      super(AuthInitial());

  Future<void> registerUser({
    required String name,
    required String email,
    required String password,
    required String role,
  }) async {
    emit(AuthLoading());
    try {
      final userCredential = await _authRepository.registerWithEmailAndPassword(
        name: name,
        email: email,
        password: password,
        role: role,
      );
      emit(AuthSuccess(userCredential.user!));
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }

  Future<void> loginUser({
    required String email,
    required String password,
  }) async {
    emit(AuthLoading());
    try {
      final userCredential = await _authRepository.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      emit(AuthSuccess(userCredential.user!));
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }

  Future<void> logoutUser() async {
    await _authRepository.signOut();
    emit(AuthInitial());
  }
}
