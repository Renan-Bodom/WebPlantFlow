from django.urls import path
from . import views

urlpatterns = [
    path('', views.conta, name='url_conta'),
    path('entrar/', views.login),
    path('validar_acesso/', views.valida_senha),
    path('sair/', views.sair),
    path('cadastro/', views.novoCadastro),
    path('removerCadastro/<userRemover>', views.removerCadastro)
]