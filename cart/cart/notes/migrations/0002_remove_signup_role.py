# Generated by Django 3.1.5 on 2021-02-28 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='role',
        ),
    ]
