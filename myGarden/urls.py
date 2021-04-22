from django.urls import path
from . import views

urlpatterns = [
    path('', views.myGarden, name='myGarden'),
    path('novaPlanta/', views.novaPlanta),
    path('excluirPlanta/<planta>', views.excluirPlanta),
    path('alterarPlanta/<planta>', views.alterarPlanta),
    path('cuidadosPlanta/<plantaSelc>', views.cuidadosPlanta)
]