from django.urls import path
from . import views

urlpatterns = [
    path('', views.alertas, name='url_alertas'),
]