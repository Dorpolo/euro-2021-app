# Generated by Django 3.2.3 on 2021-06-22 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_gametop16_gametop2_gametop4_gametop8'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='AFC Ajax'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='BSC Young Boys'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a0_w',
            field=models.CharField(choices=[('AFC Ajax', 'AFC Ajax'), ('BSC Young Boys', 'BSC Young Boys')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a1_0',
            field=models.IntegerField(verbose_name='FC Dynamo Kyiv'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a1_1',
            field=models.IntegerField(verbose_name='Villarreal CF'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a1_w',
            field=models.CharField(choices=[('FC Dynamo Kyiv', 'FC Dynamo Kyiv'), ('Villarreal CF', 'Villarreal CF')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a2_0',
            field=models.IntegerField(verbose_name='Manchester United'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a2_w',
            field=models.CharField(choices=[('Manchester United', 'Manchester United'), ('AC Milan', 'AC Milan')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a3_1',
            field=models.IntegerField(verbose_name='Rangers FC'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a3_w',
            field=models.CharField(choices=[('SK Slavia Praha', 'SK Slavia Praha'), ('Rangers FC', 'Rangers FC')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a4_0',
            field=models.IntegerField(verbose_name='AS Roma'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a4_1',
            field=models.IntegerField(verbose_name='FC Shakhtar Donetsk'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a4_w',
            field=models.CharField(choices=[('AS Roma', 'AS Roma'), ('FC Shakhtar Donetsk', 'FC Shakhtar Donetsk')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a5_0',
            field=models.IntegerField(verbose_name='Granada CF'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a5_1',
            field=models.IntegerField(verbose_name='Molde FK'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a5_w',
            field=models.CharField(choices=[('Granada CF', 'Granada CF'), ('Molde FK', 'Molde FK')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a6_1',
            field=models.IntegerField(verbose_name='Arsenal FC'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a6_w',
            field=models.CharField(choices=[('Olympiacos FC', 'Olympiacos FC'), ('Arsenal FC', 'Arsenal FC')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a7_0',
            field=models.IntegerField(verbose_name='Tottenham Hotspur FC'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a7_1',
            field=models.IntegerField(verbose_name='GNK Dinamo Zagreb'),
        ),
        migrations.AlterField(
            model_name='gametop16',
            name='gid_a7_w',
            field=models.CharField(choices=[('Tottenham Hotspur FC', 'Tottenham Hotspur FC'), ('GNK Dinamo Zagreb', 'GNK Dinamo Zagreb')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop2',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='Villarreal CF'),
        ),
        migrations.AlterField(
            model_name='gametop2',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='Manchester United'),
        ),
        migrations.AlterField(
            model_name='gametop2',
            name='gid_a0_w',
            field=models.CharField(choices=[('Villarreal CF', 'Villarreal CF'), ('Manchester United', 'Manchester United')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='Manchester United'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='AS Roma'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a0_w',
            field=models.CharField(choices=[('Manchester United', 'Manchester United'), ('AS Roma', 'AS Roma')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a1_0',
            field=models.IntegerField(verbose_name='Villarreal CF'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a1_1',
            field=models.IntegerField(verbose_name='Arsenal FC'),
        ),
        migrations.AlterField(
            model_name='gametop4',
            name='gid_a1_w',
            field=models.CharField(choices=[('Villarreal CF', 'Villarreal CF'), ('Arsenal FC', 'Arsenal FC')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a0_0',
            field=models.IntegerField(verbose_name='AFC Ajax'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a0_1',
            field=models.IntegerField(verbose_name='AS Roma'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a0_w',
            field=models.CharField(choices=[('AFC Ajax', 'AFC Ajax'), ('AS Roma', 'AS Roma')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a1_0',
            field=models.IntegerField(verbose_name='Arsenal FC'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a1_1',
            field=models.IntegerField(verbose_name='SK Slavia Praha'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a1_w',
            field=models.CharField(choices=[('Arsenal FC', 'Arsenal FC'), ('SK Slavia Praha', 'SK Slavia Praha')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a2_0',
            field=models.IntegerField(verbose_name='GNK Dinamo Zagreb'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a2_1',
            field=models.IntegerField(verbose_name='Villarreal CF'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a2_w',
            field=models.CharField(choices=[('GNK Dinamo Zagreb', 'GNK Dinamo Zagreb'), ('Villarreal CF', 'Villarreal CF')], max_length=40, verbose_name='Winning Team'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a3_0',
            field=models.IntegerField(verbose_name='Granada CF'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a3_1',
            field=models.IntegerField(verbose_name='Manchester United'),
        ),
        migrations.AlterField(
            model_name='gametop8',
            name='gid_a3_w',
            field=models.CharField(choices=[('Granada CF', 'Granada CF'), ('Manchester United', 'Manchester United')], max_length=40, verbose_name='Winning Team'),
        ),
    ]