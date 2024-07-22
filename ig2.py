import streamlit as st
import os
import re
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime

def listar_arquivos(pasta_selecionada):
    extensoes = ['.mp4', '.jpg', '.png', '.txt']
    arquivos = [f.name for f in pasta_selecionada.iterdir() if f.is_file() and f.suffix in extensoes]
    return arquivos

def organizar_arquivos(pasta_selecionada):
    extensoes = ['.mp4', '.jpg', '.png', '.txt']
    arquivos = [f for f in pasta_selecionada.iterdir() if f.is_file() and f.suffix in extensoes]
    for arquivo in arquivos:
        nome_arquivo = arquivo.stem
        nome_usuario = re.sub(r'[^\w\s]', '', nome_arquivo.split('_')[0])
        destino = pasta_selecionada / nome_usuario
        if arquivo.exists():
            if not destino.exists():
                destino.mkdir()
            arquivo_destino = destino / arquivo.name
            if arquivo_destino.exists():
                i = 1
                novo_nome = nome_arquivo
                while (destino / (novo_nome + f"_{i}")).exists():
                    i += 1
                novo_nome = novo_nome + f"_{i}"
                arquivo_destino = destino / (novo_nome + arquivo.suffix)
            shutil.move(arquivo, arquivo_destino)

def processo_reverso(pasta_selecionada):
    for root, _, files in os.walk(pasta_selecionada):
        for arquivo in files:
            arquivo_origem = Path(root) / arquivo
            arquivo_destino = pasta_selecionada / arquivo
            if arquivo_destino.exists():
                arquivo_destino.replace(arquivo_origem)
            else:
                shutil.move(arquivo_origem, arquivo_destino)
    for subdiretorio in pasta_selecionada.iterdir():
        if subdiretorio.is_dir() and not list(subdiretorio.iterdir()):
            subdiretorio.rmdir()

def salvar_lista_em_excel(pasta_selecionada):
    lista_arquivos = []
    for root, _, files in os.walk(pasta_selecionada):
        for arquivo in files:
            caminho_completo = os.path.join(root, arquivo)
            lista_arquivos.append(os.path.relpath(caminho_completo, pasta_selecionada))
    lista_arquivos_sep = [arquivo.split(os.sep) for arquivo in lista_arquivos]
    max_colunas = max(len(arquivo) for arquivo in lista_arquivos_sep)
    colunas = [f'Coluna {i + 1}' for i in range(max_colunas)]
    df = pd.DataFrame(columns=colunas)
    for i, arquivo in enumerate(lista_arquivos_sep):
        for j, diretorio in enumerate(arquivo):
            df.at[i, f'Coluna {j + 1}'] = diretorio
    pasta_raiz = os.path.basename(pasta_selecionada)
    data_atual = datetime.now().strftime('%Y-%m-%d')
    nome_arquivo = f'FileList_{pasta_raiz}_{data_atual}.xlsx'
    df.to_excel(os.path.join(pasta_selecionada, nome_arquivo), index=False)

st.title("IG Download Organizer")

pasta_selecionada = st.text_input("Selecione a pasta:")
if st.button("Listar"):
    if pasta_selecionada:
        arquivos = listar_arquivos(Path(pasta_selecionada))
        st.write(arquivos)
    else:
        st.error("Selecione uma pasta antes de listar os arquivos.")

if st.button("Processar"):
    if pasta_selecionada:
        organizar_arquivos(Path(pasta_selecionada))
        st.success("Arquivos organizados com sucesso!")
    else:
        st.error("Selecione uma pasta antes de processar os arquivos.")

if st.button("Reverso"):
    if pasta_selecionada:
        processo_reverso(Path(pasta_selecionada))
        st.success("Processo reverso concluído com sucesso!")
    else:
        st.error("Selecione uma pasta antes de executar o processo reverso.")

if st.button("Salvar Lista"):
    if pasta_selecionada:
        salvar_lista_em_excel(Path(pasta_selecionada))
        st.success("Lista salva em Excel com sucesso!")
    else:
        st.error("Selecione uma pasta antes de salvar a lista em um arquivo Excel.")
