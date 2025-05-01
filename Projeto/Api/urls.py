from django.urls import path
from . import views

urlpatterns = [
    path('status/<int:pessoa_id>/', views.get_status_pessoa),
    path('status/', views.post_status_pessoa),
]