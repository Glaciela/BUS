# Este script processa os dados 
# De viagens de ônibus não monitoradas 
# Compara com dados da bilhetagem
# E gera arquivos CSV por linha e dia útil
# Com a quantidade de bilhetes 
# Em linha e dia específico

import pandas as pd 
import os

# Função para retornar verdadeiro
# Se a variável dayhours estiver no intervalo
# Entre match e arrival
# No mesmo dia e ano
# Senão retorna falso
def compare_dates_hours(day, match, arrival, dayhour):
    dayt = day
    dayt = f"{dayt}/2024"
    matcht = match
    arrivalt = arrival
    # Remove os segundos da hora de chegada (arrivalt)
    if len(arrivalt.split(':')) == 3:
        arrivalt = ':'.join(arrivalt.split(':')[:2])

    # Separa a data e hora
    dayb = dayhour.split(' ')[0]
    hourb = dayhour.split(' ')[1]

    if dayt == dayb and matcht <= hourb <= arrivalt:
        return True
    else:
        return False

# Função para retornar a quantidade de bilhetes
# Que está no arquivo de bilhetagem (tickets)
# Para determinada linha, dia e horário
def qtde_tickets(line, tickets, day, match, arrival):
    qtde = 0
    for i in range(tickets.shape[0]):
        ticket_line = tickets['LINHA'].iloc[i]
        ticket_dayhours = tickets['DATAHORA'].iloc[i]
        if ticket_line == line and compare_dates_hours(day, match, arrival, ticket_dayhours):
            qtde += 1
    return qtde


# Armazena em uma variável as viagens não monitoradas
data_travel = 'files_data/relatorio_viagens_nao_monitoradas_outubro_2024.csv'
dt = pd.read_csv(data_travel, encoding='utf-8-sig', sep=',')

# Armazena em uma variável a bilhetagem
data_ticketing = 'files_data/bilhetagem_eletronica_outubro_2024.csv'
db = pd.read_csv(data_ticketing, encoding='utf-8-sig', sep=';')

# Armazena em uma variável as linhas de ônibus
unique_lines = dt['Linha'].unique().tolist()

# Cria um diretório para a linha, se não existir
# Em 'files_data/LineBus'
for line in unique_lines:
    line_dir = f'files_data/LineBus/{line}'
    if not os.path.exists(line_dir):
        os.makedirs(line_dir)

# Lista de dias úteis de outubro de 2024
business_days_out_2024 = [
    "01/10", "02/10", "03/10", 
    "04/10", "07/10", "08/10", 
    "09/10", "14/10", "15/10", 
    "16/10", "17/10", "18/10", 
    "21/10", "22/10", "23/10", 
    "24/10", "25/10", "29/10", 
    "30/10", "31/10"
    ]

# Filtra os dados para incluir apenas os dias úteis
# Em cada pasta contendo o número da linha
# Vai existir um arquivo para cada dia útil
for day in business_days_out_2024:
    print(f'Processando dados para o dia: {day}')
    # O processamento é feito por dia útil
    # Linha por linha
    for line in unique_lines:

        # Armazena em uma variável as viagens não monitoradas
        dt = pd.read_csv(data_travel, encoding='utf-8-sig', sep=',')
        # Armazena em uma variável a bilhetagem
        db = pd.read_csv(data_ticketing, encoding='utf-8-sig', sep=';')
            
        # Filtra os dados das viagens não monitoradas
        # Apenas com a linha e o dia do laço for
        dt = dt[(dt['Linha'] == line) & (dt['Dia'] == day)]

        # Filtra os dados da bilhetagem
        # Apenas com a linha e o dia do laço for
        db = db[(db['LINHA'] == line) & (db['DATAHORA'].str.startswith(day))]
        
        # Aplica a função para cada linha do arquivo 
        # Acrescentando uma nova coluna com a quantidade de tickets
        dt['QTDE TICKETS'] = dt.apply(
            lambda row: qtde_tickets(row['Linha'], db, row['Dia'], row['Partida'], row['Chegada']),
            axis=1
        )
        
        # Extrai os dois primeiros números de 'day' 
        # E armazena em uma variável
        # Para composição do nome do arquivo
        day_prefix = day[:2]

        # Salva a nova tabela em um novo arquivo CSV
        new_file = f'files_data/LineBus/{line}/{line}_viagens_nao_mon_{day_prefix}OUT24_atualizada.csv'
        dt.to_csv(new_file, index=False, encoding='utf-8-sig', sep=';')
        
        print(f'Arquivo {new_file} criado com sucesso!')




