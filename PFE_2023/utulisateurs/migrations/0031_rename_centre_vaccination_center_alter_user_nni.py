# Generated by Django 4.1.7 on 2023-04-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0030_alter_user_nni_alter_vaccination_dose_administré_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vaccination',
            old_name='centre',
            new_name='center',
        ),
        migrations.AlterField(
            model_name='user',
            name='nni',
            field=models.CharField(default=0.45291750071799863, max_length=20),
        ),
    ]