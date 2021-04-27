from django.shortcuts import render, redirect
from WebPlantFlow.decorators import validate_session, getSessionUser
from WebPlantFlow.pyrebase_settings import db, auth
from WebPlantFlow.funcoesTodos import mediaDiferenca, plantasDoUsuario, cuidadosTodos

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
    plantasSalvas   = db.child(bancoJardim).child(request.session.get('userId')).get()
    data['listaPlantas'] = plantasDoUsuario(plantasSalvas)

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
        db.child(bancoJardim).child(request.session.get('userId')).child(formNomeCientifico).child(formApelido).set(formPronto)

        return redirect(urlJardim)

    return render(request, 'myGarden/novaPlanta.html', data)


def excluirPlanta(request, especiePlantaSelc, plantaSelc):
    db.child(bancoJardim).child(request.session.get('userId')).child(especiePlantaSelc).child(plantaSelc).remove()

    return redirect(urlJardim)


def alterarPlanta(request, especiePlantaSelc, plantaSelc): # Falta carregar os dados para alterar no template
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    return render(request, 'myGarden/novaPlanta.html', data)



def cuidadosPlanta(request, especiePlantaSelc, plantaSelc):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #########  Planta do usuário
    plantaUser = db.child(bancoJardim).child(request.session.get('userId')).child(especiePlantaSelc).child(plantaSelc).get()
    data['plantaUsuario'] = plantaUser.val()

    #########  Planta de todos os usuarios
    try:
        cuidadosPlantaTodos = cuidadosTodos(bancoJardim, especiePlantaSelc)

        qtdAgua = 0
        qtdSol = 0
        for medir in cuidadosPlantaTodos:
            qtdAgua = qtdAgua + int(medir['agua'])
            qtdSol = qtdSol + int(medir['sol'])

        agua = mediaDiferenca(qtdAgua, cuidadosPlantaTodos, plantaUser, 'agua')
        data['mediaQtdAgua'] = agua[0]
        data['diferencaQtdAgua'] = agua[1]

        sol = mediaDiferenca(qtdSol, cuidadosPlantaTodos, plantaUser, 'sol')
        data['mediaQtdSol'] = sol[0]
        data['diferencaQtdSol'] = sol[1]

    except:
        data['mediaQtdAgua'] = 0
        data['diferencaQtdAgua'] = 0
        data['mediaQtdSol'] = 0
        data['diferencaQtdSol'] = 0


    #########  Planta do banco
    plantaBanco = db.child('listaPlantas').child(especiePlantaSelc).get()
    data['plantaBanco'] = plantaBanco.val()

    # Formulario de cuidados
    if request.method == 'POST':
        formAgua = request.POST.get("agua", '')
        formSol = request.POST.get("sol", '')

        formPronto = {"agua": formAgua,
                      "sol": formSol}
        db.child(bancoJardim).child(request.session.get('userId')).child(especiePlantaSelc).child(plantaSelc).child('cuidados').set(formPronto)


        return redirect('/meujardim/cuidadosPlanta/'+especiePlantaSelc+'/'+plantaSelc)

    return render(request, 'myGarden/cuidadosPlanta.html', data)
