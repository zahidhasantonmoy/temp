import 'dart:io';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:flexpath/features/profile/domain/models/user_profile.dart';
import 'package:flexpath/features/profile/domain/repositories/profile_repository.dart';

class ProfileRepositoryImpl implements ProfileRepository {
  final FirebaseFirestore _firestore;
  final FirebaseStorage _storage;

  ProfileRepositoryImpl({
    FirebaseFirestore? firestore,
    FirebaseStorage? storage,
  }) : _firestore = firestore ?? FirebaseFirestore.instance,
       _storage = storage ?? FirebaseStorage.instance;

  @override
  Future<UserProfile> getUserProfile(String uid) async {
    try {
      final doc = await _firestore.collection('users').doc(uid).get();
      return UserProfile.fromSnap(doc);
    } catch (e) {
      throw Exception('Error getting user profile.');
    }
  }

  @override
  Future<void> updateUserProfile(UserProfile userProfile) async {
    try {
      await _firestore
          .collection('users')
          .doc(userProfile.uid)
          .update(userProfile.toJson());
    } catch (e) {
      throw Exception('Error updating user profile.');
    }
  }

  @override
  Future<String> uploadProfilePicture(File image, String uid) async {
    try {
      final ref = _storage.ref().child('profile_pictures').child(uid);
      await ref.putFile(image);
      return await ref.getDownloadURL();
    } catch (e) {
      throw Exception('Error uploading profile picture.');
    }
  }
}
