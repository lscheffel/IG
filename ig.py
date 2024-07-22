import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime

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

# Função para selecionar a pasta
def selecionar_pasta():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        pasta_label.config(text=pasta_selecionada)
        listar_arquivos_button.config(state=tk.NORMAL)
        processar_button.config(state=tk.NORMAL)
        reverso_button.config(state=tk.NORMAL)
        abrir_button.config(state=tk.NORMAL)
        salvar_lista_button.config(state=tk.NORMAL)
    else:
        pasta_label.config(text='')

# Função para listar arquivos
def listar_arquivos_button_click():
    pasta_selecionada = Path(pasta_label.cget("text"))
    if not pasta_selecionada:
        messagebox.showerror("Erro", "Selecione uma pasta antes de listar os arquivos.")
    else:
        arquivos = listar_arquivos(pasta_selecionada)
        tabela_arquivos.delete(*tabela_arquivos.get_children())
        for arquivo in arquivos:
            tabela_arquivos.insert("", "end", values=(arquivo,))

# Função para processar arquivos
def processar_button_click():
    pasta_selecionada = Path(pasta_label.cget("text"))
    if not pasta_selecionada:
        messagebox.showerror("Erro", "Selecione uma pasta antes de processar os arquivos.")
    else:
        organizar_arquivos(pasta_selecionada)
        messagebox.showinfo("Sucesso", "Arquivos organizados com sucesso!")

# Função para executar processo reverso
def reverso_button_click():
    pasta_selecionada = Path(pasta_label.cget("text"))
    if not pasta_selecionada:
        messagebox.showerror("Erro", "Selecione uma pasta antes de executar o processo reverso.")
    else:
        processo_reverso(pasta_selecionada)
        messagebox.showinfo("Sucesso", "Processo reverso concluído com sucesso!")

# Função para abrir pasta
def abrir_button_click():
    pasta_selecionada = pasta_label.cget("text")
    if not pasta_selecionada:
        messagebox.showerror("Erro", "Selecione uma pasta antes de abrir.")
    else:
        os.startfile(pasta_selecionada)

# Função para salvar lista em Excel
def salvar_lista_button_click():
    pasta_selecionada = Path(pasta_label.cget("text"))
    if not pasta_selecionada:
        messagebox.showerror("Erro", "Selecione uma pasta antes de salvar a lista em um arquivo Excel.")
    else:
        salvar_lista_em_excel(pasta_selecionada)
        messagebox.showinfo("Sucesso", "Lista salva em Excel com sucesso!")

# Função para encerrar aplicação
def encerrar():
    root.destroy()

# Cria a janela principal
root = tk.Tk()
root.title("IG Download Organizer")
root.geometry("800x600")

# Layout da interface
titulo_label = tk.Label(root, text="IG Download Organizer", font=('Helvetica', 20))
titulo_label.pack(pady=10)

selecionar_pasta_button = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta)
selecionar_pasta_button.pack(pady=5)

pasta_label = tk.Label(root, text="", width=80)
pasta_label.pack(pady=5)

listar_arquivos_button = tk.Button(root, text="Listar", command=listar_arquivos_button_click, state=tk.DISABLED)
listar_arquivos_button.pack(pady=5)

tabela_arquivos = ttk.Treeview(root, columns=("arquivo"), show="headings", height=10)
tabela_arquivos.heading("arquivo", text="Arquivos Encontrados")
tabela_arquivos.column("arquivo", width=780)
tabela_arquivos.pack(pady=5)

processar_button = tk.Button(root, text="Processar", command=processar_button_click, state=tk.DISABLED)
processar_button.pack(pady=5)

reverso_button = tk.Button(root, text="Reverso", command=reverso_button_click, state=tk.DISABLED)
reverso_button.pack(pady=5)

abrir_button = tk.Button(root, text="Abrir", command=abrir_button_click, state=tk.DISABLED)
abrir_button.pack(pady=5)

salvar_lista_button = tk.Button(root, text="Salvar Lista", command=salvar_lista_button_click, state=tk.DISABLED)
salvar_lista_button.pack(pady=5)

encerrar_button = tk.Button(root, text="Encerrar", command=encerrar, bg="red", fg="white")
encerrar_button.pack(pady=20)

# Inicia o loop principal da interface
root.mainloop()
