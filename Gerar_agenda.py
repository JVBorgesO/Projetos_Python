import pandas as pd
from datetime import datetime, timedelta

file = 'ROTEIRO_TEMPLATE.xlsx'
df = pd.read_excel(file, sheet_name='Agenda')

print(df.head())

hoje = datetime.now()
dt_atual = hoje.strftime('%Y-%m-%d')
dia_semana = hoje.weekday()  # 0 = segunda, 6 = domingo

df['date'] = pd.to_datetime(df['date']).dt.date

dias_para_gerar = []

# segunda a quinta gerar o dia seguinte
if dia_semana in range(0, 4): 
    dias_para_gerar = [(hoje + timedelta(days=1)).date()]

# sexta gerar sabado e segunda
elif dia_semana == 4:  
    dias_para_gerar = [
        (hoje + timedelta(days=1)).date(),  
        (hoje + timedelta(days=3)).date(),  
    ]
else: # sabado e domingo nao gera arquivo
    exit()

df_filtrado = df[df['date'].isin(dias_para_gerar)]

if df_filtrado.empty:
    print('nenhum dado encontrado. arquivo nao sera gerado.')
else:
    new_df = df_filtrado[['serviceLocal', 'agent', 'date']].copy()
    new_df.insert(0, 'command', 'I')  
    new_df.insert(1, 'CF_OBS', 'ajuste roteiro ' + dt_atual) 
    new_df.insert(2, 'CF_DT_IMP', dt_atual)
    new_df['hour'] = '05:00'         
    new_df['activitiesOrigin'] = '2'         
    new_df['date'] = pd.to_datetime(new_df['date']).dt.strftime('%d/%m/%Y')

    csv_file = 'AGD_ROTEIRO_' + dt_atual + '_V2.csv'

    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        f.write('C\n')
        new_df.to_csv(f, index=False, sep=';')

    print(f'Arquivo "{csv_file}" criado com sucesso para o(s) dia(s): {", ".join(d.strftime("%d/%m/%Y") for d in dias_para_gerar)}')
