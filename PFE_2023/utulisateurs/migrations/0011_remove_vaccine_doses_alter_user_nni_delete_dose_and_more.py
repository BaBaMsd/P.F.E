# Generated by Django 4.1.7 on 2023-04-02 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0010_alter_user_nni'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccine',
            name='doses',
        ),
        migrations.AlterField(
            model_name='user',
            name='nni',
            field=models.CharField(default=0.6587296247160649, max_length=20),
        ),
        migrations.DeleteModel(
            name='Dose',
        ),
        migrations.DeleteModel(
            name='Vaccine',
        ),
    ]