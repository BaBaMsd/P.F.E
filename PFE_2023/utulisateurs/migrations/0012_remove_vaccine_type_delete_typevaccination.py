# Generated by Django 4.1.7 on 2023-06-08 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0011_wilaya_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccine',
            name='type',
        ),
        migrations.DeleteModel(
            name='TypeVaccination',
        ),
    ]
