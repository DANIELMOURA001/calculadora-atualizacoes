import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import shutil

# URLs e caminhos locais
VERSAO_URL = 'https://raw.githubusercontent.com/DANIELMOURA001/calculadora-atualizacoes/main/calculadora_tkinter.exe'
VERSAO_LOCAL = 'C:/Users/Daniel/Desktop/Calculadora/calculadora_tkinter.exe'
VERSAO_TEMP = 'C:/Users/Daniel/Desktop/Calculadora/calculadora_tkinter_temp.exe'
VERSAO_LOCAL_TXT = 'C:/Users/Daniel/Desktop/Calculadora/versao.txt'
VERSAO_TXT_URL = 'https://raw.githubusercontent.com/DANIELMOURA001/calculadora-atualizacoes/main/versao.txt'

def verificar_atualizacao():
    try:
        # Verificar a versão no servidor (GitHub)
        resposta_versao = requests.get(VERSAO_TXT_URL)
        resposta_versao.raise_for_status()
        versao_nova = resposta_versao.text.strip()

        # Verificar a versão local
        if os.path.exists(VERSAO_LOCAL_TXT):
            with open(VERSAO_LOCAL_TXT, 'r') as f:
                versao_local = f.read().strip()
        else:
            versao_local = '0.0.0'  # Versão inicial se não existir

        # Comparar versões
        if versao_nova > versao_local:
            resposta = messagebox.askyesno("Atualização Disponível", f"Uma nova versão ({versao_nova}) está disponível. Deseja atualizar?")
            if resposta:
                messagebox.showinfo("Atualizando", "O aplicativo será atualizado.")
                baixar_e_atualizar_exe(versao_nova)
                return False  # Interromper para permitir a atualização
            else:
                messagebox.showinfo("Atualização Cancelada", "Você escolheu não atualizar.")
        else:
            messagebox.showinfo("Atualização", f"Você já está usando a versão mais recente ({versao_local}).")
        return True  # Continuar normalmente se não atualizar
    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante a verificação de atualização: {e}")
        return True  # Continuar o aplicativo mesmo em caso de erro

def baixar_e_atualizar_exe(versao_nova):
    try:
        # Baixar a nova versão do executável
        resposta_exe = requests.get(VERSAO_URL, stream=True)
        resposta_exe.raise_for_status()

        # Salvar o executável temporário
        with open(VERSAO_TEMP, 'wb') as f:
            for chunk in resposta_exe.iter_content(chunk_size=8192):
                f.write(chunk)

        # Atualizar o arquivo de versão
        with open(VERSAO_LOCAL_TXT, 'w') as f:
            f.write(versao_nova)

        # Substituir o executável atual pelo novo
        if os.path.exists(VERSAO_LOCAL):
            os.remove(VERSAO_LOCAL)  # Remover o executável antigo
        shutil.move(VERSAO_TEMP, VERSAO_LOCAL)

        # Reiniciar o aplicativo atualizado
        os.startfile(VERSAO_LOCAL)
        sys.exit()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante a atualização: {e}")

def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = str(eval(screen.get()))
            screen.set(result)
        except Exception as e:
            screen.set("Erro")
    elif text == "C":
        screen.set("")
    else:
        screen.set(screen.get() + text)

def iniciar_calculadora(versao_local):
    root = tk.Tk()
    root.title(f"Calculadora - Versão {versao_local}")

    # Definir o tamanho da janela da calculadora
    largura = 300
    altura = 400

    # Centralizar a janela
    tela_largura = root.winfo_screenwidth()
    tela_altura = root.winfo_screenheight()
    pos_x = (tela_largura - largura) // 2
    pos_y = (tela_altura - altura) // 2
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Tela da calculadora
    global screen
    screen = tk.StringVar()
    entry = tk.Entry(root, textvar=screen, font="lucida 20 bold", bd=10, insertwidth=4, width=14, borderwidth=4)
    entry.grid(row=0, column=0, columnspan=4, sticky='nsew')

    # Definição dos botões
    buttons = [
        '7', '8', '9', '+',
        '4', '5', '6', '-',
        '1', '2', '3', '*',
        'C', '0', '=', '/'
    ]

    # Configurar a grade para os botões
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(i + 1, weight=1)

    row = 1
    col = 0
    for button in buttons:
        btn = tk.Button(root, text=button, font="lucida 15 bold", padx=20, pady=20)
        btn.grid(row=row, column=col, sticky='nsew')
        btn.bind("<Button-1>", click)
        col += 1
        if col == 4:
            row += 1
            col = 0

    root.mainloop()

# Verificar se o usuário deseja atualizar
if verificar_atualizacao():
    # Carregar a versão local do arquivo versao.txt
    if os.path.exists(VERSAO_LOCAL_TXT):
        with open(VERSAO_LOCAL_TXT, 'r') as f:
            versao_local = f.read().strip()
    else:
        versao_local = "0.0.0"

    # Iniciar a calculadora com a versão local
    iniciar_calculadora(versao_local)
