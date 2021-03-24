from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    data = {}
    data['sistema'] = "Web Plant Flow"
    return render(request, 'index/index.html', data)