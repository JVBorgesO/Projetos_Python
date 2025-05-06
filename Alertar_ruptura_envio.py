import pyodbc
import smtplib
import pandas as pd
import datetime
import sqlalchemy
from sqlalchemy import types, create_engine
from datetime import timedelta
from email.message import EmailMessage

# conecxao banco
db_string_p  = 'postgresql://joao_borges@is-dw-prod:In_store2025@is-dw-prod.postgres.database.azure.com:5432/is-producao'
engine_p     = create_engine(db_string_p)
conn_p       = engine_p.connect()

# config biblioteca smtplib
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
EMAIL_REMETENTE = 'joao.borges@instorebr.com'
SENHA = 'Instore@2025' 

assunto = 'Alerta de Ruptura'
# path = 'base_ruptura_v2.xlsx'
# df = pd.read_excel(path)

query1 = """

(
with tab_a as
(
select tsk_id, count(*) as tt, hty_initialdatehour, loc_id
FROM   brf_pet_2.f_dis_share_sort_as
WHERE  hty_initialdatehour >= CURRENT_DATE  

group by tsk_id , hty_initialdatehour, loc_id

)
,
tab_b as (
select tsk_id, count(*) as sim, hty_initialdatehour, loc_id
FROM   brf_pet_2.f_dis_share_sort_as
WHERE  hty_initialdatehour >= CURRENT_DATE

and e_disp = 'SIM'

group by tsk_id, hty_initialdatehour, loc_id

)

select 
loc_description, loc_mail, 

tab_a.TSK_ID, tab_a.LOC_ID , tab_a.hty_initialdatehour, sim, tt from tab_a 
full join tab_b on tab_a.tsk_id = tab_b.tsk_id
inner join brf_pet_2.d_locais ON d_locais.loc_id = tab_a.loc_id
where sim is null or sim = 0

)

UNION ALL


(
with tab_d as
(
select tsk_id, count(*) as tt, hty_initialdatehour, loc_id
FROM   brf_pet_2.f_loja_ideal
WHERE  hty_initialdatehour >= CURRENT_DATE



group by tsk_id , hty_initialdatehour, loc_id

)
,
tab_e as (
select tsk_id, count(*) as sim, hty_initialdatehour, loc_id
FROM   brf_pet_2.f_loja_ideal
WHERE  hty_initialdatehour >= CURRENT_DATE

and disponivel = 'SIM'
group by tsk_id, hty_initialdatehour, loc_id
)

select 
loc_description, loc_mail,

tab_d.TSK_ID, tab_d.LOC_ID , tab_d.hty_initialdatehour, sim, tt from tab_d 
full join tab_e on tab_d.tsk_id = tab_e.tsk_id
inner join brf_pet_2.d_locais ON d_locais.loc_id = tab_d.loc_id
where sim is null or sim = 0
)
"""
df = pd.read_sql(query1, conn_p)
pd.set_option('display.max_columns', None)
conn_p.close()


df['loc_mail'] = 'joao.borges@instorebr.com'

print(df)

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.starttls()
    smtp.login(EMAIL_REMETENTE, SENHA)

    for _, row in df.iterrows():
        email_destinatario = row['loc_mail']
        nome_loja = row['loc_description']
        data_ruptura = pd.to_datetime(row['hty_initialdatehour']).strftime('%d/%m/%Y')

        mensagem = f'''Olá,

A loja {nome_loja} não possui nenhum produto disponível desde {data_ruptura}.

Este é um alerta automático do sistema.

Atenciosamente,
Instore'''

        msg = EmailMessage()
        msg['Subject'] = assunto
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = email_destinatario
        msg.set_content(mensagem)

        try:
            smtp.send_message(msg)
            print(f'E-mail enviado para {email_destinatario}')
        except Exception as e:
            print(f'Erro ao enviar para {email_destinatario}: {e}')
