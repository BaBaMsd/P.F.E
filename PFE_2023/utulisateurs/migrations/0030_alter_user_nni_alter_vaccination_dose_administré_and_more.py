# Generated by Django 4.1.7 on 2023-04-17 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0029_alter_patient_nni_alter_user_nni_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nni',
            field=models.CharField(default=0.4965645396593843, max_length=20),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='dose_administré',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='dose_number',
            field=models.IntegerField(default=0),
        ),
    ]
