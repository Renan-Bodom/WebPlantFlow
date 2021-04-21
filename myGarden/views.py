from django.shortcuts import render, redirect
from WebPlantFlow.decorators import validate_session, getSessionUser
from WebPlantFlow.pyrebase_settings import db, auth

# Bancos
bancoJardim = 'myGarden'

# URLs
urlJardim = '/meujardim/'

def myGarden(request):
    data = {}
    data['sistema'] = "Web Plant Flow"
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    #########  Busca plantas já cadastradas pelo usuário
    plantasSalvas = db.child(bancoJardim).child(request.session.get('userId')).get()
    listaPlantas = []
    try:
        for per in plantasSalvas.each():
            listaPlantas.append(per.val())
    except:
        print('Jardim vazio')
    data['listaPlantas'] = listaPlantas

    return render(request, 'myGarden/myGarden.html', data)


def novaPlanta(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    ########### Carrega lista de plantas cadastradas
    loadListaPlantas = db.child('listaPlantas').get()
    listaPlantasBanco = []
    for planta in loadListaPlantas.each():
        listaPlantasBanco.append(planta.val())
    data['listaPlantasBanco'] = listaPlantasBanco

    if request.method == 'POST':
        formApelido    = request.POST.get("apelido", '')
        formNomeCientifico    = request.POST.get("nomeCientifico", '')
        formData    = request.POST.get("data", '')

        formPronto = {"apelido":   formApelido,
                      "nomeCientifico":  formNomeCientifico,
                      "data": formData}
        db.child(bancoJardim).child(request.session.get('userId')).child(formApelido).set(formPronto)

        return redirect(urlJardim)

    return render(request, 'myGarden/novaPlanta.html', data)


def excluirPlanta(request, planta):
    db.child(bancoJardim).child(request.session.get('userId')).child(planta).remove()

    return redirect(urlJardim)


def alterarPlanta(request, planta): # Falta carregar os dados para alterar no template
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    if request.method == 'POST':
        nome        = "nome"
        formNome    = request.POST.get(nome, '')

        formPronto = {"nome":   formNome,
                      "outro":  "Outras informações"}
        db.child(bancoJardim).child(request.session.get('userId')).child(formNome).set(formPronto)

        return redirect(urlJardim)

    return render(request, 'myGarden/novaPlanta.html', data)
