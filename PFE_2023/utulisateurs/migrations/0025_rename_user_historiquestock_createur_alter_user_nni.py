# Generated by Django 4.1.7 on 2023-04-05 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0024_rename_quantity_stockvaccins_quantite_alter_user_nni'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historiquestock',
            old_name='user',
            new_name='createur',
        ),
        migrations.AlterField(
            model_name='user',
            name='nni',
            field=models.CharField(default=0.846557149736437, max_length=20),
        ),
    ]
