import 'package:flutter/material.dart';

import '../Data/pdf_service.dart';

class VaccinationCard extends StatefulWidget {
  final Color? color;
  const VaccinationCard({
    Key? key,
    this.color,
  }) : super(key: key);

  @override
  State<VaccinationCard> createState() => _VaccinationCardState();
}

class _VaccinationCardState extends State<VaccinationCard> {
  final PdfInvoiceService service = PdfInvoiceService();

  String font = 'JetBrainsMono';
  @override
  Widget build(BuildContext context) {
    return
        // Scaffold(
        //   body:

        Center(
      child: Container(
        decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(30),
            // color: Colors.greenAccent[200],
            color: widget.color ?? Colors.greenAccent[200],
            boxShadow: const [
              BoxShadow(
                blurRadius: 6,
                color: Colors.black26,
                // offset: Offset(2, 2),
              ),
            ]),
        height: MediaQuery.of(context).size.height / 1.5,
        width: MediaQuery.of(context).size.width / 1.09,
        child: Column(
          children: [
            Row(
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Image.asset(
                    'Img/vaccine.png',
                    height: 30,
                  ),
                ),
                const SizedBox(
                  width: 20,
                ),
                Text(
                  'Carte de vaccination',
                  style: TextStyle(
                    fontSize: 20,
                    fontFamily: font,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            SizedBox(
              // color: Colors.purple,
              height: MediaQuery.of(context).size.height / 2,
              width: MediaQuery.of(context).size.width / 1.2,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  FieldSet(
                    title: 'Nom:',
                    content: 'Hello',
                  ),
                  FieldSet(
                    title: 'Nom:',
                    content: 'Hello',
                  ),
                  FieldSet(
                    title: 'Nom:',
                    content: 'Hello',
                  ),
                  FieldSet(
                    title: 'Nom:',
                    content: 'Hello',
                  ),
                ],
              ),
            ),
            Expanded(
                child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: const Icon(Icons.document_scanner),
                    onPressed: () async {
                      // final data = await PdfInvoiceService.createHelloWorld();
                      final data = await service.createHelloWorld();
                      service.savePdfFile('fileName', data);
                    },
                  ),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Image.asset(
                      'Img/qr-code.png',
                      height: 100,
                    ),
                  ),
                  // Text('data'),
                ],
              ),
            )
                // Align(
                //   alignment: Alignment.bottomRight,
                //   child: Padding(
                //     padding: EdgeInsets.all(8.0),
                //     child: Text('data'),
                //   ),
                // ),
                )
          ],
        ),
      ),
    );
    // );
  }
}

class FieldSet extends StatelessWidget {
  String? title;
  String? content;
  FieldSet({
    Key? key,
    this.title,
    this.content,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title ?? ''),
        Text(
          content ?? '',
          style: const TextStyle(fontSize: 30),
        ),
      ],
    );
  }
}
