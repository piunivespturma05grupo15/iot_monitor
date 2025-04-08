from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, requests

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
import io
import base64
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import ApoioContato

def home(request):
    return render(request, 'sections/home.html')

def cadastro_usuario(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
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
                return redirect('realizados')  # Página de destino após o login
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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home or another page after login
    else:
        form = AuthenticationForm()

    return render(request, 'sections/login.html', {'form': form})

@login_required(login_url='login_view')
def home(request):
    return render(request, 'sections/home.html', {'is_homepage': True})

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

    contexto = {
        'pessoa_id': pessoa_id,
        'itens': ["glp", "co2", "temperatura", "posicao", "saturacao", "localizacao"]
    }
    print(f"PESSSOAAAAAAAAAAAAAA######## ID: {pessoa_id}")
    return render(request, 'sections/gauge.html', contexto)