# Generated by Django 3.2.3 on 2021-06-05 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0017_auto_20210605_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last Name')),
                ('nick_name', models.CharField(max_length=20, verbose_name='Nick Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('league_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.league', to_field='league_name')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]