import sys
import os

# Adiciona o caminho base para importar Models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Models.database import conectar

def criar_venda(usuario_logado):
    print("\n--- CADASTRAR VENDA ---")
    produto = input("Produto: ").strip()
    try:
        valor = float(input("Valor: ").replace(',', '.'))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vendas (usuario_id, produto, valor) VALUES (?, ?, ?)", 
                       (usuario_logado, produto, valor))
        conn.commit()
        conn.close()
        print("✅ Venda cadastrada!")
    except ValueError:
        print("❌ Valor inválido!")

def ler_vendas():
    print("\n--- LISTA DE VENDAS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()
    conn.close()
    
    if not vendas:
        print("Nenhuma venda encontrada.")
    else:
        for v in vendas:
            print(f"ID: {v[0]} | Usuário: {v[1]} | Produto: {v[2]} | Valor: R${v[3]:.2f} | Data: {v[4]}")

def atualizar_venda(usuario_logado):
    ler_vendas()
    try:
        id_venda = int(input("\nDigite o ID da venda que deseja editar: "))
        novo_produto = input("Novo nome do produto: ").strip()
        novo_valor = float(input("Novo valor: ").replace(',', '.'))
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE vendas SET produto = ?, valor = ? WHERE id = ?", 
                       (novo_produto, novo_valor, id_venda))
        if cursor.rowcount > 0:
            conn.commit()
            print("✅ Venda atualizada!")
        else:
            print("❌ ID não encontrado.")
        conn.close()
    except ValueError:
        print("❌ Entrada inválida!")

def deletar_venda():
    ler_vendas()
    try:
        id_venda = int(input("\nDigite o ID da venda que deseja excluir: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE id = ?", (id_venda,))
        if cursor.rowcount > 0:
            conn.commit()
            print("✅ Venda excluída!")
        else:
            print("❌ ID não encontrado.")
        conn.close()
    except ValueError:
        print("❌ Entrada inválida!")