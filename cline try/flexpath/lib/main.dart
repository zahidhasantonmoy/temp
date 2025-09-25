import 'package:firebase_core/firebase_core.dart';
import 'package:flexpath/app/config/app_theme.dart';
import 'package:flexpath/app/di.dart' as di;
import 'package:flexpath/app/navigation/app_router.dart';
import 'package:flexpath/features/auth/presentation/cubit/auth_cubit.dart';
import 'package:flexpath/features/profile/presentation/cubit/profile_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    // Options will be added by the FlutterFire CLI.
    // options: DefaultFirebaseOptions.currentPlatform,
  );
  di.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => di.sl<AuthCubit>()),
        BlocProvider(create: (_) => di.sl<ProfileCubit>()),
      ],
      child: MaterialApp.router(
        title: 'Flexpath',
        theme: AppTheme.lightTheme,
        routerConfig: AppRouter.router,
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
