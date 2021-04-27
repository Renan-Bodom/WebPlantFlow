def mediaDiferenca(qtdAgua, cuidadosPlantaTodos, plantaUser):
    mediaQtdAgua = qtdAgua/len(cuidadosPlantaTodos)
    try:
        diferenca = abs(mediaQtdAgua - int(plantaUser.val()['cuidados']['agua']))
    except:
        diferenca = abs(mediaQtdAgua - 0)

    data = [mediaQtdAgua, diferenca]

    return data