# Generated by Django 4.1.7 on 2023-05-01 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0034_user_phone_number_alter_user_nni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centredevaccination',
            name='moughataa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.moughataa'),
        ),
    ]
