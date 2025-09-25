import 'package:flexpath/features/auth/presentation/cubit/auth_cubit.dart';
import 'package:flexpath/features/profile/presentation/cubit/profile_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final authState = context.watch<AuthCubit>().state;
    if (authState is AuthSuccess) {
      context.read<ProfileCubit>().getUserProfile(authState.user.uid);
    }

    return Scaffold(
      body: BlocBuilder<ProfileCubit, ProfileState>(
        builder: (context, state) {
          if (state is ProfileLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state is ProfileFailure) {
            return Center(child: Text(state.message));
          }
          if (state is ProfileLoaded) {
            final userProfile = state.userProfile;
            return CustomScrollView(
              slivers: [
                SliverAppBar(
                  expandedHeight: 200.0,
                  floating: false,
                  pinned: true,
                  flexibleSpace: FlexibleSpaceBar(
                    title: Text(userProfile.name),
                    background:
                        userProfile.photoUrl != null
                            ? Image.network(
                              userProfile.photoUrl!,
                              fit: BoxFit.cover,
                            )
                            : Container(color: Colors.grey),
                  ),
                ),
                SliverList(
                  delegate: SliverChildListDelegate([
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            userProfile.tagline ?? 'No tagline',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            userProfile.email,
                            style: Theme.of(context).textTheme.titleMedium,
                          ),
                          const Divider(height: 32),
                          Text(
                            'Skills',
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                          const SizedBox(height: 8),
                          Wrap(
                            spacing: 8.0,
                            children:
                                userProfile.skills
                                    ?.map((skill) => Chip(label: Text(skill)))
                                    .toList() ??
                                [],
                          ),
                          const Divider(height: 32),
                          Text(
                            'Overview',
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                          const SizedBox(height: 8),
                          Text(userProfile.overview ?? 'No overview yet.'),
                        ],
                      ),
                    ),
                  ]),
                ),
              ],
            );
          }
          return const Center(child: Text('No user logged in.'));
        },
      ),
    );
  }
}
