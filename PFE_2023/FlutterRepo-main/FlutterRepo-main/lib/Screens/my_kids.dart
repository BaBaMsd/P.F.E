import 'package:flutter/material.dart';
import 'package:vaccination/widgets/vaccination_card.dart';

class MyChildrenScreen extends StatefulWidget {
  const MyChildrenScreen({super.key});

  @override
  State<MyChildrenScreen> createState() => _MyChildrenScreenState();
}

class _MyChildrenScreenState extends State<MyChildrenScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // const Text(
            //   'Mes enfants',
            //   style: TextStyle(
            //     fontSize: 30,
            //     fontWeight: FontWeight.bold,
            //     fontFamily: 'JetBrainsMono',
            //     wordSpacing: 1,
            //   ),
            // ),
            Expanded(
              child: PageView(
                scrollDirection: Axis.vertical,
                children: const [
                  VaccinationCard(
                    color: Colors.grey,
                  ),
                  VaccinationCard(
                    color: Colors.red,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
