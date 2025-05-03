from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_monitorado = models.CharField(max_length=200)
    idade = models.CharField(max_length=3)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_monitorado

class ApoioContato(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='contatos', null=True, blank=True)

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