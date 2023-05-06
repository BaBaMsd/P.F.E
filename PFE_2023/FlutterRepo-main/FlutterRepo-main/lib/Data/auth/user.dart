import 'dart:convert';

class UserModel {
  final String email;
  final String password;
  final String password2;
  UserModel({
    required this.email,
    required this.password,
    required this.password2,
  });

  UserModel copyWith({
    String? email,
    String? password,
    String? password2,
  }) {
    return UserModel(
      email: email ?? this.email,
      password: password ?? this.password,
      password2: password2 ?? this.password2,
    );
  }

  Map<String, dynamic> toMap() {
    final result = <String, dynamic>{};

    result.addAll({'email': email});
    result.addAll({'password': password});
    result.addAll({'password2': password2});

    return result;
  }

  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      email: map['email'] ?? '',
      password: map['password'] ?? '',
      password2: map['password2'] ?? '',
    );
  }

  String toJson() => json.encode(toMap());

  factory UserModel.fromJson(String source) =>
      UserModel.fromMap(json.decode(source));

  @override
  String toString() =>
      'UserModel(email: $email, password: $password, password2: $password2)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is UserModel &&
        other.email == email &&
        other.password == password &&
        other.password2 == password2;
  }

  @override
  int get hashCode => email.hashCode ^ password.hashCode ^ password2.hashCode;
}
