from rest_framework import serializers
from .models import StatusPessoa

class StatusPessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPessoa
        fields = '__all__'