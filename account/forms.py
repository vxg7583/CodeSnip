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
    fav_coding_lang = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Coding Language'}))
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo','fav_coding_lang',\
                   'headline','email','git_url')
