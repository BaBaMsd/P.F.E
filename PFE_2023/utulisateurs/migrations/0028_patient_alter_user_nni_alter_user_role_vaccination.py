# Generated by Django 4.1.7 on 2023-04-13 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0027_alter_admincenter_user_alter_user_nni_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('dateNaissance', models.DateField()),
                ('nni', models.BigIntegerField()),
                ('sexe', models.CharField(choices=[('homme', 'Homme'), ('femme', 'Femme')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='nni',
            field=models.CharField(default=0.5458287541245369, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('directeur-regional', 'Directeur-Regional'), ('responsable-center', 'Responsable-Center'), ('patient', 'Patient'), ('professionnel', 'Professionnel'), ('gerent-stock', 'Gerent-Stock')], default='patient', max_length=20),
        ),
        migrations.CreateModel(
            name='Vaccination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dose_number', models.IntegerField()),
                ('dose_administré', models.IntegerField()),
                ('date_darnier_dose', models.DateField()),
                ('status', models.CharField(choices=[('en_attendant', 'En_Attendant'), ('validé', 'Validé'), ('abondant', 'Abondant')], max_length=20)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='vaccination_qr_codes/')),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.centredevaccination')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.patient')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.vaccine')),
            ],
        ),
    ]
