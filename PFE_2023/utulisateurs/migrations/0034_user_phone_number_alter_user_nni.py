# Generated by Django 4.1.7 on 2023-04-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utulisateurs', '0033_alter_admincenter_center_alter_user_nni'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='nni',
            field=models.CharField(default='', max_length=20),
        ),
    ]
