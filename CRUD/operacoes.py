import os
from Models.database import conectar
from utils.formatacao import formatar_moeda

def criar_venda(usuario_id):
    print("\n--- CADASTRAR VENDA ---")
    produto = input("Produto: ").strip()
    if not produto:
        print("❌ O nome do produto não pode ser vazio.")
        return
    try:
        quantidade = int(input("Quantidade: ").strip())
        if quantidade <= 0:
            print("❌ A quantidade deve ser um número inteiro positivo.")
            return
        custo = float(input("Custo unitário: ").replace(",", "."))
        valor = float(input("Preço de venda unitário: ").replace(",", "."))

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vendas (usuario_id, produto, quantidade, custo, valor) VALUES (?, ?, ?, ?, ?)", 
                       (usuario_id, produto, quantidade, custo, valor))
        conn.commit()
        conn.close()
        print("✅ Venda cadastrada!")
    except ValueError:
        print("❌ Entrada inválida!")

def ler_vendas(usuario_id):
    print("\n--- LISTA DE VENDAS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, produto, quantidade, custo, valor, data FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall()
    conn.close()
    
    if not vendas:
        print("Nenhuma venda encontrada.")
    else:
        print(f"\n{'ID':<4} {'Produto':<20} {'Qtd':<5} {'Custo Un.':<12} {'Venda Un.':<12} {'Lucro':<10} {'Data':<20}")
        print("-" * 90)
        for v in vendas:
            lucro = (v[2] * v[4]) - (v[2] * v[3])
            print(f"{v[0]:<4} {v[1]:<20} {v[2]:<5} {formatar_moeda(v[3]):<12} {formatar_moeda(v[4]):<12} {formatar_moeda(lucro):<10} {v[5]:<20}")

def atualizar_venda(usuario_id):
    ler_vendas(usuario_id)
    try:
        id_venda = int(input("\nDigite o ID da venda que deseja editar: "))
