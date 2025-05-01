from django.urls import path
from . import views
from .views import StartWhatsappSessionView, SendMessageView, qrcode_view

urlpatterns = [
    path('', views.home, name='home'),

    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),    
    path('login/', views.login_view, name='login_view'),
    path('help/', views.help, name='help'),
    path('salvar-contato/', views.salvar_contato, name='salvar_contato'),
    path('listar-contatos/', views.listar_contatos, name='listar_contatos'),
    path('status/<int:pessoa_id>/', views.status_pessoa, name='status_pessoa'),
    path('start-whatsapp-session/', StartWhatsappSessionView.as_view(), name='start_whatsapp_session'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('qrcode/', qrcode_view, name='qrcode_view'),

]