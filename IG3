import os
import re
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime
import streamlit as st

# Função para listar arquivos na pasta selecionada
def listar_arquivos(pasta_selecionada):
    extensoes = ['.mp4', '.jpg', '.png', '.txt']
    arquivos = [f.name for f in pasta_selecionada.iterdir() if f.is_file() and f.suffix in extensoes]
    return arquivos

# Função para organizar arquivos na pasta
def organizar_arquivos(pasta_selecionada):
    extensoes = ['.mp4', '.jpg', '.png', '.txt']
    arquivos = [f for f in pasta_selecionada.iterdir() if f.is_file() and f.suffix in extensoes]

    for arquivo in arquivos:
        nome_arquivo = arquivo.stem
        nome_usuario = re.sub(r'[^\w\s]', '', nome_arquivo.split('_')[0])  # Remove caracteres inválidos

        destino = pasta_selecionada / nome_usuario

        # Verifica se o arquivo original ainda existe
        if arquivo.exists():
            if not destino.exists():
                destino.mkdir()

            # Move o arquivo para o destino
            arquivo_destino = destino / arquivo.name

            # Verifica se o arquivo de destino já existe
            if arquivo_destino.exists():
                i = 1
                novo_nome = nome_arquivo
                while (destino / (novo_nome + f"_{i}")).exists():
                    i += 1
                novo_nome = novo_nome + f"_{i}"
                arquivo_destino = destino / (novo_nome + arquivo.suffix)

            shutil.move(arquivo, arquivo_destino)

# Função para o processo reverso
def processo_reverso(pasta_selecionada):
    for root, _, files in os.walk(pasta_selecionada):
        for arquivo in files:
            arquivo_origem = Path(root) / arquivo
            arquivo_destino = pasta_selecionada / arquivo

            # Verifica se o arquivo de destino já existe na pasta raiz
            if arquivo_destino.exists():
                arquivo_destino.replace(arquivo_origem)
            else:
                shutil.move(arquivo_origem, arquivo_destino)

    # Apaga subdiretórios vazios
    for subdiretorio in pasta_selecionada.iterdir():
        if subdiretorio.is_dir() and not list(subdiretorio.iterdir()):
            subdiretorio.rmdir()

# Função para salvar a lista em um arquivo Excel
def salvar_lista_em_excel(pasta_selecionada):
    lista_arquivos = []
    for root, _, files in os.walk(pasta_selecionada):
        for arquivo in files:
            caminho_completo = os.path.join(root, arquivo)
            lista_arquivos.append(os.path.relpath(caminho_completo, pasta_selecionada))

    lista_arquivos_sep = [arquivo.split(os.sep) for arquivo in lista_arquivos]

    # Determine o número máximo de colunas necessárias com base no arquivo mais profundo
    max_colunas = max(len(arquivo) for arquivo in lista_arquivos_sep)

    # Crie uma lista de nomes de colunas
    colunas = [f'Coluna {i + 1}' for i in range(max_colunas)]

    # Crie um DataFrame preenchendo os valores de coluna para cada nível de diretório
    df = pd.DataFrame(columns=colunas)
    for i, arquivo in enumerate(lista_arquivos_sep):
        for j, diretorio in enumerate(arquivo):
            df.at[i, f'Coluna {j + 1}'] = diretorio

    # Salve o DataFrame em um arquivo Excel
    pasta_raiz = os.path.basename(pasta_selecionada)
    data_atual = datetime.now().strftime('%Y-%m-%d')
    nome_arquivo = f'FileList_{pasta_raiz}_{data_atual}.xlsx'

    df.to_excel(os.path.join(pasta_selecionada, nome_arquivo), index=False)

# Interface Streamlit
st.title("IG Download Organizer")

# Seleção da pasta
pasta_selecionada = st.text_input("Selecione a pasta", value="")

# Botões
if st.button("Selecionar Pasta"):
    pasta_selecionada = st.text_input("Pasta selecionada", value=st.text_input("Selecione a pasta", value=""))

if pasta_selecionada:
    pasta_path = Path(pasta_selecionada)

    if st.button("Listar Arquivos"):
        arquivos = listar_arquivos(pasta_path)
        st.write("Arquivos Encontrados:")
        for arquivo in arquivos:
            st.write(arquivo)

    if st.button("Processar Arquivos"):
        organizar_arquivos(pasta_path)
        st.success("Arquivos organizados com sucesso!")

    if st.button("Reverso"):
        processo_reverso(pasta_path)
        st.success("Processo reverso concluído com sucesso!")

    if st.button("Abrir Pasta"):
        os.startfile(pasta_selecionada)
        st.info("Pasta aberta")

    if st.button("Salvar Lista em Excel"):
        salvar_lista_em_excel(pasta_path)
        st.success("Lista salva em Excel com sucesso!")

# Executar Streamlit: salve este arquivo como app.py e rode no terminal com `streamlit run app.py`
