# Generated by Django 3.2.3 on 2021-05-27 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league_name', models.CharField(max_length=20, unique=True, verbose_name='League Name')),
                ('league_owner_email', models.EmailField(blank=True, max_length=254, verbose_name='League Manager Email')),
                ('league_owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('league_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.league', to_field='league_name')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid_8222_0', models.IntegerField(verbose_name='Turkey')),
                ('gid_8222_1', models.IntegerField(verbose_name='Italy')),
                ('gid_8198_0', models.IntegerField(verbose_name='Wales')),
                ('gid_8198_1', models.IntegerField(verbose_name='Switzerland')),
                ('gid_8206_0', models.IntegerField(verbose_name='Turkey')),
                ('gid_8206_1', models.IntegerField(verbose_name='Wales')),
                ('gid_8207_0', models.IntegerField(verbose_name='Italy')),
                ('gid_8207_1', models.IntegerField(verbose_name='Switzerland')),
                ('gid_8213_0', models.IntegerField(verbose_name='Italy')),
                ('gid_8213_1', models.IntegerField(verbose_name='Wales')),
                ('gid_8214_0', models.IntegerField(verbose_name='Switzerland')),
                ('gid_8214_1', models.IntegerField(verbose_name='Turkey')),
                ('gid_8199_0', models.IntegerField(verbose_name='Denmark')),
                ('gid_8199_1', models.IntegerField(verbose_name='Finland')),
                ('gid_8200_0', models.IntegerField(verbose_name='Belgium')),
                ('gid_8200_1', models.IntegerField(verbose_name='Russia')),
                ('gid_8205_0', models.IntegerField(verbose_name='Finland')),
                ('gid_8205_1', models.IntegerField(verbose_name='Russia')),
                ('gid_8208_0', models.IntegerField(verbose_name='Denmark')),
                ('gid_8208_1', models.IntegerField(verbose_name='Belgium')),
                ('gid_8216_0', models.IntegerField(verbose_name='Finland')),
                ('gid_8216_1', models.IntegerField(verbose_name='Belgium')),
                ('gid_8217_0', models.IntegerField(verbose_name='Russia')),
                ('gid_8217_1', models.IntegerField(verbose_name='Denmark')),
                ('gid_19950_0', models.IntegerField(verbose_name='Austria')),
                ('gid_19950_1', models.IntegerField(verbose_name='North Macedonia')),
                ('gid_8202_0', models.IntegerField(verbose_name='Netherlands')),
                ('gid_8202_1', models.IntegerField(verbose_name='Ukraine')),
                ('gid_19953_0', models.IntegerField(verbose_name='Ukraine')),
                ('gid_19953_1', models.IntegerField(verbose_name='North Macedonia')),
                ('gid_8209_0', models.IntegerField(verbose_name='Netherlands')),
                ('gid_8209_1', models.IntegerField(verbose_name='Austria')),
                ('gid_19957_0', models.IntegerField(verbose_name='North Macedonia')),
                ('gid_19957_1', models.IntegerField(verbose_name='Netherlands')),
                ('gid_8215_0', models.IntegerField(verbose_name='Ukraine')),
                ('gid_8215_1', models.IntegerField(verbose_name='Austria')),
                ('gid_8201_0', models.IntegerField(verbose_name='England')),
                ('gid_8201_1', models.IntegerField(verbose_name='Croatia')),
                ('gid_19951_0', models.IntegerField(verbose_name='Scotland')),
                ('gid_19951_1', models.IntegerField(verbose_name='Czech Republic')),
                ('gid_8210_0', models.IntegerField(verbose_name='Croatia')),
                ('gid_8210_1', models.IntegerField(verbose_name='Czech Republic')),
                ('gid_19955_0', models.IntegerField(verbose_name='England')),
                ('gid_19955_1', models.IntegerField(verbose_name='Scotland')),
                ('gid_19958_0', models.IntegerField(verbose_name='Croatia')),
                ('gid_19958_1', models.IntegerField(verbose_name='Scotland')),
                ('gid_8218_0', models.IntegerField(verbose_name='Czech Republic')),
                ('gid_8218_1', models.IntegerField(verbose_name='England')),
                ('gid_19952_0', models.IntegerField(verbose_name='Poland')),
                ('gid_19952_1', models.IntegerField(verbose_name='Slovakia')),
                ('gid_8203_0', models.IntegerField(verbose_name='Spain')),
                ('gid_8203_1', models.IntegerField(verbose_name='Sweden')),
                ('gid_19954_0', models.IntegerField(verbose_name='Sweden')),
                ('gid_19954_1', models.IntegerField(verbose_name='Slovakia')),
                ('gid_8212_0', models.IntegerField(verbose_name='Spain')),
                ('gid_8212_1', models.IntegerField(verbose_name='Poland')),
                ('gid_19959_0', models.IntegerField(verbose_name='Slovakia')),
                ('gid_19959_1', models.IntegerField(verbose_name='Spain')),
                ('gid_8219_0', models.IntegerField(verbose_name='Sweden')),
                ('gid_8219_1', models.IntegerField(verbose_name='Poland')),
                ('gid_19949_0', models.IntegerField(verbose_name='Hungary')),
                ('gid_19949_1', models.IntegerField(verbose_name='Portugal')),
                ('gid_8204_0', models.IntegerField(verbose_name='France')),
                ('gid_8204_1', models.IntegerField(verbose_name='Germany')),
                ('gid_19956_0', models.IntegerField(verbose_name='Hungary')),
                ('gid_19956_1', models.IntegerField(verbose_name='France')),
                ('gid_8211_0', models.IntegerField(verbose_name='Portugal')),
                ('gid_8211_1', models.IntegerField(verbose_name='Germany')),
                ('gid_19960_0', models.IntegerField(verbose_name='Germany')),
                ('gid_19960_1', models.IntegerField(verbose_name='Hungary')),
                ('gid_8220_0', models.IntegerField(verbose_name='Portugal')),
                ('gid_8220_1', models.IntegerField(verbose_name='France')),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
