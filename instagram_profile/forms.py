from django import forms
from . import models
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('gender', 'birthday', 'photo')


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('bad password')
        return cd['password1']


class PhotographyForm(forms.ModelForm):
    class Meta:
        model = models.Photography
        fields = ('photo', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'body')
