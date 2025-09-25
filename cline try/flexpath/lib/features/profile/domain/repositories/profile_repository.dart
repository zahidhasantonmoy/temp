import 'dart:io';
import 'package:flexpath/features/profile/domain/models/user_profile.dart';

abstract class ProfileRepository {
  Future<UserProfile> getUserProfile(String uid);
  Future<void> updateUserProfile(UserProfile userProfile);
  Future<String> uploadProfilePicture(File image, String uid);
}
