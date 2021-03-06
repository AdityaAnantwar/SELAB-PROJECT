# Generated by Django 3.1.7 on 2021-03-27 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msa_app', '0003_auto_20210327_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(default='default customer', max_length=100)),
                ('customer_number', models.BigIntegerField(null=True)),
                ('amount', models.IntegerField(null=True)),
                ('bill_copy', models.CharField(default='Not available', max_length=50, null=True)),
            ],
            options={
                'db_table': 'bill_data',
            },
        ),
        migrations.RenameField(
            model_name='sales',
            old_name='medicine_ids',
            new_name='medicine_id',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='customer_number',
        ),
    ]
