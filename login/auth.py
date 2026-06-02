import sqlite3
import sys
import os

# Adiciona o caminho base para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
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
        usuario = input("Usuário: ").strip()
        senha = input("Senha: ").strip()
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            print(f"\n✅ Login realizado com sucesso! Bem-vindo, {usuario}.")
            return usuario
        else:
            tentativas -= 1
            print(f"❌ Incorreto. Tentativas restantes: {tentativas}")
            
    return None
