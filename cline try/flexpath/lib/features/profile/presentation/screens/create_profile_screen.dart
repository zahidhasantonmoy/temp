import 'dart:io';
import 'package:flexpath/features/profile/presentation/cubit/profile_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:image_picker/image_picker.dart';

class CreateProfileScreen extends StatefulWidget {
  const CreateProfileScreen({super.key});

  @override
  State<CreateProfileScreen> createState() => _CreateProfileScreenState();
}

class _CreateProfileScreenState extends State<CreateProfileScreen> {
  int _currentStep = 0;
  File? _image;
  final _taglineController = TextEditingController();
  final _skillsController = TextEditingController();
  final _overviewController = TextEditingController();
  final List<String> _skills = [];

  Future<void> _pickImage() async {
    final pickedFile = await ImagePicker().pickImage(
      source: ImageSource.gallery,
    );
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Create Your Profile')),
      body: Stepper(
        type: StepperType.horizontal,
        currentStep: _currentStep,
        onStepContinue: () {
          if (_currentStep < 2) {
            setState(() {
              _currentStep += 1;
            });
          } else {
            // Final step: save profile
          }
        },
        onStepCancel: () {
          if (_currentStep > 0) {
            setState(() {
              _currentStep -= 1;
            });
          }
        },
        steps: [
          Step(
            title: const Text('Basic Info'),
            content: Column(
              children: [
                GestureDetector(
                  onTap: _pickImage,
                  child: CircleAvatar(
                    radius: 50,
                    backgroundImage: _image != null ? FileImage(_image!) : null,
                    child:
                        _image == null
                            ? const Icon(Icons.camera_alt, size: 50)
                            : null,
                  ),
                ),
                const SizedBox(height: 20),
                TextField(
                  controller: _taglineController,
                  decoration: const InputDecoration(labelText: 'Tagline'),
                ),
              ],
            ),
            isActive: _currentStep >= 0,
          ),
          Step(
            title: const Text('Skills'),
            content: Column(
              children: [
                TextField(
                  controller: _skillsController,
                  decoration: InputDecoration(
                    labelText: 'Add a skill',
                    suffixIcon: IconButton(
                      icon: const Icon(Icons.add),
                      onPressed: () {
                        if (_skillsController.text.isNotEmpty) {
                          setState(() {
                            _skills.add(_skillsController.text);
                            _skillsController.clear();
                          });
                        }
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 8.0,
                  children:
                      _skills
                          .map(
                            (skill) => Chip(
                              label: Text(skill),
                              onDeleted: () {
                                setState(() {
                                  _skills.remove(skill);
                                });
                              },
                            ),
                          )
                          .toList(),
                ),
              ],
            ),
            isActive: _currentStep >= 1,
          ),
          Step(
            title: const Text('Overview'),
            content: TextField(
              controller: _overviewController,
              maxLines: 5,
              decoration: const InputDecoration(
                labelText: 'Tell us about yourself',
                border: OutlineInputBorder(),
              ),
            ),
            isActive: _currentStep >= 2,
          ),
        ],
      ),
    );
  }
}
