# forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'telephone')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        telephone = cleaned_data.get('telephone')

        if not email and not telephone:
            raise ValidationError("Veuillez renseigner un email ou un numéro de téléphone.")

        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'telephone')
