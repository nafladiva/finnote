from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput

from .models import *

# forms untuk menghandle form - form yang digunakan di app nya
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['nama', 'jenis_transaksi', 'jumlah', 'date']

class TanggunganForm(forms.ModelForm):
    class Meta:
        model = Tanggungan
        fields = ['nama', 'jumlah']

class SaldoUserForm(forms.ModelForm):
    class Meta:
        model = SaldoUser
        fields = ['current_saldo']
        
        def save_model(self, request, obj, form, change):
            obj.user_id = request.user
            super().save_model(request, obj, form, change)