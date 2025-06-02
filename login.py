import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3
from db import conectar_banco
from menu_principal import abrir_menu_principal
from logger import registrar_log


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_login(email, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT senha_hash FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        senha_hash = resultado[0]
        return senha_hash == hash_senha(senha)
    return False

def criar_usuario(nome, email, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                       (nome, email, hash_senha(senha)))
        conn.commit()
        registrar_log("Usuário criado com sucesso", email)
        return True
    except sqlite3.IntegrityError:
        registrar_log("Erro ao criar usuário (email já existe)", email)
        return False
    finally:
        conn.close()

def abrir_criar_conta():
    janela = tk.Toplevel()
    janela.title("Criar Conta")
    janela.geometry("300x250")

    tk.Label(janela, text="Nome:").pack(pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Email:").pack(pady=5)
    entry_email = tk.Entry(janela)
    entry_email.pack()

    tk.Label(janela, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    def confirmar_criacao():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        if nome and email and senha:
            if criar_usuario(nome, email, senha):
                messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Email já cadastrado.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    tk.Button(janela, text="Criar Conta", command=confirmar_criacao).pack(pady=10)

def abrir_login():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x220")

    tk.Label(login, text="Email:").pack(pady=5)
    entry_usuario = tk.Entry(login)
    entry_usuario.pack()

    tk.Label(login, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(login, show="*")
    entry_senha.pack()

    def fazer_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if verificar_login(usuario, senha):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            registrar_log("Login realizado com sucesso", usuario)
            login.destroy()
            abrir_menu_principal()
        else:
            registrar_log("Tentativa de login inválida", usuario)
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    tk.Button(login, text="Entrar", command=fazer_login).pack(pady=10)
    tk.Button(login, text="Criar Conta", command=abrir_criar_conta).pack()

    login.mainloop()
