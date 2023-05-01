import 'package:fluentui_icons/fluentui_icons.dart';
import 'package:flutter/material.dart';
import 'package:vaccination/Screens/map_page.dart';
import 'package:vaccination/Screens/my_kids.dart';

import 'home_page.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  void navigateBottomBar(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  final List<Widget> _pages = const [
    HomePage(),
    MyChildrenScreen(),
    MapPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Vacciné',
          style: TextStyle(
            color: Colors.black,
            fontSize: 30,
            fontFamily: 'JetBrainsMono',
          ),
        ),
        leading: Builder(builder: (context) {
          return IconButton(
            onPressed: () {
              Scaffold.of(context).openDrawer();
            },
            icon: const Icon(
              Icons.menu,
              size: 40,
            ),
          );
        }),
        toolbarHeight: MediaQuery.of(context).size.height / 11,
        foregroundColor: Colors.teal,
        backgroundColor: Colors.white,
        elevation: 0.0,
      ),
      drawer: Drawer(
        width: MediaQuery.of(context).size.width / 1.6,
        child: Container(
          color: Colors.teal[400],
          child: ListView(
            physics: const NeverScrollableScrollPhysics(),
            children: [
              Column(
                children: const [
                  DrawerHeader(
                      child: Icon(
                    Icons.monetization_on,
                    size: 100,
                  )),
                  Text(
                    'state.user.nom',
                  ),
                  SizedBox(
                    height: 20,
                  )
                ],
              ),
              SizedBox(
                // color: Colors.blueGrey,
                height: MediaQuery.of(context).size.height / 1.65,
                child: Container(
                  height: 40,
                  color: Colors.green,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ListTile(
                        onTap: () {
                          debugPrint('Bye');
                        },
                        leading: const Icon(Icons.logout),
                        title: const Text(
                          'Sign out',
                          style: TextStyle(
                            fontSize: 20,
                          ),
                        ),
                      ),
                      ListTile(
                        onTap: () {
                          debugPrint('Bye');
                        },
                        leading: const Icon(Icons.logout),
                        title: const Text(
                          'Sign out',
                          style: TextStyle(
                            fontSize: 20,
                          ),
                        ),
                      ),
                      ListTile(
                        onTap: () {
                          debugPrint('Bye');
                        },
                        leading: const Icon(Icons.logout),
                        title: const Text(
                          'Sign out',
                          style: TextStyle(
                            fontSize: 20,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              ListTile(
                onTap: () {
                  debugPrint('Bye');
                },
                leading: const Icon(Icons.logout),
                title: const Text(
                  'Sign out',
                  style: TextStyle(
                    fontSize: 20,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      backgroundColor: Colors.white,
      bottomNavigationBar: BottomNavigationBar(
        fixedColor: Colors.black,
        elevation: 0.0,
        backgroundColor: Colors.white,
        currentIndex: _selectedIndex,
        onTap: navigateBottomBar,
        items: const [
          BottomNavigationBarItem(
              icon: Icon(FluentSystemIcons.ic_fluent_home_filled),
              label: 'Home'),
          BottomNavigationBarItem(
              icon: Icon(
                FluentSystemIcons.ic_fluent_people_community_filled,
              ),
              label: 'Mes enfants'),
          BottomNavigationBarItem(
              icon: Icon(
                FluentSystemIcons.ic_fluent_map_filled,
              ),
              label: 'Near by centers'),
        ],
      ),
      body: SafeArea(
        bottom: false,
        child: _pages[_selectedIndex],
      ),
    );
  }
}
