# Generated by Django 3.1.7 on 2021-04-04 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msa_app', '0007_expiredmedicines_medicinestock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='threshold',
        ),
        migrations.AddField(
            model_name='medicinestock',
            name='threshold',
            field=models.IntegerField(default=50, null=True),
        ),
    ]
