from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from data import players


class Game(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    gid_8222_0 = models.IntegerField('Turkey')
    gid_8222_1 = models.IntegerField('Italy')
    gid_8198_0 = models.IntegerField('Wales')
    gid_8198_1 = models.IntegerField('Switzerland')
    gid_8206_0 = models.IntegerField('Turkey')
    gid_8206_1 = models.IntegerField('Wales')
    gid_8207_0 = models.IntegerField('Italy')
    gid_8207_1 = models.IntegerField('Switzerland')
    gid_8213_0 = models.IntegerField('Italy')
    gid_8213_1 = models.IntegerField('Wales')
    gid_8214_0 = models.IntegerField('Switzerland')
    gid_8214_1 = models.IntegerField('Turkey')
    gid_8199_0 = models.IntegerField('Denmark')
    gid_8199_1 = models.IntegerField('Finland')
    gid_8200_0 = models.IntegerField('Belgium')
    gid_8200_1 = models.IntegerField('Russia')
    gid_8205_0 = models.IntegerField('Finland')
    gid_8205_1 = models.IntegerField('Russia')
    gid_8208_0 = models.IntegerField('Denmark')
    gid_8208_1 = models.IntegerField('Belgium')
    gid_8216_0 = models.IntegerField('Finland')
    gid_8216_1 = models.IntegerField('Belgium')
    gid_8217_0 = models.IntegerField('Russia')
    gid_8217_1 = models.IntegerField('Denmark')
    gid_19950_0 = models.IntegerField('Austria')
    gid_19950_1 = models.IntegerField('North Macedonia')
    gid_8202_0 = models.IntegerField('Netherlands')
    gid_8202_1 = models.IntegerField('Ukraine')
    gid_19953_0 = models.IntegerField('Ukraine')
    gid_19953_1 = models.IntegerField('North Macedonia')
    gid_8209_0 = models.IntegerField('Netherlands')
    gid_8209_1 = models.IntegerField('Austria')
    gid_19957_0 = models.IntegerField('North Macedonia')
    gid_19957_1 = models.IntegerField('Netherlands')
    gid_8215_0 = models.IntegerField('Ukraine')
    gid_8215_1 = models.IntegerField('Austria')
    gid_8201_0 = models.IntegerField('England')
    gid_8201_1 = models.IntegerField('Croatia')
    gid_19951_0 = models.IntegerField('Scotland')
    gid_19951_1 = models.IntegerField('Czech Republic')
    gid_8210_0 = models.IntegerField('Croatia')
    gid_8210_1 = models.IntegerField('Czech Republic')
    gid_19955_0 = models.IntegerField('England')
    gid_19955_1 = models.IntegerField('Scotland')
    gid_19958_0 = models.IntegerField('Croatia')
    gid_19958_1 = models.IntegerField('Scotland')
    gid_8218_0 = models.IntegerField('Czech Republic')
    gid_8218_1 = models.IntegerField('England')
    gid_19952_0 = models.IntegerField('Poland')
    gid_19952_1 = models.IntegerField('Slovakia')
    gid_8203_0 = models.IntegerField('Spain')
    gid_8203_1 = models.IntegerField('Sweden')
    gid_19954_0 = models.IntegerField('Sweden')
    gid_19954_1 = models.IntegerField('Slovakia')
    gid_8212_0 = models.IntegerField('Spain')
    gid_8212_1 = models.IntegerField('Poland')
    gid_19959_0 = models.IntegerField('Slovakia')
    gid_19959_1 = models.IntegerField('Spain')
    gid_8219_0 = models.IntegerField('Sweden')
    gid_8219_1 = models.IntegerField('Poland')
    gid_19949_0 = models.IntegerField('Hungary')
    gid_19949_1 = models.IntegerField('Portugal')
    gid_8204_0 = models.IntegerField('France')
    gid_8204_1 = models.IntegerField('Germany')
    gid_19956_0 = models.IntegerField('Hungary')
    gid_19956_1 = models.IntegerField('France')
    gid_8211_0 = models.IntegerField('Portugal')
    gid_8211_1 = models.IntegerField('Germany')
    gid_19960_0 = models.IntegerField('Germany')
    gid_19960_1 = models.IntegerField('Hungary')
    gid_8220_0 = models.IntegerField('Portugal')
    gid_8220_1 = models.IntegerField('France')
    top_scorer_1 = models.CharField('Scorer I', max_length=100, choices=players.PLAYER_LIST, blank=True)
    top_scorer_2 = models.CharField('Scorer II', max_length=100, choices=players.PLAYER_LIST, blank=True)
    top_scorer_3 = models.CharField('Scorer III', max_length=100, choices=players.PLAYER_LIST, blank=True)
    top_assist_1 = models.CharField('Assists I', max_length=100, choices=players.PLAYER_LIST, blank=True)
    top_assist_2 = models.CharField('Assists II', max_length=100, choices=players.PLAYER_LIST, blank=True)
    top_assist_3 = models.CharField('Assists III', max_length=100, choices=players.PLAYER_LIST, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    # @staticmethod
    # def get_absolute_url():
    #     return reverse('home')


class League(models.Model):
    league_name = models.CharField('League Name', max_length=20, unique=True)
    league_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_absolute_url():
        return reverse('home')


class LeagueUser(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    league_name = models.ForeignKey(League, to_field='league_name', on_delete=models.CASCADE)
    first_name = models.CharField('First Name', max_length=20)
    last_name = models.CharField('Last Name', max_length=20)
    email = models.EmailField('Email')
    image = models.ImageField(null=True, blank=True, upload_to="images")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_absolute_url():
        return reverse('home')


class CleanPredictions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_full_name = models.CharField('User', max_length=100)
    league_name = models.ForeignKey(League, to_field='league_name', on_delete=models.CASCADE)
    match_label = models.CharField('Match', max_length=100)
    predicted_score = models.CharField('Predicted Score', max_length=100)
    real_score = models.CharField('Real Score', max_length=100)
    game_status = models.CharField('Game Status', max_length=100)
    date = models.DateField('Date', max_length=100)
    hour = models.TimeField('Hour', max_length=100)
    pred_score_home = models.IntegerField('Predicted Score Home')
    pred_score_away = models.IntegerField('Predicted Score Away')
    real_score_home = models.IntegerField('Real Score Home')
    real_score_away = models.IntegerField('Real Score Away')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


