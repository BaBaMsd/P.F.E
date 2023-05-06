import 'package:flutter/material.dart';
import 'package:vaccination/widgets/vaccination_card.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // floatingActionButton: FloatingActionButton(onPressed: () {}),
      backgroundColor: Colors.white,
      body: Column(
        children: const [
          Expanded(
            child: VaccinationCard(),
          ),
        ],
      ),
    );
  }
}
