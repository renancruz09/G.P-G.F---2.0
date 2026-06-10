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
        if custo < 0:
            print("❌ O custo não pode ser negativo.")
            return
        valor = float(input("Preço de venda unitário: ").replace(",", "."))
        if valor < 0:
            print("❌ O valor de venda não pode ser negativo.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vendas (usuario_id, produto, quantidade, custo, valor) VALUES (?, ?, ?, ?, ?)", 
                       (usuario_id, produto, quantidade, custo, valor))
        conn.commit()
        conn.close()
        print("✅ Venda cadastrada!")
    except ValueError:
        print("❌ Entrada inválida para quantidade, custo ou valor!")

def ler_vendas(usuario_id):
    print("\n--- LISTA DE VENDAS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, produto, quantidade, custo, valor, data FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall()
    conn.close()
    
    if not vendas:
        print("Nenhuma venda encontrada para este usuário.")
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
        novo_produto = input("Novo nome do produto (deixe em branco para manter): ").strip()
        nova_quantidade_str = input("Nova quantidade (deixe em branco para manter): ").strip()
        novo_custo_str = input("Novo custo unitário (deixe em branco para manter): ").strip()
        novo_valor_str = input("Novo preço de venda unitário (deixe em branco para manter): ").strip()
        
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT produto, quantidade, custo, valor FROM vendas WHERE id = ? AND usuario_id = ?", (id_venda, usuario_id))
        venda_existente = cursor.fetchone()
        
        if not venda_existente:
            print("❌ ID não encontrado ou você não tem permissão para editar esta venda.")
            conn.close()
            return
            
        produto_atual, quantidade_atual, custo_atual, valor_atual = venda_existente
        
        produto = novo_produto if novo_produto else produto_atual
        quantidade = int(nova_quantidade_str) if nova_quantidade_str else quantidade_atual
        custo = float(novo_custo_str.replace(",", ".")) if novo_custo_str else custo_atual
        valor = float(novo_valor_str.replace(",", ".")) if novo_valor_str else valor_atual

        cursor.execute("UPDATE vendas SET produto = ?, quantidade = ?, custo = ?, valor = ? WHERE id = ? AND usuario_id = ?", 
                       (produto, quantidade, custo, valor, id_venda, usuario_id))
        if cursor.rowcount > 0:
            conn.commit()
            print("✅ Venda atualizada!")
        else:
            print("❌ Nenhuma alteração realizada.")
        conn.close()
    except ValueError:
        print("❌ Entrada inválida!")

def deletar_venda(usuario_id):
    ler_vendas(usuario_id)
    try:
        id_venda = int(input("\nDigite o ID da venda que deseja excluir: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE id = ? AND usuario_id = ?", (id_venda, usuario_id))
        if cursor.rowcount > 0:
            conn.commit()
            print("✅ Venda excluída!")
        else:
            print("❌ ID não encontrado ou você não tem permissão para excluir esta venda.")
        conn.close()
    except ValueError:
        print("❌ Entrada inválida!")

def calcular_financas(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT quantidade, custo, valor FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall()
    conn.close()

    total_vendas = 0.0
    total_custos = 0.0

    for qtd, custo_unit, valor_unit in vendas:
        total_vendas += qtd * valor_unit
        total_custos += qtd * custo_unit
    
    lucro_bruto = total_vendas - total_custos

    print("\n" + "="*40)
    print("        RESUMO FINANCEIRO")
    print("="*40)
    print(f"Total de Vendas:  {formatar_moeda(total_vendas)}")
    print(f"Total de Custos:  {formatar_moeda(total_custos)}")
    print(f"Lucro Bruto:      {formatar_moeda(lucro_bruto)}")
    print("-" * 40)
    if total_vendas > 0:
        margem_lucro = (lucro_bruto / total_vendas) * 100
        print(f"Margem de Lucro:  {margem_lucro:.2f}%")
    else:
        print("Margem de Lucro:  N/A (sem vendas)")
    print("="*40)
