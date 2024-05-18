import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _typeController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();
  final TextEditingController _urlController = TextEditingController(
      text: 'https://codeone-ksp-traffic-monitoring-site.onrender.com/report');
  Position? _currentPosition;
  String _url =
      'https://codeone-ksp-traffic-monitoring-site.onrender.com/report';

  Future<bool> _handleLocationPermission() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            padding:
                const EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
            dismissDirection: DismissDirection.horizontal,
            content: Row(
              children: [
                Icon(
                  Icons.warning_rounded,
                  color: Colors.red[400],
                  size: 20.0,
                ),
                const SizedBox(
                  width: 20.0,
                ),
                const Text(
                  'Location services are disabled. Please enable the services',
                  style: TextStyle(fontSize: 20.0),
                ),
              ],
            )));
      }
      return false;
    }
    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              padding:
                  const EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
              dismissDirection: DismissDirection.horizontal,
              content: Row(
                children: [
                  Icon(
                    Icons.warning_rounded,
                    color: Colors.red[400],
                    size: 20.0,
                  ),
                  const SizedBox(
                    width: 20.0,
                  ),
                  const Text(
                    'Location permissions are denied',
                    style: TextStyle(fontSize: 20.0),
                  ),
                ],
              )));
        }
        return false;
      }
    }
    if (permission == LocationPermission.deniedForever) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            padding:
                const EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
            dismissDirection: DismissDirection.horizontal,
            content: Row(
              children: [
                Icon(
                  Icons.warning_rounded,
                  color: Colors.red[400],
                  size: 20.0,
                ),
                const SizedBox(
                  width: 20.0,
                ),
                const Text(
                  'Location permissions are permanently denied, we cannot request permissions.',
                  style: TextStyle(fontSize: 20.0),
                ),
              ],
            )));
      }
      return false;
    }
    return true;
  }

  Future<bool> _getCurrentPosition() async {
    final hasPermission = await _handleLocationPermission();
    var success = false;

    if (!hasPermission) return false;
    await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high)
        .then((Position position) {
      success = true;
      setState(() => _currentPosition = position);
    }).catchError((e) {
      debugPrint(e.toString());
      success = false;
    });
    return success;
  }

  Future<void> sendReport(double latitude, double longitude, String type,
      String description) async {
    if (type == "0") {
      type = "Traffic";
    } else if (type == "1") {
      type = "Roadblock";
    } else if (type == "2") {
      type = "Accident";
    } else {
      type = "Traffic";
    }

    final response = await http
        .post(
          Uri.parse(_url),
          headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
          },
          body: jsonEncode(<String, String>{
            'latitude': latitude.toString(),
            'longitude': longitude.toString(),
            'type': type,
            'description': description
          }),
        )
        .timeout(const Duration(seconds: 10))
        .catchError((error) {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            padding:
                const EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
            dismissDirection: DismissDirection.horizontal,
            content: Row(
              children: [
                Icon(
                  Icons.warning_rounded,
                  color: Colors.red[400],
                  size: 20.0,
                ),
                const SizedBox(
                  width: 20.0,
                ),
                const Text(
                  'Unable to access server.',
                  style: TextStyle(fontSize: 20.0),
                ),
              ],
            )));
      }
    });

    if (response.statusCode == 200) {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            padding:
                const EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
            dismissDirection: DismissDirection.horizontal,
            content: Row(
              children: [
                Icon(
                  Icons.check_circle,
                  color: Colors.green[600],
                  size: 20.0,
                ),
                const SizedBox(
                  width: 20.0,
                ),
                const Text(
                  'Alert Raised Successfully!!',
                  style: TextStyle(fontSize: 20.0),
                ),
              ],
            )));
      }
    } else {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            padding:
                const EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
            dismissDirection: DismissDirection.horizontal,
            content: Row(
              children: [
                Icon(
                  Icons.warning_rounded,
                  color: Colors.red[400],
                  size: 20.0,
                ),
                const SizedBox(
                  width: 20.0,
                ),
                const Text(
                  'An Error Occurred. Try Again',
                  style: TextStyle(fontSize: 20.0),
                ),
              ],
            )));
      }
    }
  }

  Future<void> showLoader() {
    return showDialog<void>(
      context: context,
      barrierDismissible: false, // user must tap button!
      builder: (BuildContext context) {
        return const AlertDialog(
            content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Center(
              child: Padding(
                padding: EdgeInsets.all(8.0),
                child: Text("Loading..."),
              ),
            ),
            SizedBox(
                height: 20.0,
                child: AspectRatio(
                    aspectRatio: 1, child: CircularProgressIndicator())),
          ],
        ));
      },
    );
  }

  void _raiseError() {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text(
              'You need to have live location enabled to send report an issue')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
        child: Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const Column(
            children: [
              Center(
                child: Text('Is there any traffic',
                    style: TextStyle(
                      fontSize: 30.0,
                      fontWeight: FontWeight.bold,
                    )),
              ),
              Center(
                child: Text('congestion nearby?',
                    style: TextStyle(
                      fontSize: 30.0,
                      fontWeight: FontWeight.bold,
                    )),
              ),
              SizedBox(
                height: 10.0,
              ),
              Center(
                child: Text('Report it right away!',
                    style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.normal,
                    )),
              ),
            ],
          ),
          ElevatedButton(
            onPressed: () async {
              await showDialog<void>(
                  context: context,
                  builder: (context) => AlertDialog(
                        content: Stack(
                          clipBehavior: Clip.none,
                          children: <Widget>[
                            Positioned(
                              right: -40,
                              top: -40,
                              child: InkResponse(
                                onTap: () {
                                  Navigator.of(context).pop();
                                },
                                child: CircleAvatar(
                                  backgroundColor: Colors.red[200],
                                  child: const Icon(Icons.close),
                                ),
                              ),
                            ),
                            Form(
                              key: _formKey,
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.start,
                                mainAxisSize: MainAxisSize.min,
                                children: <Widget>[
                                  const Padding(
                                    padding: EdgeInsets.all(8),
                                    child: Text("What is the issue?"),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(8),
                                    child: DropdownButtonFormField<int>(
                                      value: 0,
                                      items: const [
                                        DropdownMenuItem(
                                            value: 0, child: Text("Traffic")),
                                        DropdownMenuItem(
                                            value: 1, child: Text("Roadblock")),
                                        DropdownMenuItem(
                                            value: 2, child: Text("Accident")),
                                      ],
                                      onChanged: (int? value) {
                                        _typeController.text = value.toString();
                                      },
                                      decoration: const InputDecoration(
                                        border: OutlineInputBorder(),
                                      ),
                                    ),
                                  ),
                                  const Padding(
                                    padding: EdgeInsets.all(8),
                                    child: Text("Give short description"),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(8),
                                    child: TextFormField(
                                      controller: _descriptionController,
                                      maxLength: 150,
                                      maxLines: 3,
                                      decoration: const InputDecoration(
                                        border: OutlineInputBorder(),
                                      ),
                                    ),
                                  ),
                                  const SizedBox(
                                    height: 10.0,
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(8),
                                    child: Center(
                                      child: ElevatedButton(
                                        child: const Text('Report'),
                                        onPressed: () async {
                                          if (_formKey.currentState!
                                              .validate()) {
                                            _formKey.currentState!.save();
                                            Navigator.of(context).pop();
                                            showLoader();
                                            final positionUpdated =
                                                await _getCurrentPosition();
                                            if (positionUpdated &&
                                                _currentPosition != null) {
                                              await sendReport(
                                                  _currentPosition!.latitude,
                                                  _currentPosition!.longitude,
                                                  _typeController.text,
                                                  _descriptionController.text);
                                            } else {
                                              _raiseError();
                                            }
                                          }
                                        },
                                      ),
                                    ),
                                  )
                                ],
                              ),
                            ),
                          ],
                        ),
                      ));
            },
            style: ElevatedButton.styleFrom(
              shape: const CircleBorder(),
              padding: const EdgeInsets.all(50),
              backgroundColor: Colors.red[300], // Button color
              foregroundColor: Colors.red, // Splash color
            ),
            child: const Icon(
              Icons.warning_rounded,
              color: Colors.white,
              size: 50.0,
            ),
          ),
          TextButton(
            onPressed: () async {
              await showDialog(
                  context: context,
                  builder: (context) => Dialog(
                          child: Padding(
                        padding: const EdgeInsets.all(40.0),
                        child: Form(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(_url),
                              TextFormField(
                                controller: _urlController,
                              ),
                              TextButton(
                                onPressed: () {
                                  setState(() {
                                    _url = _urlController.text;
                                  });
                                  Navigator.of(context).pop();
                                },
                                child: const Text("Update"),
                              )
                            ],
                          ),
                        ),
                      )));
            },
            style: ButtonStyle(
              backgroundColor:
                  WidgetStateProperty.all<Color>(Colors.transparent),
            ),
            child: const Text(
              "Close App",
              style: TextStyle(color: Colors.transparent),
            ),
          ),
        ],
      ),
    ));
  }
}
