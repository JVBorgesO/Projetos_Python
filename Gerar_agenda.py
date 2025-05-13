import pandas as pd
from datetime import datetime

file = 'ROTEIRO_TEMPLATE.xlsx'
df = pd.read_excel(file, sheet_name='teste')

print(df.head())

dt_atual = datetime.now().strftime('%Y-%m-%d')

new_df = df[['serviceLocal', 'agent', 'date']].copy()

new_df.insert(0, 'command', 'I')  
new_df.insert(1, 'CF_OBS', 'ajuste roteiro ' + dt_atual) 
new_df.insert(2, 'CF_DT_IMP', dt_atual)
new_df['hour'] = '05:00'         
new_df['activitiesOrigin'] = '2'         

new_df['date'] = pd.to_datetime(new_df['date']).dt.strftime('%d/%m/%Y')

print(new_df)

csv_file = 'AGD_ROTEIRO_' + dt_atual + '_V2.csv'

# Gerar o CSV com ponto e vírgula como delimitador
new_df.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig')

print(f'Arquivo "{csv_file}" criado com sucesso.')
