import os
from Models.database import conectar
from utils.formatacao import formatar_moeda

def criar_venda(usuario_id):
    print("\n--- CADASTRAR VENDA ---")
    produto = input("Produto: ").strip()
    if not produto: return
    try:
        quantidade = int(input("Quantidade: ").strip())
        custo = float(input("Custo unitário: ").replace(",", "."))
        valor = float(input("Preço de venda unitário: ").replace(",", "."))
        conn = conectar(); cursor = conn.cursor()
        cursor.execute("INSERT INTO vendas (usuario_id, produto, quantidade, custo, valor) VALUES (?, ?, ?, ?, ?)", (usuario_id, produto, quantidade, custo, valor))
        conn.commit(); conn.close()
        print("✅ Venda cadastrada!")
    except ValueError: print("❌ Entrada inválida!")

def ler_vendas(usuario_id):
    print("\n--- LISTA DE VENDAS ---")
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT id, produto, quantidade, custo, valor, data FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall(); conn.close()
    if not vendas: print("Nenhuma venda encontrada.")
    else:
        print(f"\n{'ID':<4} {'Produto':<20} {'Qtd':<5} {'Custo Un.':<12} {'Venda Un.':<12} {'Lucro Total':<12} {'Data':<20}")
        print("-" * 95)
        for v in vendas:
            lucro_total = (v[2] * v[4]) - (v[2] * v[3])
            print(f"{v[0]:<4} {v[1]:<20} {v[2]:<5} {formatar_moeda(v[3]):<12} {formatar_moeda(v[4]):<12} {formatar_moeda(lucro_total):<12} {v[5]:<20}")

def atualizar_venda(usuario_id):
    ler_vendas(usuario_id)
    try:
        id_venda = int(input("\nDigite o ID da venda que deseja editar: "))
        conn = conectar(); cursor = conn.cursor()
        cursor.execute("SELECT produto, quantidade, custo, valor FROM vendas WHERE id = ? AND usuario_id = ?", (id_venda, usuario_id))
        venda_existente = cursor.fetchone()
        if not venda_existente:
            print("❌ ID não encontrado."); conn.close(); return
        
        novo_produto = input(f"Novo nome [{venda_existente[0]}]: ").strip()
        nova_qtd = input(f"Nova quantidade [{venda_existente[1]}]: ").strip()
        novo_custo = input(f"Novo custo [{venda_existente[2]}]: ").strip()
        novo_valor = input(f"Novo preço [{venda_existente[3]}]: ").strip()
        
        produto = novo_produto if novo_produto else venda_existente[0]
        quantidade = int(nova_qtd) if nova_qtd else venda_existente[1]
        custo = float(novo_custo.replace(",", ".")) if novo_custo else venda_existente[2]
        valor = float(novo_valor.replace(",", ".")) if novo_valor else venda_existente[3]

        cursor.execute("UPDATE vendas SET produto = ?, quantidade = ?, custo = ?, valor = ? WHERE id = ? AND usuario_id = ?", (produto, quantidade, custo, valor, id_venda, usuario_id))
        conn.commit(); conn.close(); print("✅ Venda atualizada!")
    except ValueError: print("❌ Entrada inválida!")

def deletar_venda(usuario_id):
    ler_vendas(usuario_id)
    try:
        id_venda = int(input("\nID para excluir: "))
        conn = conectar(); cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE id = ? AND usuario_id = ?", (id_venda, usuario_id))
        if cursor.rowcount > 0: conn.commit(); print("✅ Excluída!")
        conn.close()
    except ValueError: print("❌ Inválido!")

def calcular_financas(usuario_id):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT quantidade, custo, valor FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall(); conn.close()
    total_vendas = sum(v[0] * v[2] for v in vendas)
    total_custos = sum(v[0] * v[1] for v in vendas)
    lucro = total_vendas - total_custos
    print(f"\nResumo: Vendas {formatar_moeda(total_vendas)} | Custos {formatar_moeda(total_custos)} | Lucro {formatar_moeda(lucro)}")
