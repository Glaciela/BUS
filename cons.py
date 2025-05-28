import pandas as pd
import os

linha_atual = 211
dia_mes_atuais = [
    "01/10", "02/10", "03/10", 
    "04/10", "07/10", "08/10", 
    "09/10", "14/10", "15/10", 
    "16/10", "17/10", "18/10", 
    "21/10", "22/10", "23/10", 
    "24/10", "25/10", "29/10", 
    "30/10", "31/10"
    ]
tabelas_atuais = [1,2,3,4]

QTDE_Total = 0

for dia_mes_atual in dia_mes_atuais:
    for tabela_atual in tabelas_atuais:
        print(f'Processando dados para o dia: {dia_mes_atual} e tabela: {tabela_atual}')
        data_ticketing = 'files_data/bilhetagem_eletronica_outubro_2024.csv'

        db = pd.read_csv(data_ticketing, encoding='utf-8-sig', sep=';')

        # Filtragem para linha 
        db = db[db['LINHA'] == linha_atual]

        db = db[db['TABELA'] == tabela_atual]

        db = db[db['DATAHORA'].str.startswith(f'{dia_mes_atual}/2024')]

        # print(db)

        break

        data_travel = 'files_data/relatorio_viagens_nao_monitoradas_outubro_2024.csv'
        dt = pd.read_csv(data_travel, encoding='utf-8-sig', sep=',')

        dt = dt[dt['Linha'] == linha_atual]

        dt = dt[dt['Referência'] == f'{tabela_atual}']

        dt = dt[dt['Dia'] == f'{dia_mes_atual}']

        # print(dt)

        dt['Partida'] = dt['Partida'].str.slice(0, 5)

        dt['Chegada'] = dt['Chegada'].str.slice(0, 5)

        # print(dt)

        # Extrai o horário (HH:MM) de DATAHORA em db
        db['HORARIO'] = db['DATAHORA'].str.split(' ').str[1].str.slice(0, 5)

        # Função para contar quantos horários estão entre Partida e Chegada
        def contar_qtde(row):
            partida = row['Partida']
            chegada = row['Chegada']
            # Considera apenas horários entre partida e chegada (inclusive)
            return db[(db['HORARIO'] >= partida) & (db['HORARIO'] <= chegada)].shape[0]

        dt['QTDE'] = dt.apply(contar_qtde, axis=1)
        # print(dt)

        dt_zero_qtde = dt[dt['QTDE'] == 0]
        print("Quantidade de linhas em dt_zero_qtde:", len(dt_zero_qtde))

        QTDE_Total += len(dt_zero_qtde)

print("Quantidade de linhas em QTDE_Total:", QTDE_Total)
