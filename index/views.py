from django.shortcuts import render
from WebPlantFlow.decorators import validate_session, getSessionUser


@validate_session
def index(request):
    data = {}
    data['sistema'] = "WebPlantFlow"
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    return render(request, 'index/index.html', data)