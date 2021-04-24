from django.urls import path
from . import views

urlpatterns = [
    path('', views.myGarden, name='myGarden'),
    path('novaPlanta/', views.novaPlanta),
    path('excluirPlanta/<especiePlantaSelc>/<plantaSelc>', views.excluirPlanta),
    path('alterarPlanta/<especiePlantaSelc>/<plantaSelc>', views.alterarPlanta),
    path('cuidadosPlanta/<especiePlantaSelc>/<plantaSelc>', views.cuidadosPlanta)
]