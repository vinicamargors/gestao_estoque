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

def abrir_login():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x200")

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
    login.mainloop()
