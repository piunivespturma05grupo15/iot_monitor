# api/views.py
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StatusPessoa
from .serializers import StatusPessoaSerializer

@api_view(['GET'])
def get_status_pessoa(request, pessoa_id):
    status = StatusPessoa.objects.filter(pessoa_id=pessoa_id).last()
    
    if status:
        serializer = StatusPessoaSerializer(status)
        return Response(serializer.data)
    else:
        # Gerar valores simulados
        glp = round(random.uniform(150, 250), 2)
        co2_ppm = random.randint(400, 5000)
        temperatura = round(random.uniform(36.0, 39.0), 1)
        saturacao = random.randint(93, 100)
        posicao = random.choice(['Sentado', 'Deitado', 'Em pé', 'Queda'])
        localizacao = random.choice(['Quarto', 'Sala', 'Cozinha'])

        # Determinar risco de CO2
        if co2_ppm <= 1000:
            co2_status = 'normal'
        elif co2_ppm <= 2000:
            co2_status = 'alerta'
        else:
            co2_status = 'risco'

        return Response({
            'glp': glp,
            'co2': co2_ppm,
            'co2_status': co2_status,  # <- novo campo de risco
            'temperatura': temperatura,
            'saturacao': saturacao,
            'posicao': posicao,
            'localizacao': localizacao
        })

@api_view(['POST'])
def post_status_pessoa(request):
    serializer = StatusPessoaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    print("❌ Erros de validação:", serializer.errors)  # 👈 isso deve aparecer no terminal
    return Response(serializer.errors, status=400)