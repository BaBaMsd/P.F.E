import 'dart:io';
// import 'package:pdf/pdf.dart';
import 'package:flutter/services.dart';
import 'package:open_document/open_document.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:pdf/widgets.dart';

class CustomRow {
  final String itemName;
  final String itemPrice;
  final String amount;
  final String total;
  final String vat;

  CustomRow(this.itemName, this.itemPrice, this.amount, this.total, this.vat);
}

class PdfInvoiceService {
  CustomRow customRow =
      CustomRow('itemName', 'itemPrice', 'amount', 'total', 'vat');
  Future<Uint8List> createHelloWorld() async {
    final fontData =
        await rootBundle.load('fonts/JetBrainsMono-VariableFont_wght.ttf');
    final ttf = Font.ttf(fontData);
    // final customFont = pw.Font.ttf(fontData.buffer.asUint8List());
    final pdf = pw.Document();
    pdf.addPage(
      pw.Page(
        pageFormat: PdfPageFormat.a4,
        build: (pw.Context context) {
          return pw.Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              pw.Text('Chemsdine',
                  style: TextStyle(
                    fontSize: 36,
                    font: ttf,
                  )),
              pw.SizedBox(height: 20),
              pw.Divider(),
              pw.Center(
                child: pw.Text(
                  'hello',
                  style: pw.TextStyle(
                    font: ttf,
                    // font: pw.Font(),
                  ),
                ),
              ),
              pw.Divider(),
            ],
          );
        },
      ),
    );
    return pdf.save();
  }

  Future<void> savePdfFile(String fileName, Uint8List byteList) async {
    final output = await getTemporaryDirectory();
    var filePath = '${output.path}/$fileName.pdf';
    final file = File(filePath);
    await file.writeAsBytes(byteList);
    await OpenDocument.openDocument(filePath: filePath);
  }
}
