# Generated by Django 4.1.7 on 2023-04-03 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0019_alter_user_nni_delete_dose_delete_vaccine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nni',
            field=models.CharField(default=0.19703857787583123, max_length=20),
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('total_doses', models.IntegerField()),
                ('fabricant', models.CharField(max_length=50)),
                ('doses_administrées', models.IntegerField()),
                ('type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='utulisateurs.typevaccination')),
            ],
        ),
        migrations.CreateModel(
            name='Dose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('durée', models.DurationField()),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doses', to='utulisateurs.vaccine')),
            ],
        ),
    ]