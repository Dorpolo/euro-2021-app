# Generated by Django 3.2.3 on 2021-07-08 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0003_auto_20210622_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='Wales'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='Denmark'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a0_w',
            field=models.CharField(choices=[('Wales', 'Wales'), ('Denmark', 'Denmark')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a1_0',
            field=models.IntegerField(verbose_name='Italy'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a1_1',
            field=models.IntegerField(verbose_name='Austria'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a1_w',
            field=models.CharField(choices=[('Italy', 'Italy'), ('Austria', 'Austria')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a2_0',
            field=models.IntegerField(verbose_name='Netherlands'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a2_1',
            field=models.IntegerField(verbose_name='Czech Republic'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a2_w',
            field=models.CharField(choices=[('Netherlands', 'Netherlands'), ('Czech Republic', 'Czech Republic')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a3_0',
            field=models.IntegerField(verbose_name='Belgium'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a3_1',
            field=models.IntegerField(verbose_name='Portugal'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a3_w',
            field=models.CharField(choices=[('Belgium', 'Belgium'), ('Portugal', 'Portugal')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a4_0',
            field=models.IntegerField(verbose_name='Croatia'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a4_1',
            field=models.IntegerField(verbose_name='Spain'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a4_w',
            field=models.CharField(choices=[('Croatia', 'Croatia'), ('Spain', 'Spain')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a5_0',
            field=models.IntegerField(verbose_name='France'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a5_1',
            field=models.IntegerField(verbose_name='Switzerland'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a5_w',
            field=models.CharField(choices=[('France', 'France'), ('Switzerland', 'Switzerland')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a6_0',
            field=models.IntegerField(verbose_name='England'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a6_1',
            field=models.IntegerField(verbose_name='Germany'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a6_w',
            field=models.CharField(choices=[('England', 'England'), ('Germany', 'Germany')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a7_0',
            field=models.IntegerField(verbose_name='Sweden'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a7_1',
            field=models.IntegerField(verbose_name='Ukraine'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a7_w',
            field=models.CharField(choices=[('Sweden', 'Sweden'), ('Ukraine', 'Ukraine')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop2',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='Italy'),
        ),
        migrations.AlterField(
            model_name='gametop2',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='England'),
        ),
        migrations.AlterField(
            model_name='gametop2',
            name='gid_a0_w',
            field=models.CharField(choices=[('Italy', 'Italy'), ('England', 'England')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='Italy'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='Spain'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a0_w',
            field=models.CharField(choices=[('Italy', 'Italy'), ('Spain', 'Spain')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a1_0',
            field=models.IntegerField(verbose_name='England'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a1_1',
            field=models.IntegerField(verbose_name='Denmark'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a1_w',
            field=models.CharField(choices=[('England', 'England'), ('Denmark', 'Denmark')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='Switzerland'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='Spain'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a0_w',
            field=models.CharField(choices=[('Switzerland', 'Switzerland'), ('Spain', 'Spain')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a1_0',
            field=models.IntegerField(verbose_name='Belgium'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a1_1',
            field=models.IntegerField(verbose_name='Italy'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a1_w',
            field=models.CharField(choices=[('Belgium', 'Belgium'), ('Italy', 'Italy')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a2_0',
            field=models.IntegerField(verbose_name='Czech Republic'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a2_1',
            field=models.IntegerField(verbose_name='Denmark'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a2_w',
            field=models.CharField(choices=[('Czech Republic', 'Czech Republic'), ('Denmark', 'Denmark')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a3_0',
            field=models.IntegerField(verbose_name='Ukraine'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a3_1',
            field=models.IntegerField(verbose_name='England'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a3_w',
            field=models.CharField(choices=[('Ukraine', 'Ukraine'), ('England', 'England')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('league_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.league', to_field='league_name')),
                ('user_name', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]