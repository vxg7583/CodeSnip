from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username  = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget = forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileEditForm(forms.ModelForm):
    fav_coding_lang = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'eg:python, java'}),
        required=False,
        label='Favorite Coding Language'
    )

    git_url = forms.CharField(
        label='Git URL',
        widget=forms.TextInput(attrs={'placeholder': 'github.com/your-user-name'}),
        required=False
    )

    linkedin_url = forms.CharField(
        label='LinkedIn URL',
        widget=forms.TextInput(attrs={'placeholder': 'linkedin.com/in/your-user-name'}),
        required=False
    )

    favorite_tech_stack = forms.CharField(
        label='Tech Stack',
        widget=forms.TextInput(attrs={'placeholder': 'Django-Postgres-Bootstrap'}),
        required=False
    )



    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo','fav_coding_lang',\
                   'headline','email','git_url','linkedin_url','favorite_tech_stack')
