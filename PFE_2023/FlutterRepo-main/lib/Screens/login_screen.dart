import 'package:flutter/material.dart';

import '../widgets/text_field.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool isParent = false;
  final String font = 'JetBrainsMono';
  final TextEditingController _nniController = TextEditingController();
  final TextEditingController _nomController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
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

                    // Text('NNI'),
                  ],
                ),
              ),
              SizedBox(
                // color: Colors.green,
                height: MediaQuery.of(context).size.height / 2.7,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Center(
                      child: CustomTextField(
                        fieldName: 'NNI :',
                        height: MediaQuery.of(context).size.height / 16,
                        width: MediaQuery.of(context).size.width / 1.1,
                        controller: _nniController,
                      ),
                    ),
                    CustomTextField(
                      fieldName: 'Nom :',
                      height: MediaQuery.of(context).size.height / 16,
                      width: MediaQuery.of(context).size.width / 1.1,
                      controller: _nomController,
                    ),
                    CustomTextField(
                      maxLength: 4,
                      textInputType: const TextInputType.numberWithOptions(
                          signed: true, decimal: true),
                      fieldName: 'Phone :',
                      height: MediaQuery.of(context).size.height / 16,
                      width: MediaQuery.of(context).size.width / 1.1,
                      controller: _phoneController,
                    ),
                  ],
                ),
              ),
              Padding(
                padding: EdgeInsets.only(
                    left: MediaQuery.of(context).size.width / 12, top: 2),
                child: Row(
                  children: [
                    const Text('Êtes vous un parent ?'),
                    Checkbox(
                      value: isParent,
                      onChanged: (bool? t) {
                        setState(() {
                          isParent = !isParent;
                        });
                      },
                    ),
                    // const Text('Êtes vous un parent ?'),
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
                        // print(isParent);
                        // print(_nniController.text);
                      },
                      child: const Text(
                        'S\'inscrire',
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
