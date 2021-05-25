from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Game(models.Model):
    user_name = models.CharField('User Name', max_length=20)
    gid_8222 = models.CharField('Turkey - Italy', max_length=6)
    gid_8198 = models.CharField('Wales - Switzerland', max_length=6)
    gid_8199 = models.CharField('Denmark - Finland', max_length=6)
    gid_8200 = models.CharField('Belgium - Russia', max_length=6)
    gid_8201 = models.CharField('England - Croatia', max_length=6)
    gid_19950 = models.CharField('Austria - North Macedonia', max_length=6)
    gid_8202 = models.CharField('Netherlands - Ukraine', max_length=6)
    gid_19951 = models.CharField('Scotland - Czech Republic', max_length=6)
    gid_19952 = models.CharField('Poland - Slovakia', max_length=6)
    gid_8203 = models.CharField('Spain - Sweden', max_length=6)
    gid_19949 = models.CharField('Hungary - Portugal', max_length=6)
    gid_8204 = models.CharField('France - Germany', max_length=6)
    gid_8205 = models.CharField('Finland - Russia', max_length=6)
    gid_8206 = models.CharField('Turkey - Wales', max_length=6)
    gid_8207 = models.CharField('Italy - Switzerland', max_length=6)
    gid_19953 = models.CharField('Ukraine - North Macedonia', max_length=6)
    gid_8208 = models.CharField('Denmark - Belgium', max_length=6)
    gid_8209 = models.CharField('Netherlands - Austria', max_length=6)
    gid_19954 = models.CharField('Sweden - Slovakia', max_length=6)
    gid_8210 = models.CharField('Croatia - Czech Republic', max_length=6)
    gid_19955 = models.CharField('England - Scotland', max_length=6)
    gid_19956 = models.CharField('Hungary - France', max_length=6)
    gid_8211 = models.CharField('Portugal - Germany', max_length=6)
    gid_8212 = models.CharField('Spain - Poland', max_length=6)
    gid_8213 = models.CharField('Italy - Wales', max_length=6)
    gid_8214 = models.CharField('Switzerland - Turkey', max_length=6)
    gid_8215 = models.CharField('Ukraine - Austria', max_length=6)
    gid_19957 = models.CharField('North Macedonia - Netherlands', max_length=6)
    gid_8216 = models.CharField('Finland - Belgium', max_length=6)
    gid_8217 = models.CharField('Russia - Denmark', max_length=6)
    gid_8218 = models.CharField('Czech Republic - England', max_length=6)
    gid_19958 = models.CharField('Croatia - Scotland', max_length=6)
    gid_8219 = models.CharField('Sweden - Poland', max_length=6)
    gid_19959 = models.CharField('Slovakia - Spain', max_length=6)
    gid_8220 = models.CharField('Portugal - France', max_length=6)
    gid_19960 = models.CharField('Germany - Hungary', max_length=6)

    def get_absolute_url(self):
        return reverse('home')


class League(models.Model):
    league_name = models.CharField('League Name', max_length=20)
    league_owner = models.CharField('League Manager', max_length=20)
    league_owner_email = models.EmailField('League Manager Email')

    @staticmethod
    def get_absolute_url():
        return reverse('home')


class LeagueUser(models.Model):
    first_name = models.CharField('First Name', max_length=20)
    last_name = models.CharField('Last Name', max_length=20)
    email = models.EmailField('Email')

    @staticmethod
    def get_absolute_url():
        return reverse('home')