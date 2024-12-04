def enviar_totais_ftp(dtini, dtfim, arquivo):
   
    host = ""
    port = 
    username = ""
    password = ""
    
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

"""

query_estoque = f"""

"""

query_qtd_vendida = f"""

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



