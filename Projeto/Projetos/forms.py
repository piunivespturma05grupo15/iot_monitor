from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil
import re

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Usuário (Login)", 
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nome_monitorado = forms.CharField(
        label="Nome do Monitorado", 
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    idade = forms.CharField(
        label="Idade", 
        max_length=3, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    endereco = forms.CharField(
        label="Endereço", 
        max_length=200, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefone = forms.CharField(
        label="Telefone (WhatsApp)", 
        max_length=20, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+55 (DDD) 90000-0000',
            'pattern': r'^\+55\s\(\d{2}\)\s\d{5}-\d{4}$',
            'title': 'Número no formato +55 (DDD) 90000-0000',
        })
    )
    password1 = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirme a Senha", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "nome_monitorado", "idade", "endereco", "telefone")

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
    
    # Remove tudo que não for número
        numero = re.sub(r'\D', '', telefone)

        if not numero.startswith('55'):
            raise forms.ValidationError('Número deve começar com +55.')
    
        if len(numero) != 13:
            raise forms.ValidationError('Número de telefone deve ter 13 dígitos (ex: +55 DDD 9XXXX XXXX).')

        return numero
    
    def save(self, commit=True):
        user = super().save(commit)
        Perfil.objects.create(
            user=user,
            nome_monitorado=self.cleaned_data['nome_monitorado'],
            idade=self.cleaned_data['idade'],
            endereco=self.cleaned_data['endereco'],
            telefone=self.cleaned_data['telefone'],
        )
        return user