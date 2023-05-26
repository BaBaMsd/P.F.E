# Generated by Django 4.1.7 on 2023-05-24 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0004_remove_certificatvaccination_doses_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccin_Dose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.patient')),
                ('vaccin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.vaccine')),
                ('vaccination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.vaccination')),
            ],
        ),
        migrations.AddField(
            model_name='certificatvaccination',
            name='doses',
            field=models.ManyToManyField(to='utulisateurs.vaccin_dose'),
        ),
    ]
