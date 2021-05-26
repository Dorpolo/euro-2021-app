from django import forms
from .models import Game, League, LeagueUser
from pipelines.read_data import EuroApi

logos = EuroApi().main()


class BetForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = (
            'user_name',
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
            'user_name': forms.Select(attrs={'class': 'form-select', 'placeholder': 'e.g: Avi Nimni'}),
            'gid_8222_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8222_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8198_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8198_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8206_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8206_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8207_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8207_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8213_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8213_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8214_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8214_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),

            'gid_8199_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8199_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8200_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8200_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8205_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8205_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8208_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8208_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8216_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8216_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8217_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8217_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),

            'gid_19950_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19950_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8202_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8202_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19953_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19953_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8209_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8209_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19957_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19957_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8215_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8215_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),

            'gid_8201_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8201_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19951_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19951_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8210_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8210_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19955_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19955_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19958_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19958_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8218_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8218_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),

            'gid_19952_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19952_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8203_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8203_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19954_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19954_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8212_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8212_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19959_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19959_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8219_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8219_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),

            'gid_19949_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19949_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8204_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8204_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19956_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19956_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8211_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8211_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19960_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_19960_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8220_0': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'gid_8220_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }

    def paired_teams(self):
        return [
            [field for field in self if 'gid_8222' in field.name],
            [field for field in self if 'gid_8198' in field.name],
            [field for field in self if 'gid_8206' in field.name],
            [field for field in self if 'gid_8207' in field.name],
            [field for field in self if 'gid_8213' in field.name],
            [field for field in self if 'gid_8214' in field.name],
            [field for field in self if 'gid_8199' in field.name],
            [field for field in self if 'gid_8200' in field.name],
            [field for field in self if 'gid_8205' in field.name],
            [field for field in self if 'gid_8208' in field.name],
            [field for field in self if 'gid_8216' in field.name],
            [field for field in self if 'gid_8217' in field.name],
            [field for field in self if 'gid_19950' in field.name],
            [field for field in self if 'gid_8202' in field.name],
            [field for field in self if 'gid_19953' in field.name],
            [field for field in self if 'gid_8209' in field.name],
            [field for field in self if 'gid_19957' in field.name],
            [field for field in self if 'gid_8215' in field.name],
            [field for field in self if 'gid_8201' in field.name],
            [field for field in self if 'gid_19951' in field.name],
            [field for field in self if 'gid_8210' in field.name],
            [field for field in self if 'gid_19955' in field.name],
            [field for field in self if 'gid_19958' in field.name],
            [field for field in self if 'gid_8218' in field.name],
            [field for field in self if 'gid_19952' in field.name],
            [field for field in self if 'gid_8203' in field.name],
            [field for field in self if 'gid_19954' in field.name],
            [field for field in self if 'gid_8212' in field.name],
            [field for field in self if 'gid_19959' in field.name],
            [field for field in self if 'gid_8219' in field.name],
            [field for field in self if 'gid_19949' in field.name],
            [field for field in self if 'gid_8204' in field.name],
            [field for field in self if 'gid_19956' in field.name],
            [field for field in self if 'gid_8211' in field.name],
            [field for field in self if 'gid_19960' in field.name],
            [field for field in self if 'gid_8220' in field.name],
        ]

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
        fields = ('league_name',)

        widgets = {
            'league_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Avi Nimni'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = LeagueUser
        fields = ('user_name', 'league_name', 'first_name', 'last_name', 'email', )

        widgets = {
            'user_name': forms.Select(attrs={'class': 'form-select', 'placeholder': 'e.g: Avi Nimni'}),
            'league_name': forms.Select(attrs={'class': 'form-select', 'placeholder': 'e.g: Avi Nimni'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Avi'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Nimni'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: tal_banin@gmail.com'}),
        }


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)