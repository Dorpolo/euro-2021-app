# Generated by Django 3.2.3 on 2021-05-31 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210530_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='leagueuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]