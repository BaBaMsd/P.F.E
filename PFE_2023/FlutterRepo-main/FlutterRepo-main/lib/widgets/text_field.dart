import 'package:flutter/material.dart';

// ignore: must_be_immutable
class CustomTextField extends StatelessWidget {
  String? fieldName;
  final double height;
  final double width;
  int? maxLength;
  TextInputType? textInputType;

  final TextEditingController controller;

  CustomTextField({
    Key? key,
    this.fieldName,
    this.maxLength,
    required this.height,
    required this.width,
    required this.controller,
    this.textInputType,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text(fieldName ?? ''),
        ),
        Container(
          decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              boxShadow: const [
                BoxShadow(
                  blurRadius: 4,
                  offset: Offset(2, 2),
                  color: Colors.black26,
                ),
              ]),
          height: height,
          width: width,
          child: Padding(
            padding: const EdgeInsets.all(12.0),
            child: TextField(
              // maxLengthEnforcement: MaxLengthEnforcement.none,
              // maxLengthEnforcement: MaxLengthEnforcement.enforce,
              maxLength: maxLength,
              keyboardType: textInputType,
              decoration: const InputDecoration(
                border: InputBorder.none,
                counterText: '',
              ),
              autocorrect: false,
              controller: controller,
            ),
          ),
        )
      ],
    );
  }
}
