# Generated by Django 3.2.3 on 2021-06-01 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20210601_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cleanpredictions',
            name='last_name',
        ),
    ]
