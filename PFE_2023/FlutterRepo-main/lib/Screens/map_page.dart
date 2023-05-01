import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';

class MapPage extends StatefulWidget {
  const MapPage({super.key});

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  Position? _currentPosition;
  bool isLoading = true;
  // Position _position

  Future<Position> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return Future.error('Location services are disabled.');
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return Future.error('Location permissions are denied');
      }
    }

    if (permission == LocationPermission.deniedForever) {
      return Future.error(
          'Location permissions are permanently denied, we cannot request permissions.');
    }

    final Position position;

    try {
      position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        _currentPosition = position;
      });
    } catch (e) {
      // print(e);
      throw e.toString();
    }

    // print(_currentPosition);

    return position;
  }

  List<Marker> markers = [
    Marker(
      width: 80.0,
      height: 80.0,
      point: LatLng(18.10089, -15.991947409354378),
      builder: (ctx) => const Icon(Icons.location_on),
    ),
    Marker(
      width: 100.0,
      height: 100.0,
      point: LatLng(18.10089, -15.991947409354378),
      builder: (ctx) => const Icon(
        Icons.location_on,
        size: 40,
      ),
    ),
  ];

  @override
  void initState() {
    _determinePosition();

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // floatingActionButton: FloatingActionButton(onPressed: () async {
      //   final p = await _determinePosition();
      //   print(p);
      // }),
      backgroundColor: Colors.white,
      body: _currentPosition == null
          ? const Center(child: CircularProgressIndicator())
          : FlutterMap(
              options: MapOptions(
                center: LatLng(
                  _currentPosition!.latitude,
                  _currentPosition!.longitude,
                ),
                zoom: 8,
              ),
              nonRotatedChildren: [
                AttributionWidget.defaultWidget(
                  source: 'OpenStreetMap contributors',
                  onSourceTapped: null,
                ),
              ],
              children: [
                MarkerLayer(
                  markers: [
                    Marker(
                      point: LatLng(18.10089, -15.991947409354378),
                      width: 80,
                      height: 80,
                      builder: (context) => const Icon(
                        Icons.pin_drop_rounded,
                        size: 100,
                      ),
                    ),
                  ],
                ),
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'com.example.app',
                ),
              ],
            ),
    );
  }
}
