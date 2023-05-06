import 'dart:convert';

import 'package:hive_flutter/hive_flutter.dart';
import 'package:http/http.dart' as http;

class AuthService {
  Future<String> signIn(String phoneNumber, String password) async {
    print('object');
    const baseUrl = 'http://192.168.1.203:8000/';
    const endpoint = 'login_P/';

    final uri = Uri.parse(baseUrl + endpoint);
    // const url = 'http://192.168.1.203:8000/login_P/';
    // final uri = Uri.parse(url);
    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(
        {'phone_number': phoneNumber, 'password': password},
      ),
    );

    if (response.statusCode == 200) {
      print('object');
      print(response.body);
      return response.body;
    } else {
      throw Exception('Something went wrong');
    }
  }

  Future<String> signUp(String email, String password, String password2) async {
    const baseUrl = 'http://127.0.0.1:8000/';
    const endpoint = 'users/register/';

    final uri = Uri.parse(baseUrl + endpoint);

    final response = await http.post(uri,
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(
          {
            'email': email,
            'password': password,
            'password2': password2,
          },
        ));

    print(response.statusCode);

    if (response.statusCode == 200) {
      signIn(email, password);
      // print(response.body)
      // var x = json.decode(response.body);
      // var y = x['refresh'];
      // var z = x['access'];
      // debugPrint('this is the refresh $y');
      // debugPrint('this is the access $z');
      return response.body;
    } else {
      throw Exception(response.body);
    }
  }
}


// Sanandreas@@