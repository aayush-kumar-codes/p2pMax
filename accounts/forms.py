import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .utils.helper import validate_binance_keys


class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
  )
  password2 = forms.CharField(
      label=_("Password Confirmation"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
  )

  def clean_telegram_id(self):
        telegram_id = self.cleaned_data['telegram_id']

        if not re.match(r'^@[A-Za-z0-9_]+$', telegram_id):
            raise ValidationError(_('Enter correct telegram id'))

        # Check uniqueness of the telegram_id
        if User.objects.filter(telegram_id=telegram_id).exists():
            raise ValidationError(_('This Telegram ID is already in use'))

        return telegram_id  

  class Meta:
    model = User
    fields = ('email', 'telegram_id')

    widgets = {
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'Email'
      }),
      'telegram_id': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Telegram Id'
      })
    }


class AddBinanceKeyForm(forms.ModelForm):
    #def clean_binance_key(self):
    #    binance_key = self.cleaned_data['binance_key']
    #    if not validate_binance_keys(binance_key):
    #        raise ValidationError(_("Please Enter a valid Binance API Key"))
    #    return binance_key

    class Meta:
        model = User
        fields = ('binance_key', 'secret_key')

        widgets = {
            'binance_key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Binance API Key'
            }),
            'secret_key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Secret Key'
            })
        }
