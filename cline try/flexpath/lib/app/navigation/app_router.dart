import 'package:flexpath/features/auth/presentation/screens/login_screen.dart';
import 'package:flexpath/features/auth/presentation/screens/register_screen.dart';
import 'package:flexpath/features/auth/presentation/screens/role_selection_screen.dart';
import 'package:flexpath/features/common/presentation/screens/onboarding_screen.dart';
import 'package:flexpath/features/common/presentation/screens/splash_screen.dart';
import 'package:flexpath/features/profile/presentation/screens/create_profile_screen.dart';
import 'package:flexpath/features/profile/presentation/screens/profile_screen.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/splash',
    routes: [
      GoRoute(
        path: '/splash',
        pageBuilder:
            (context, state) => CustomTransitionPage<void>(
              key: state.pageKey,
              child: const SplashScreen(),
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) =>
                      FadeTransition(opacity: animation, child: child),
            ),
      ),
      GoRoute(
        path: '/onboarding',
        pageBuilder:
            (context, state) => CustomTransitionPage<void>(
              key: state.pageKey,
              child: const OnboardingScreen(),
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) =>
                      FadeTransition(opacity: animation, child: child),
            ),
      ),
      GoRoute(
        path: '/role-selection',
        pageBuilder:
            (context, state) => CustomTransitionPage<void>(
              key: state.pageKey,
              child: const RoleSelectionScreen(),
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) =>
                      FadeTransition(opacity: animation, child: child),
            ),
      ),
      GoRoute(
        path: '/login',
        pageBuilder:
            (context, state) => CustomTransitionPage<void>(
              key: state.pageKey,
              child: const LoginScreen(),
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) =>
                      FadeTransition(opacity: animation, child: child),
            ),
      ),
      GoRoute(
        path: '/register/:role',
        pageBuilder: (context, state) {
          final role = state.pathParameters['role']!;
          return CustomTransitionPage<void>(
            key: state.pageKey,
            child: RegisterScreen(role: role),
            transitionsBuilder:
                (context, animation, secondaryAnimation, child) =>
                    FadeTransition(opacity: animation, child: child),
          );
        },
      ),
      GoRoute(
        path: '/create-profile',
        pageBuilder:
            (context, state) => CustomTransitionPage<void>(
              key: state.pageKey,
              child: const CreateProfileScreen(),
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) =>
                      FadeTransition(opacity: animation, child: child),
            ),
      ),
      GoRoute(
        path: '/profile',
        pageBuilder:
            (context, state) => CustomTransitionPage<void>(
              key: state.pageKey,
              child: const ProfileScreen(),
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) =>
                      FadeTransition(opacity: animation, child: child),
            ),
      ),
    ],
  );
}
