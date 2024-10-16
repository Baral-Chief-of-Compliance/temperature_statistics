from django import forms
from temperature_statistics_app.models import Town, Temperature
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


#форма для добавления города
class TownForm(forms.ModelForm):
    class Meta:
        model = Town
        fields = ['t_name']
        widgets = {
            't_name': forms.TextInput(attrs={'class': 'form-control border-secondary','placeholder': 'Название города'}),
        }


#форма для добавления температуры города
class TemperatureForm(forms.ModelForm):
    class Meta:
        model = Temperature
        fields = ['tmp_date', 'tmp_value']
        widgets = {
            'tmp_date': forms.DateTimeInput(attrs={
                'class': 'form-control border-secondary',
                'placeholder': 'Дата и время установки температуры',
                'id': 'date-time-picker'
                }),
            'tmp_value': forms.NumberInput(attrs={
                'class': 'form-control border-secondary',
                'placeholder': 'Значение температуры по Цельсия'
                }),
        }


#форма для получения графика температуры в конкретный день
class DayTemperatureForm(forms.ModelForm):
    class Meta:
        model = Temperature
        fields = ['tmp_date',]
        widgets = {
            'tmp_date': forms.DateTimeInput(attrs={
                'class': 'form-control border-secondary',
                'placeholder': 'Дата анализируемого дня',
                'id': 'date-time-picker'
                })
        }


#форма для авторизации пользователя
class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control border-primary','placeholder': 'Логин'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control border-primary','placeholder':'Пароль'}))
    def confirm_login_allowed(self, user):
        pass