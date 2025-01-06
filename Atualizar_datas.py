from querys import info_prod_ecomerce
from datetime import datetime
import pandas as pd


def gerar_arquivo(dtini, dtfim):
    dados_produtos = info_prod_ecomerce(dtini, dtfim)
    if isinstance(dados_produtos, pd.DataFrame):
        dados_produtos = dados_produtos.applymap(
            lambda x: str(x).replace('.', ',') if isinstance(x, (float, str)) else x
        )
        nome_arquivo_produtos = "prods_ecomerce_.csv"
        dados_produtos.to_csv(nome_arquivo_produtos, sep=';', index=False, encoding='utf-8')
        print(f"Arquivo CSV de e-comerce gerado com sucesso!: {nome_arquivo_produtos}")
    else:
        print("Erro ao gerar o arquivo de e-comerce.")


dtini_input = input("Insira a data inicial (DD/MM/AAAA): ")
dtfim_input = input("Insira a data final (DD/MM/AAAA): ")

try:
    dtini = datetime.strptime(dtini_input, "%d/%m/%Y").strftime("%Y-%m-%d")
    dtfim = datetime.strptime(dtfim_input, "%d/%m/%Y").strftime("%Y-%m-%d")

    gerar_arquivo(dtini, dtfim)
except ValueError:
    print("Formato de data inválido. Certifique-se de usar DD/MM/AAAA.")
