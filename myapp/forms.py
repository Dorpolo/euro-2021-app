from django import forms
from .models import Game, League, LeagueUser


class BetForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('user_name', 'gid_8222', 'gid_8198', 'gid_8199', 'gid_8200', 'gid_8201', 'gid_19950',
                  'gid_8202', 'gid_19951', 'gid_19952', 'gid_8203', 'gid_19949', 'gid_8204',
                  'gid_8205', 'gid_8206', 'gid_8207', 'gid_19953', 'gid_8208', 'gid_8209',
                  'gid_19954', 'gid_8210', 'gid_19955', 'gid_19956', 'gid_8211', 'gid_8212',
                  'gid_8213', 'gid_8214', 'gid_8215', 'gid_19957', 'gid_8216', 'gid_8217',
                  'gid_8218', 'gid_19958', 'gid_8219', 'gid_19959', 'gid_8220', 'gid_19960')

        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Avi Nimni'}),
            'gid_8222': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8198': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8199': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8200': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8201': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19950': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8202': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19951': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19952': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8203': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19949': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8204': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8205': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8206': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8207': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19953': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8208': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8209': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19954': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8210': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19955': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19956': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8211': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8212': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8213': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8214': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8215': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19957': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8216': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8217': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8218': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19958': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8219': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19959': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_8220': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
            'gid_19960': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: 0-0'}),
        }


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
        fields = ('first_name', 'last_name', 'email', )

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Avi'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: Nimni'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g: tal_banin@gmail.com'}),
        }

    def clean_name(self):
        phone = self.cleaned_data.get("first_name")
        if len(phone) != 2:
            raise forms.ValidationError("Invalid phone number")
        return phone

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("first_name")
        # Custom Validation Logic
        # Here
        return self.cleaned_data
