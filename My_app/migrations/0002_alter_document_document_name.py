# Generated by Django 5.0.2 on 2025-02-20 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_name',
            field=models.CharField(max_length=100),
        ),
    ]
