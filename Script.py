import pandas as pd
import requests
import json
import time
base_url = 'https://www.receitaws.com.br/v1/cnpj/'
arquivo = 'LAYOUT_PADRAO.xlsx'

df = pd.read_excel(arquivo)
df['resultado'] = None
df['logradouro'] = None
df['numero'] = None
df['municipio'] = None
df['bairro'] = None
df['uf'] = None
df['cep'] = None

print(df)
for x in range(len(df)):
    print(x)
    try:
        reg = 14 - len(str(df['CNPJ'][x]))
        cnpj = ('0' * reg) + str(df['CNPJ'][x])
        consulta = base_url + cnpj
        r = requests.get(consulta)
        r = r.content
        df['resultado'][x] =   json.loads(r)
        df['logradouro'][x] =  json.loads(r)['logradouro']
        df['numero'][x]     =  json.loads(r)['numero']
        df['municipio'][x]  =  json.loads(r)['municipio']
        df['bairro'][x]     =  json.loads(r)['bairro']
        df['uf'][x]         =  json.loads(r)['uf']
        df['cep'][x]        =  json.loads(r)['cep']
        
    except:
        print('erro próximo')
    time.sleep(20)


df.to_excel('resultado.xlsx')
