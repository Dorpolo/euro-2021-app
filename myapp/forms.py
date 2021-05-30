from django import forms
from django.db import models
from .models import Game, League, LeagueUser, Post
from pipelines.read_data import EuroApi
from data.teams import team_game_map

logos = EuroApi().main()


class BetForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = (
            'gid_8222_0', 'gid_8222_1',
            'gid_8198_0', 'gid_8198_1',
            'gid_8206_0', 'gid_8206_1',
            'gid_8207_0', 'gid_8207_1',
            'gid_8213_0', 'gid_8213_1',
            'gid_8214_0', 'gid_8214_1',
            'gid_8199_0', 'gid_8199_1',
            'gid_8200_0', 'gid_8200_1',
            'gid_8205_0', 'gid_8205_1',
            'gid_8208_0', 'gid_8208_1',
            'gid_8216_0', 'gid_8216_1',
            'gid_8217_0', 'gid_8217_1',
            'gid_19950_0', 'gid_19950_1',
            'gid_8202_0', 'gid_8202_1',
            'gid_19953_0', 'gid_19953_1',
            'gid_8209_0', 'gid_8209_1',
            'gid_19957_0', 'gid_19957_1',
            'gid_8215_0', 'gid_8215_1',
            'gid_8201_0', 'gid_8201_1',
            'gid_19951_0', 'gid_19951_1',
            'gid_8210_0', 'gid_8210_1',
            'gid_19955_0', 'gid_19955_1',
            'gid_19958_0', 'gid_19958_1',
            'gid_8218_0', 'gid_8218_1',
            'gid_19952_0', 'gid_19952_1',
            'gid_8203_0', 'gid_8203_1',
            'gid_19954_0', 'gid_19954_1',
            'gid_8212_0', 'gid_8212_1',
            'gid_19959_0', 'gid_19959_1',
            'gid_8219_0', 'gid_8219_1',
            'gid_19949_0', 'gid_19949_1',
            'gid_8204_0', 'gid_8204_1',
            'gid_19956_0', 'gid_19956_1',
            'gid_8211_0', 'gid_8211_1',
            'gid_19960_0', 'gid_19960_1',
            'gid_8220_0', 'gid_8220_1',
        )

        widgets = {
            'gid_8222_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8222_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8198_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8198_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8206_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8206_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8207_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8207_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8213_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8213_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8214_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8214_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),

            'gid_8199_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8199_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8200_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8200_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8205_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8205_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8208_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8208_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8216_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8216_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8217_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8217_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),

            'gid_19950_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19950_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8202_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8202_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19953_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19953_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8209_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8209_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19957_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19957_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8215_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8215_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),

            'gid_8201_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8201_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19951_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19951_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8210_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8210_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19955_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19955_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19958_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19958_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8218_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8218_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),

            'gid_19952_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19952_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8203_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8203_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19954_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19954_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8212_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8212_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19959_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19959_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8219_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8219_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),

            'gid_19949_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19949_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8204_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8204_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19956_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19956_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8211_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8211_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19960_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_19960_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8220_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'gid_8220_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '-'}),
        }

    def more_data(self):
        sorted_fixtures = logos
        data = [
            list(
                set([item[8] for item in sorted_fixtures if item[2] == f'Group {group}'])
            ) for group in ['A', 'B', 'C', 'D', 'E', 'F']]
        return data


class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ('league_name', 'league_owner', 'league_owner_email')

        widgets = {
            'league_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Avi Nimni'}),
            'league_owner': forms.Select(attrs={'class': 'form-select', 'placeholder': 'e.g: Avi Nimni'}),
            'league_owner_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = LeagueUser
        fields = ('league_name', 'first_name', 'last_name', 'email', )

        widgets = {
            'league_name': forms.Select(attrs={'class': 'form-select', 'placeholder': 'e.g: Avi Nimni'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Avi'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Nimni'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: tal_banin@gmail.com'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'author']
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'post-text',
                'required': True,
                'placeholder': 'Say something...'
            }),
            'author': forms.Select(attrs={
                'id': 'post-text',
                'required': True,
                'placeholder': 'Say something...'
            })
        }