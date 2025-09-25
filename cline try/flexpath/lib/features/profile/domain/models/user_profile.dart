import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:equatable/equatable.dart';

class UserProfile extends Equatable {
  final String uid;
  final String name;
  final String email;
  final String role;
  final String? photoUrl;
  final String? tagline;
  final List<String>? skills;
  final String? overview;

  const UserProfile({
    required this.uid,
    required this.name,
    required this.email,
    required this.role,
    this.photoUrl,
    this.tagline,
    this.skills,
    this.overview,
  });

  @override
  List<Object?> get props => [
    uid,
    name,
    email,
    role,
    photoUrl,
    tagline,
    skills,
    overview,
  ];

  factory UserProfile.fromSnap(DocumentSnapshot snap) {
    var snapshot = snap.data() as Map<String, dynamic>;
    return UserProfile(
      uid: snapshot['uid'],
      name: snapshot['name'],
      email: snapshot['email'],
      role: snapshot['role'],
      photoUrl: snapshot['photoUrl'],
      tagline: snapshot['tagline'],
      skills: List<String>.from(snapshot['skills'] ?? []),
      overview: snapshot['overview'],
    );
  }

  Map<String, dynamic> toJson() => {
    'uid': uid,
    'name': name,
    'email': email,
    'role': role,
    'photoUrl': photoUrl,
    'tagline': tagline,
    'skills': skills,
    'overview': overview,
  };
}
