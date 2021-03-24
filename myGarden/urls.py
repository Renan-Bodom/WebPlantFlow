from django.urls import path
from . import views

urlpatterns = [
    path('', views.myGarden, name='myGarden'),
]