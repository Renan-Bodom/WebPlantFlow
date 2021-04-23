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
        for plantaUser in plantasSalvas.each():
            planta = plantaUser.val()
            planta['popular'] = db.child('listaPlantas').child(planta['nomeCientifico']).get().val()['popular']
            planta['foto'] = db.child('listaPlantas').child(planta['nomeCientifico']).get().val()['foto']
            planta['info'] = db.child('listaPlantas').child(planta['nomeCientifico']).get().val()['informacoes']
            listaPlantas.append(planta)
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

    return render(request, 'myGarden/novaPlanta.html', data)



def cuidadosPlanta(request, plantaSelc):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #########  Planta do usuário
    plantaUser = db.child(bancoJardim).child(request.session.get('userId')).child(plantaSelc).get()
    data['plantaUsuario'] = plantaUser.val()

    #########  Planta do banco
    plantaBanco = db.child('listaPlantas').child(plantaUser.val()['nomeCientifico']).get()
    data['plantaBanco'] = plantaBanco.val()

    if request.method == 'POST':
        formAgua = request.POST.get("agua", '')
        formSol = request.POST.get("sol", '')

        formPronto = {"agua": formAgua,
                      "sol": formSol}
        db.child(bancoJardim).child(request.session.get('userId')).child(plantaSelc).child('cuidados').set(formPronto)


        return redirect('/meujardim/cuidadosPlanta/'+plantaSelc)

    return render(request, 'myGarden/cuidadosPlanta.html', data)
