import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:vaccination/Data/auth/auth_service.dart';

import '../widgets/text_field.dart';

class Login extends StatefulWidget {
  const Login({super.key});

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> {
  bool isParent = false;
  final String font = 'JetBrainsMono';
  final TextEditingController _nniController = TextEditingController();
  final TextEditingController _nomController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(
                // color: Colors.red,
                height: MediaQuery.of(context).size.height / 2.6,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Center(
                      child: Image.asset(
                        'Img/vaccinated.png',
                        height: MediaQuery.of(context).size.height / 3,
                      ),
                    ),
                    const Text(
                      'Vacciné',
                      style: TextStyle(
                        fontSize: 22,
                        fontFamily: 'JetBrainsMono',
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(
                // color: Colors.green,
                height: MediaQuery.of(context).size.height / 2.7,
                child: Column(
                  // crossAxisAlignment: Cro,
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Center(
                      child: CustomTextField(
                        maxLength: 200,
                        textInputType: const TextInputType.numberWithOptions(
                            signed: true, decimal: true),
                        fieldName: 'Phone :',
                        height: MediaQuery.of(context).size.height / 16,
                        width: MediaQuery.of(context).size.width / 1.1,
                        controller: _phoneController,
                      ),
                    ),
                    Center(
                      child: CustomTextField(
                        maxLength: 200,
                        // textInputType: (
                        //     signed: true, decimal: true),
                        fieldName: 'Password :',
                        height: MediaQuery.of(context).size.height / 16,
                        width: MediaQuery.of(context).size.width / 1.1,
                        controller: _passwordController,
                      ),
                    ),

                    // Row(
                    //   mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    //   children: [
                    //     SizedBox(
                    //       height: 68,
                    //       width: 64,
                    //       child: TextField(
                    //         onChanged: (value) {
                    //           if (value.length == 1) {
                    //             FocusScope.of(context).nextFocus();
                    //           }
                    //         },
                    //         textAlign: TextAlign.center,
                    //         keyboardType: TextInputType.number,
                    //         inputFormatters: [
                    //           LengthLimitingTextInputFormatter(1),
                    //           FilteringTextInputFormatter.digitsOnly,
                    //         ],
                    //       ),
                    //     ),
                    //     SizedBox(
                    //       height: 68,
                    //       width: 64,
                    //       child: TextField(
                    //         onChanged: (value) {
                    //           if (value.length == 1) {
                    //             FocusScope.of(context).nextFocus();
                    //           }
                    //         },
                    //         textAlign: TextAlign.center,
                    //         keyboardType: TextInputType.number,
                    //         inputFormatters: [
                    //           LengthLimitingTextInputFormatter(1),
                    //           FilteringTextInputFormatter.digitsOnly,
                    //         ],
                    //       ),
                    //     ),
                    //     SizedBox(
                    //       height: 68,
                    //       width: 64,
                    //       child: TextField(
                    //         onChanged: (value) {
                    //           if (value.length == 1) {
                    //             FocusScope.of(context).nextFocus();
                    //           }
                    //         },
                    //         textAlign: TextAlign.center,
                    //         keyboardType: TextInputType.number,
                    //         inputFormatters: [
                    //           LengthLimitingTextInputFormatter(1),
                    //           FilteringTextInputFormatter.digitsOnly,
                    //         ],
                    //       ),
                    //     ),
                    //     SizedBox(
                    //       height: 68,
                    //       width: 64,
                    //       child: TextField(
                    //         onChanged: (value) {
                    //           if (value.length == 1) {
                    //             FocusScope.of(context).nextFocus();
                    //           }
                    //         },
                    //         textAlign: TextAlign.center,
                    //         keyboardType: TextInputType.number,
                    //         inputFormatters: [
                    //           LengthLimitingTextInputFormatter(1),
                    //           FilteringTextInputFormatter.digitsOnly,
                    //         ],
                    //       ),
                    //     ),
                    //   ],
                    // )
                  ],
                ),
              ),
              Center(
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(12),
                    child: MaterialButton(
                      // shape: ShapeBorder(),
                      color: Colors.greenAccent[200],
                      onPressed: () {
                        AuthService().signIn(
                            _phoneController.text, _passwordController.text);
                        // print(isParent);
                        // print(_nniController.text);
                      },
                      child: const Text(
                        'Se connecter',
                      ),
                    ),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
