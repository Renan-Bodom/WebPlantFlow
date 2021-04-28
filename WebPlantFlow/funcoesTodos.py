from WebPlantFlow.pyrebase_settings import db, auth

#Calcula media e diferença com a comunidade
def mediaDiferenca(qtdAgua, cuidadosPlantaTodos, plantaUser, itemCuidados):
    mediaQtdAgua = qtdAgua/len(cuidadosPlantaTodos)
    try:
        diferenca = abs(mediaQtdAgua - int(plantaUser.val()['cuidados'][itemCuidados]))
    except:
        diferenca = abs(mediaQtdAgua - 0)

    data = [mediaQtdAgua, diferenca]

    return data

#########  Busca plantas já cadastradas pelo usuário
def plantasDoUsuario(plantasSalvas):
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

    return listaPlantas


def cuidadosTodos (bancoJardim, especiePlantaSelc, cidadeUser):
    jardimTodosUser = db.child(bancoJardim).get()
    plantasDaEspecie = []
    for plantaTodos in jardimTodosUser.each():
        try:
            especiesUsers = plantaTodos.val()[especiePlantaSelc]
            if db.child('users').child(plantaTodos.key()).get().val()['cidade'] == cidadeUser:
                plantasDaEspecie.append(especiesUsers)
            else:
                print('Esse não faz parte da região')
        except:
            print('Este jardineiro não tem essa planta')

    cuidadosPlantaTodos = []
    for dadosPlantaTodos in plantasDaEspecie:
        for apelido in dadosPlantaTodos:
            try:
                cuidadosPlantaTodos.append(dadosPlantaTodos[apelido]['cuidados'])
            except:
                print('Ninguém cuidando dessa planta')

    return cuidadosPlantaTodos


def mensagemAlerta(item, plantaUser):
    mensagem = 'Quantidade de ' + item + ' para ' + plantaUser['popular'] + '(' + plantaUser['apelido'] +')'

    return mensagem