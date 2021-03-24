from django.shortcuts import render

# Create your views here.

def myGarden(request):
    data = {}
    data['sistema'] = "Web Plant Flow"
    return render(request, 'myGarden/myGarden.html', data)
