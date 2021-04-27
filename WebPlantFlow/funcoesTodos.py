from WebPlantFlow.pyrebase_settings import db, auth

#Calcula media e diferença com a comunidade
def mediaDiferenca(qtdAgua, cuidadosPlantaTodos, plantaUser):
    mediaQtdAgua = qtdAgua/len(cuidadosPlantaTodos)
    try:
        diferenca = abs(mediaQtdAgua - int(plantaUser.val()['cuidados']['agua']))
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