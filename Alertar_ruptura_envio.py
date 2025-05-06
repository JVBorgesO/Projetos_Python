import pyodbc
import smtplib
import pandas as pd
import datetime
import sqlalchemy
from sqlalchemy import types, create_engine
from datetime import timedelta
from email.message import EmailMessage

# conecxao banco
db_string_p  = ''
engine_p     = create_engine(db_string_p)
conn_p       = engine_p.connect()

# config biblioteca smtplib
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
EMAIL_REMETENTE = ''
SENHA = '' 

assunto = 'Alerta de Ruptura'
# path = 'base_ruptura_v2.xlsx'
# df = pd.read_excel(path)

query1 = """

"""
df = pd.read_sql(query1, conn_p)
pd.set_option('display.max_columns', None)
conn_p.close()

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
