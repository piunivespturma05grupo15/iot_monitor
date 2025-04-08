from django.db import models

class StatusPessoa(models.Model):
    pessoa_id = models.IntegerField()
    glp = models.IntegerField()
    co2 = models.IntegerField()
    temperatura = models.FloatField()
    posicao = models.CharField(max_length=20)
    saturacao = models.IntegerField()
    localizacao = models.CharField(max_length=50)

    def __str__(self):
        return f"Status Pessoa {self.pessoa_id}"
