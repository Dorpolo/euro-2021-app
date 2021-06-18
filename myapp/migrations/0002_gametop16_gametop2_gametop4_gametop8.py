# Generated by Django 3.2.3 on 2021-06-17 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameTop8',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid_a0_0', models.IntegerField(verbose_name='FC Dynamo Kyiv')),
                ('gid_a0_1', models.IntegerField(verbose_name='Club Brugge KV')),
                ('gid_a0_w', models.CharField(choices=[('FC Dynamo Kyiv', 'FC Dynamo Kyiv'), ('Club Brugge KV', 'Club Brugge KV')], max_length=40, verbose_name='Winning Team')),
                ('gid_a0_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a1_0', models.IntegerField(verbose_name='SC Braga')),
                ('gid_a1_1', models.IntegerField(verbose_name='AS Roma')),
                ('gid_a1_w', models.CharField(choices=[('SC Braga', 'SC Braga'), ('AS Roma', 'AS Roma')], max_length=40, verbose_name='Winning Team')),
                ('gid_a1_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a2_0', models.IntegerField(verbose_name='FK Crvena zvezda')),
                ('gid_a2_1', models.IntegerField(verbose_name='AC Milan')),
                ('gid_a2_w', models.CharField(choices=[('FK Crvena zvezda', 'FK Crvena zvezda'), ('AC Milan', 'AC Milan')], max_length=40, verbose_name='Winning Team')),
                ('gid_a2_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a3_0', models.IntegerField(verbose_name='SK Slavia Praha')),
                ('gid_a3_1', models.IntegerField(verbose_name='Leicester City')),
                ('gid_a3_w', models.CharField(choices=[('SK Slavia Praha', 'SK Slavia Praha'), ('Leicester City', 'Leicester City')], max_length=40, verbose_name='Winning Team')),
                ('gid_a3_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameTop4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid_a0_0', models.IntegerField(verbose_name='FC Dynamo Kyiv')),
                ('gid_a0_1', models.IntegerField(verbose_name='Club Brugge KV')),
                ('gid_a0_w', models.CharField(choices=[('FC Dynamo Kyiv', 'FC Dynamo Kyiv'), ('Club Brugge KV', 'Club Brugge KV')], max_length=40, verbose_name='Winning Team')),
                ('gid_a0_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a1_0', models.IntegerField(verbose_name='SC Braga')),
                ('gid_a1_1', models.IntegerField(verbose_name='AS Roma')),
                ('gid_a1_w', models.CharField(choices=[('SC Braga', 'SC Braga'), ('AS Roma', 'AS Roma')], max_length=40, verbose_name='Winning Team')),
                ('gid_a1_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameTop2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid_a0_0', models.IntegerField(verbose_name='FC Dynamo Kyiv')),
                ('gid_a0_1', models.IntegerField(verbose_name='Club Brugge KV')),
                ('gid_a0_w', models.CharField(choices=[('FC Dynamo Kyiv', 'FC Dynamo Kyiv'), ('Club Brugge KV', 'Club Brugge KV')], max_length=40, verbose_name='Winning Team')),
                ('gid_a0_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameTop16',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid_a0_0', models.IntegerField(verbose_name='FC Dynamo Kyiv')),
                ('gid_a0_1', models.IntegerField(verbose_name='Club Brugge KV')),
                ('gid_a0_w', models.CharField(choices=[('FC Dynamo Kyiv', 'FC Dynamo Kyiv'), ('Club Brugge KV', 'Club Brugge KV')], max_length=40, verbose_name='Winning Team')),
                ('gid_a0_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a1_0', models.IntegerField(verbose_name='SC Braga')),
                ('gid_a1_1', models.IntegerField(verbose_name='AS Roma')),
                ('gid_a1_w', models.CharField(choices=[('SC Braga', 'SC Braga'), ('AS Roma', 'AS Roma')], max_length=40, verbose_name='Winning Team')),
                ('gid_a1_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a2_0', models.IntegerField(verbose_name='FK Crvena zvezda')),
                ('gid_a2_1', models.IntegerField(verbose_name='AC Milan')),
                ('gid_a2_w', models.CharField(choices=[('FK Crvena zvezda', 'FK Crvena zvezda'), ('AC Milan', 'AC Milan')], max_length=40, verbose_name='Winning Team')),
                ('gid_a2_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a3_0', models.IntegerField(verbose_name='SK Slavia Praha')),
                ('gid_a3_1', models.IntegerField(verbose_name='Leicester City')),
                ('gid_a3_w', models.CharField(choices=[('SK Slavia Praha', 'SK Slavia Praha'), ('Leicester City', 'Leicester City')], max_length=40, verbose_name='Winning Team')),
                ('gid_a3_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a4_0', models.IntegerField(verbose_name='Wolfsberger AC')),
                ('gid_a4_1', models.IntegerField(verbose_name='Tottenham Hotspur FC')),
                ('gid_a4_w', models.CharField(choices=[('Wolfsberger AC', 'Wolfsberger AC'), ('Tottenham Hotspur FC', 'Tottenham Hotspur FC')], max_length=40, verbose_name='Winning Team')),
                ('gid_a4_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a5_0', models.IntegerField(verbose_name='FC Krasnodar')),
                ('gid_a5_1', models.IntegerField(verbose_name='GNK Dinamo Zagreb')),
                ('gid_a5_w', models.CharField(choices=[('FC Krasnodar', 'FC Krasnodar'), ('GNK Dinamo Zagreb', 'GNK Dinamo Zagreb')], max_length=40, verbose_name='Winning Team')),
                ('gid_a5_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a6_0', models.IntegerField(verbose_name='Olympiacos FC')),
                ('gid_a6_1', models.IntegerField(verbose_name='PSV Eindhoven')),
                ('gid_a6_w', models.CharField(choices=[('Olympiacos FC', 'Olympiacos FC'), ('PSV Eindhoven', 'PSV Eindhoven')], max_length=40, verbose_name='Winning Team')),
                ('gid_a6_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('gid_a7_0', models.IntegerField(verbose_name='Real Sociedad')),
                ('gid_a7_1', models.IntegerField(verbose_name='Manchester United')),
                ('gid_a7_w', models.CharField(choices=[('Real Sociedad', 'Real Sociedad'), ('Manchester United', 'Manchester United')], max_length=40, verbose_name='Winning Team')),
                ('gid_a7_alt', models.CharField(blank=True, max_length=3, verbose_name='Cup Alternative Score')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
