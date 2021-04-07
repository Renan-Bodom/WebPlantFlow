from django.shortcuts import render
from WebPlantFlow.decorators import validate_session, getSessionUser

# Create your views here.

def myGarden(request):
    data = {}
    data['sistema'] = "Web Plant Flow"
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""
    return render(request, 'myGarden/myGarden.html', data)
