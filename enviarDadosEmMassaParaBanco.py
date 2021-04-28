import pandas as pd
from WebPlantFlow.WebPlantFlow.pyrebase_settings import db


# Carrega o banco
csv         = './plantasBrasileiras.csv'
baseDados   = pd.read_csv(csv, sep=',')


print(len(baseDados))
linha = 0
while linha < len(baseDados):
    '''
    print('Popular:', baseDados.loc[linha]['Popular'])
    print('Científico:', baseDados.loc[linha]['Científico'])
    print('Informações:', baseDados.loc[linha]['Informações'])
    print('Foto:', baseDados.loc[linha]['Foto'])
    '''

    dados = {"popular":     baseDados.loc[linha]['Popular'],
             "cientifico":  baseDados.loc[linha]['Científico'],
             "informacoes": baseDados.loc[linha]['Informações'],
             "foto":        baseDados.loc[linha]['Foto']}

    print('Salvando a planta:', baseDados.loc[linha]['Popular'], '...............em um total de', linha, 'plantas.')
    db.child('listaPlantas').child(baseDados.loc[linha]['Científico']).set(dados)

    linha = linha + 1