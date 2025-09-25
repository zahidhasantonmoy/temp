import 'dart:io';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flexpath/features/profile/domain/models/user_profile.dart';
import 'package:flexpath/features/profile/domain/repositories/profile_repository.dart';

part 'profile_state.dart';

class ProfileCubit extends Cubit<ProfileState> {
  final ProfileRepository _profileRepository;

  ProfileCubit({required ProfileRepository profileRepository})
    : _profileRepository = profileRepository,
      super(ProfileInitial());

  Future<void> getUserProfile(String uid) async {
    emit(ProfileLoading());
    try {
      final userProfile = await _profileRepository.getUserProfile(uid);
      emit(ProfileLoaded(userProfile));
    } catch (e) {
      emit(ProfileFailure(e.toString()));
    }
  }

  Future<void> updateUserProfile(UserProfile userProfile) async {
    emit(ProfileLoading());
    try {
      await _profileRepository.updateUserProfile(userProfile);
      final updatedProfile = await _profileRepository.getUserProfile(
        userProfile.uid,
      );
      emit(ProfileLoaded(updatedProfile));
    } catch (e) {
      emit(ProfileFailure(e.toString()));
    }
  }

  Future<void> uploadProfilePicture(File image, String uid) async {
    emit(ProfileLoading());
    try {
      final photoUrl = await _profileRepository.uploadProfilePicture(
        image,
        uid,
      );
      final userProfile = await _profileRepository.getUserProfile(uid);
      final updatedProfile = UserProfile(
        uid: userProfile.uid,
        name: userProfile.name,
        email: userProfile.email,
        role: userProfile.role,
        photoUrl: photoUrl,
        tagline: userProfile.tagline,
        skills: userProfile.skills,
        overview: userProfile.overview,
      );
      await _profileRepository.updateUserProfile(updatedProfile);
      emit(ProfileLoaded(updatedProfile));
    } catch (e) {
      emit(ProfileFailure(e.toString()));
    }
  }
}
