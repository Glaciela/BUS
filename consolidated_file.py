# Este script junta os dados de viagens não monitoradas
# Já com a quantidade de bilhetes
# Que estão em arquivos separados
# Divididos em linhas e dias úteis
# E salva em um arquivo CSV consolidado 

import pandas as pd
import os

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

# Armazena em uma variável todas as pastas 
# Dentro de 'files_data/LineBus'
# Que contem as linhas de ônibus
# Transforma a lista de pastas em inteiros
# E ordena os números das linhas
folders = sorted([name for name in os.listdir('files_data/LineBus') if os.path.isdir(os.path.join('files_data/LineBus', name))])
folders = [int(name) for name in folders if name.isdigit()]
folders.sort()
print(folders)

# Caminho para salvar o arquivo consolidado
output_csv = 'files_data/linhas_consolidadas.csv'

# Lista para armazenar DataFrames
dfs = []

for day in business_days_out_2024:
    print(f'Processando dados para o dia: {day}')
    for line in folders:
        # Extrai os dois primeiros números de 'day'
        day_prefix = day[:2]
        # Caminho para o arquivo CSV
        file_path = f'files_data/LineBus/{line}/{line}_viagens_nao_mon_{day_prefix}OUT24_atualizada.csv'
        # Verifica se o arquivo CSV existe
        if os.path.exists(file_path):
            # Leitura do arquivo CSV
            df = pd.read_csv(file_path)
            dfs.append(df)
        else:
            print(f'Arquivo {file_path} nao encontrado.')

# Concatena os DataFrames em um unico DataFrame
consolidated_df = pd.concat(dfs, ignore_index=True)

# Salva o DataFrame consolidado em um arquivo CSV
consolidated_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

print(f'Arquivo consolidado salvo em: {output_csv}')

