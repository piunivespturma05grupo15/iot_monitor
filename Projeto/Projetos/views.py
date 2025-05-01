from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import pytz
import json, requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Perfil, ApoioContato

@login_required(login_url='login_view')
def home(request):
    perfil = None
    pessoa_id = None

    try:
        perfil = Perfil.objects.get(user=request.user)
        pessoa_id = perfil.id
    except Perfil.DoesNotExist:
        pass

    # Ajustar para fuso horário de Brasília
    fuso_brasilia = pytz.timezone('America/Sao_Paulo')
    hora_atual = timezone.now().astimezone(fuso_brasilia).hour

    if hora_atual < 12:
        saudacao = 'Bom dia'
    elif hora_atual < 18:
        saudacao = 'Boa tarde'
    else:
        saudacao = 'Boa noite'

    return render(request, 'sections/home.html', {
        'perfil': perfil,
        'pessoa_id': pessoa_id,
        'saudacao': saudacao,
        'is_homepage': True,
    })

def cadastro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('qrcode_view')
    else:
        form = CustomUserCreationForm()

    return render(request, 'sections/cadastro_usuario.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Página de destino após o login
            else:
                error_message = "Usuário ou senha incorretos. Por favor, tente novamente."
                return render(request, 'sections/login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Formulário inválido. Por favor, tente novamente."
            return render(request, 'sections/login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()

    return render(request, 'sections/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required(login_url='login_view')
def qrcode_view(request):
    return render(request, 'sections/qrcode.html')

def help(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        numero = request.POST.get('numero')
        tipo_contato = request.POST.get('tipo_contato')

        # Aqui você pode salvar no banco (modelo) ou apenas simular
        print(f"Contato cadastrado: {nome}, {numero}, {tipo_contato}")

        mensagem = "Contato cadastrado com sucesso!"
        return render(request, 'sections/help.html', {'mensagem': mensagem})

    return render(request, 'sections/help.html')

@csrf_exempt
def salvar_contato(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome')
        numero = data.get('numero')
        relacao = data.get('relacao')

        # Salvar no banco
        ApoioContato.objects.create(nome=nome, numero=numero, relacao=relacao)

        # Buscar todos os contatos
        contatos = ApoioContato.objects.all().values()

        # Retornar como JSON
        return JsonResponse({'status': 'ok', 'contatos': list(contatos)})
    
def listar_contatos(request):
    if request.method == 'GET':
        contatos = list(ApoioContato.objects.values())
        return JsonResponse({'status': 'ok', 'contatos': contatos})


@login_required(login_url='login_view')
def status_pessoa(request, pessoa_id):
    try:
        pessoa = Perfil.objects.get(id=pessoa_id)  # Busca a pessoa pelo ID
    except Perfil.DoesNotExist:
        pessoa = None

    contexto = {
        'pessoa_id': pessoa_id,
        'telefone': pessoa.telefone if pessoa else None,  # Passa o número de telefone
        'itens': ["glp", "co2", "temperatura", "posicao", "saturacao", "localizacao"]
    }
    print(f"PESSOA ID: {pessoa_id}, TELEFONE: {contexto['telefone']}")
    return render(request, 'sections/gauge.html', contexto)

class StartWhatsappSessionView(View):
    def get(self, request):
        # Lógica para iniciar a sessão do WhatsApp
        return HttpResponse('Iniciando sessão do WhatsApp')

# Função para enviar mensagem via Node.js
def send_whatsapp_message(to, message):
    url = 'http://localhost:3000/send-message'
    payload = {'to': to, 'message': message}
    
    print(f"[DEBUG] Enviando para {to}: {message}")  # Log da mensagem que está sendo enviada
    
    try:
        response = requests.post(url, json=payload)
        
        # Verificando a resposta e logando o status da requisição
        print(f"[DEBUG] Status da resposta: {response.status_code}")
        print(f"[DEBUG] Resposta do servidor: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] Erro ao enviar a requisição: {e}")
        return False

# View para enviar a mensagem
@method_decorator(csrf_exempt, name='dispatch')
class SendMessageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            numero_destinatario = data.get('to')  # Pode substituir por data['to'] se quiser dinamizar
            mensagem = data.get('message')
            
            if not mensagem:
                return JsonResponse({'status': 'Mensagem não fornecida'}, status=400)

            print(f"[DEBUG] Enviando mensagem para {numero_destinatario}: {mensagem}")  # Log da requisição
            sucesso = send_whatsapp_message(numero_destinatario, mensagem)

            if sucesso:
                return JsonResponse({'status': 'Mensagem enviada com sucesso!'})
            else:
                return JsonResponse({'status': 'Erro ao enviar a mensagem!'}, status=500)

        except Exception as e:
            print(f"[ERROR] Erro no servidor: {str(e)}")  # Log do erro no servidor
            return JsonResponse({'status': 'Erro no servidor', 'error': str(e)}, status=500)