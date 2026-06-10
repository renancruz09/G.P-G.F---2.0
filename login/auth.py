import sqlite3
import os
from Models.database import conectar

def cadastrar_usuario():
    print("\n" + "-"*30)
    print("      NOVO CADASTRO")
    print("-" * 30)
    
    usuario = input("Escolha um nome de usuário: ").strip()
    if not usuario:
        print("❌ O nome de usuário não pode ser vazio.")
        return False
        
    senha = input("Escolha uma senha: ").strip()
    confirmar = input("Confirme a senha: ").strip()
    
    if senha != confirmar:
        print("❌ As senhas não coincidem.")
        return False
    
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        print("\n✅ Usuário cadastrado com sucesso!")
        return True
    except sqlite3.IntegrityError:
        print("❌ Este usuário já existe!")
        return False
    finally:
        conn.close()

def realizar_login():
    print("\n" + "="*30)
    print("      SISTEMA DE LOGIN")
    print("="*30)
    
    tentativas = 3
    while tentativas > 0:
        usuario_digitado = input("Usuário: ").strip()
        senha_digitada = input("Senha: ").strip()
        
        conn = conectar()
        cursor = conn.cursor()
        # Buscamos apenas o ID e o Nome
        cursor.execute("SELECT id, usuario FROM usuarios WHERE usuario = ? AND senha = ?", (usuario_digitado, senha_digitada))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            user_id, username = resultado # Aqui ele pega exatamente 2 valores
            print(f"\n✅ Login realizado com sucesso! Bem-vindo, {username}.")
            return user_id, username
        else:
            tentativas -= 1
            print(f"❌ Incorreto. Tentativas restantes: {tentativas}")
            
    return None, None
