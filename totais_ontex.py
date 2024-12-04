from jnsql import simpleQuery
from ftplib import FTP
from datetime import datetime, timedelta
import os

def enviar_totais_ftp(dtini, dtfim, arquivo):
   
    host = "172.31.2.164"
    port = 12021
    username = "jnftp"
    password = "senhaftp"
    
    arquivo = f"totais_ontex_{dtini}_{dtfim}.txt"
    print(f"Nome do arquivo local: {arquivo}")
    
    # Caminho do arquivo no diretório local
    diretorio = os.getcwd()
    arquivo_diretorio = os.path.join(diretorio, arquivo)
    print(f"O arquivo diretorio é: {arquivo_diretorio}")

    dtatual = datetime.now()
    remote_file = f"/EDI_ONTEX/totais/{arquivo}"
    print(f"O arquivo remoto será: {remote_file}")

    try:
        # Conectar ao servidor FTP
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(username, password)

        # Fazer o upload do arquivo
        with open(arquivo_diretorio, 'rb') as file:
            ftp.storbinary(f"STOR {remote_file}", file)

        print(f"Arquivo {arquivo_diretorio} enviado para {remote_file} com sucesso!")

        ftp.quit()

    except Exception as e:
        print(f"Erro: {e}")

dtatual = datetime.now().date()
dtanterior = dtatual - timedelta(days=1)
dtini = dtanterior
dtfim = dtatual

query_vendas = f"""
WITH ITENS AS (
    SELECT
        c.NUNOTA,
        c.SERIENOTA,
        IIF(c.CODTIPOPER IN (102, 119, 128, 1000, 100), '01', '02') AS TIPFAT,
        i.CODPROD,
        i.QTDNEG,
        i.VLRUNIT,
        IIF(ctp.tipmov = 'B', 'S', 'N') AS BONIFICADO,
        i.VLRTOT,
        (i.VLRTOT - i.VLRDESC) AS VLRLIG,
        ISNULL(i.VLRIPI, 0) AS VLRIPI,
        ISNULL(c.VLRCOFINS, 0) AS VLRCOFINS,
        0 AS VLRSUBST,
        ISNULL(i.VLRICMS, 0) AS VLRICMS,
        ISNULL(IIF(i.VLRDESC < 0, 0, i.VLRDESC), 0) AS VLRDESC
    FROM
        TGFCAB c
        INNER JOIN TGFITE i ON i.NUNOTA = c.NUNOTA
        INNER JOIN TGFPRO pro ON pro.CODPROD = i.CODPROD
        INNER JOIN TGFPAR p ON p.CODPARC = c.CODPARC
        INNER JOIN ad_cvtop_full ctp ON ctp.codtipoper = c.CODTIPOPER
    WHERE
        c.DTFATUR BETWEEN '{dtini}' AND '{dtfim}'
        AND c.CODPARC NOT IN (16529)
        AND pro.CODPARCFORN = 9143
)
SELECT
    SUM(VLRTOT) AS TOTAL_VLRTOT
FROM
    ITENS;
"""

query_estoque = f"""
WITH SALDOS AS (
    SELECT 
        p.CODPROD,
        ROUND(IIF(v.DIVIDEMULTIPLICA = 'M', (s.SALDO / v.QUANTIDADE), (s.SALDO * v.QUANTIDADE)), 2) AS SALDO_CALCULADO
    FROM
        TGFPRO p
        INNER JOIN TGFVOA v ON v.CODPROD = p.CODPROD
        OUTER APPLY (
            SELECT
                SUM(ITE.QTDNEG * ITE.ATUALESTOQUE) AS SALDO
            FROM 
                TGFITE ITE 
                INNER JOIN TGFCAB CAB ON CAB.NUNOTA = ITE.NUNOTA
            WHERE 
                ITE.ATUALESTOQUE <> 0
                AND CAB.DTNEG <= '{dtfim}'
                AND RESERVA = 'N'
                AND CODLOCALORIG = 1
                AND ITE.CODPROD = p.CODPROD
        ) s
    WHERE
        p.CODPARCFORN = 9143
        AND p.ATIVO = 'S'
        AND s.SALDO > 1
        AND s.SALDO IS NOT NULL
)
SELECT 
    SUM(SALDO_CALCULADO) AS TOTAL_SALDO_CALCULADO
FROM 
    SALDOS;
"""

query_qtd_vendida = f"""
WITH PRODUTOS AS (
    SELECT
        '2' CODIGO,
        '23191831000193' NUMERO,
        p.CODPROD,
        RTRIM(MAX(v.CODBARRA)) AS COBARRA,
        MAX(v.AD_ITENSPORVENDA) AS ITENSPORVENDA,
        CAST(MAX(sankhya.AD_SNK_PRECO_JN(0, p.CODPROD, '{dtfim}')) AS DECIMAL(18, 2)) AS PRECO,
        RTRIM(p.DESCRPROD) AS PRODUTO,
        IIF(p.ATIVO = 'S', '01', '02') AS Linha
    FROM
        TGFPRO p
        LEFT JOIN TGFVOA v ON v.CODPROD = p.CODPROD
        INNER JOIN TGFITE i ON i.CODPROD = p.CODPROD
        INNER JOIN TGFCAB c ON c.NUNOTA = i.NUNOTA
    WHERE
        p.CODPARCFORN = 9143
        AND c.DTFATUR BETWEEN '{dtini}' AND '{dtfim}'
    GROUP BY
        p.CODPROD,
        p.DESCRPROD,
        p.ATIVO
)
SELECT
    SUM(ITENSPORVENDA) AS QUANTIDADE_VENDIDA
FROM
    PRODUTOS;
"""

try:
    # Executa as queries
    total_vendas = simpleQuery(query_vendas)
    total_saldo = simpleQuery(query_estoque)
    qtd_vendida = simpleQuery(query_qtd_vendida)
    
    resultado_vendas = total_vendas.iloc[0, 0]
    resultado_saldo = total_saldo.iloc[0, 0]
    resultado_quantidade = qtd_vendida.iloc[0, 0]
    
    conteudo = (
        f"Valores totais:\n\n"
        f"1. Total de Vendas: {resultado_vendas}\n"
        f"2. Total Estoque: {resultado_saldo}\n"
        f"3. Quantidade Vendida: {resultado_quantidade}\n"
    )
    
    arquivo = f"totais_ontex_{dtini}_{dtfim}.txt"
    
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    print(f"Resultados salvos com sucesso em '{arquivo}'")
    print("Enviando arquivo para o FTP",enviar_totais_ftp(dtini, dtfim, arquivo))
    
except Exception as e:
    print(f"Erro ao executar as consultas ou salvar o arquivo: {e}")



