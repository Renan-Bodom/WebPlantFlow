from django.shortcuts import render
from WebPlantFlow.decorators import validate_session, getSessionUser


@validate_session
def alertas(request):
    data = {}
    data['sistema'] = "WebPlantFlow"
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    return render(request, 'alertas/alertas.html', data)