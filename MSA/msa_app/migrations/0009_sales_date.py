# Generated by Django 3.1.7 on 2021-04-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msa_app', '0008_auto_20210404_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
