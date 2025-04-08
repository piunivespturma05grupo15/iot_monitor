from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class ApoioContato(models.Model):
    OPCOES_RELACAO = [
        ('familia', 'Família'),
        ('cuidador', 'Cuidador'),
        ('vizinhos', 'Vizinhos'),
        ('emergencia', 'Serviços de Emergência'),
    ]

    nome = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)
    relacao = models.CharField(max_length=20, choices=OPCOES_RELACAO)

    def __str__(self):
        return f"{self.nome} - {self.relacao}"