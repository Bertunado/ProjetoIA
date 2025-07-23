from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pecas, name='lista_pecas'), 
    path('adicionar/', views.adiciona_peca, name='adiciona_peca'),
    path('escolher/', views.escolher_peca, name='escolher_peca'),
    path('lista/<str:tipo_peca>/', views.lista_pecas_filtrada, name='lista_pecas_filtrada'),
    path('chat/', views.chat_peca, name='chat_peca'),
    path('registrar/', views.registrar_peca, name='registrar_peca'),
    path('registrada/', views.peca_registrada, name='peca_registrada'), 
]