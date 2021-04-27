from django.shortcuts import render
from WebPlantFlow.decorators import validate_session, getSessionUser
from WebPlantFlow.pyrebase_settings import db, auth

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
    listaPlantas = []
    try:
        listaEspeciePlanta = []
        for especiePlanta in plantasSalvas.each():
            listaEspeciePlanta.append(especiePlanta.val())
        for especieUser in listaEspeciePlanta:
            for plantaUser in especieUser:
                planta = especieUser[plantaUser]
                planta['popular'] = db.child('listaPlantas').child(planta['nomeCientifico']).get().val()['popular']
                planta['foto'] = db.child('listaPlantas').child(planta['nomeCientifico']).get().val()['foto']
                planta['info'] = db.child('listaPlantas').child(planta['nomeCientifico']).get().val()['informacoes']
                listaPlantas.append(planta)
    except:
        print('Jardim vazio')

    mostrarAlertas = []
    for plantaUser in listaPlantas:
        #########  Planta de todos os usuarios
        try:
            jardimTodosUser = db.child(bancoJardim).get()
            plantasDaEspecie = []
            for plantaTodos in jardimTodosUser.each():
                try:
                    plantasDaEspecie.append(plantaTodos.val()[plantaUser['nomeCientifico']])
                except:
                    print('Jardineiros sem esta planta')
            cuidadosPlantaTodos = []
            for dadosPlantaTodos in plantasDaEspecie:
                for nome in dadosPlantaTodos:
                    try:
                        cuidadosPlantaTodos.append(dadosPlantaTodos[nome]['cuidados'])
                    except:
                        print('Ninguém cuidando dessa planta')

            qtdAgua = 0
            qtdSol = 0
            for medir in cuidadosPlantaTodos:
                qtdAgua = qtdAgua + int(medir['agua'])
                qtdSol = qtdSol + int(medir['sol'])

            mediaQtdAgua = qtdAgua / len(cuidadosPlantaTodos)
            data['mediaQtdAgua'] = mediaQtdAgua
            if 30 < abs(mediaQtdAgua - int(plantaUser['cuidados']['agua'])):
                mostrarAlertas.append('Faltando água na planta ' + plantaUser['popular'] + '('+ plantaUser['apelido'] +')')
            else:
                print('Água ok')

            mediaQtdSol = qtdSol / len(cuidadosPlantaTodos)
            data['mediaQtdSol'] = mediaQtdSol
            if 3 < abs(mediaQtdSol - int(plantaUser['cuidados']['sol'])):
                mostrarAlertas.append('Faltando sol na planta ' + plantaUser['apelido'])
            else:
                print('Sol ok')

        except:
            print('Não foi possível comparar esta planta')

    data['mostrarAlertas'] = mostrarAlertas

    return render(request, 'alertas/alertas.html', data)