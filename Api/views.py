# api/views.py
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
        return Response({
            'glp': 999,
            'co2': 999,
            'temperatura': 999,
            'posicao': "Fail",
            'saturacao': 99,
            'localizacao': "Fail"
        })

@api_view(['POST'])
def post_status_pessoa(request):
    serializer = StatusPessoaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    print("❌ Erros de validação:", serializer.errors)  # 👈 isso deve aparecer no terminal
    return Response(serializer.errors, status=400)