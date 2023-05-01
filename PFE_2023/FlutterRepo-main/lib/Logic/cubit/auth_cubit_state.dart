part of 'auth_cubit_cubit.dart';

@immutable
abstract class AuthCubitState {}

class AuthCubitInitial extends AuthCubitState {}
class AuthCubitLoading extends AuthCubitState {}
class AuthCubitLoaded extends AuthCubitState {}
class AuthCubitError extends AuthCubitState {}
// class AuthCubitInitial extends AuthCubitState {}
