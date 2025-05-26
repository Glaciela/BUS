# Este script processa 
# A quantidade de viagens não monitoradas
# E também sem bilhetes
# E compara com a quantidade total de viagens programadas
# Criando um arquivo com a nova informação
# Em porcentagem

import pandas as pd
import os

# Função que recebe a linha
# E o arquivo contendo a quantidade de bilhetes por linha
# E retorna a quantidade de vezes que a linha não tem bilhetes
# (QTDE TICKETS = 0)
def qtde_no_tickets(line, con):
    qtde_0 = 0
    for i in range(con.shape[0]):
        if con['Linha'].iloc[i] == line:
            if con['QTDE TICKETS'].iloc[i] == 0:
                qtde_0 += 1

    return qtde_0

# Armazena em uma variável as linhas com a quantidade de bilhetes
line_con = pd.read_csv('files_data/linhas_consolidadas.csv',encoding='utf-8-sig', sep=';')

# Armazena em uma variável as viagens programadas de outubro de 2024
travel_prog = pd.read_csv('files_data/n_viagens_programadas_outubro_2024.csv',encoding='utf-8-sig', sep=';')

# Remove colunas totalmente vazias de travel_prog
travel_prog.dropna(axis=1, how='all', inplace=True)

# Insere em uma coluna na variável travel_prog
# A quantidade de viagens programadas sem bilhete
# E não monitoradas
travel_prog.insert(5, 'Sem bilhete', travel_prog.apply(
    lambda row: qtde_no_tickets(row['N. Linha'], line_con),
    axis=1
))

# Insere em uma coluna na variável travel_prog
# A porcentagem de viagens programadas sem bilhete
# E não monitoradas
# Em comparação com o total de viagens programadas
travel_prog.insert(6, 'Porcentagem', 
    travel_prog.apply(
        lambda row: round((row['Sem bilhete'] / row['n. viagens'] * 100), 1) if row['n. viagens'] != 0 else 0,
        axis=1
    )
)

# Salva a nova tabela em um novo arquivo CSV
new_file = 'files_data/n_viagens_programadas_outubro_2024_atualizado.csv'
travel_prog.to_csv(new_file, index=False, encoding='utf-8-sig', sep=';')
        
print(f'Arquivo {new_file} criado com sucesso!')




