from django.shortcuts import render
from WebPlantFlow.decorators import validate_session, getSessionUser
from WebPlantFlow.pyrebase_settings import db, auth
from WebPlantFlow.funcoesTodos import mediaDiferenca, plantasDoUsuario, cuidadosTodos, mensagemAlerta

# Bancos
bancoJardim = 'myGarden'

@validate_session
def alertas(request):
    data = {}
    data['sistema'] = "WebPlantFlow"
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #########  Busca plantas já cadastradas pelo usuário
    plantasSalvas = db.child(bancoJardim).child(request.session.get('userId')).get()
    listaPlantas = plantasDoUsuario(plantasSalvas)

    mostrarAlertas = []
    for plantaUser in listaPlantas:
        #########  Encontrar alertas para as plantas
        try:
            cuidadosPlantaTodos = cuidadosTodos(bancoJardim, plantaUser['nomeCientifico'], request.session.get('cidadeUsuario'))

            qtdAgua = 0
            qtdSol = 0
            for medir in cuidadosPlantaTodos:
                qtdAgua = qtdAgua + int(medir['agua'])
                qtdSol = qtdSol + int(medir['sol'])

            # Tentar reduzir custo computacional na linha de baixo!
            plantaUser2 = db.child(bancoJardim).child(request.session.get('userId')).child(plantaUser['nomeCientifico']).child(plantaUser['apelido']).get()

            agua = mediaDiferenca(qtdAgua, cuidadosPlantaTodos, plantaUser2, 'agua')
            if agua[1] > 20:
                mostrarAlertas.append(mensagemAlerta('água', plantaUser))

            sol = mediaDiferenca(qtdSol, cuidadosPlantaTodos, plantaUser2, 'sol')
            if sol[1] > 1:
                mostrarAlertas.append(mensagemAlerta('sol', plantaUser))


        except:
            print('Não foi possível comparar esta planta')

    data['mostrarAlertas'] = mostrarAlertas

    return render(request, 'alertas/alertas.html', data)