from Models.database import conectar

# ==========================================
#          MÓDULO DE PRODUTOS
# ==========================================

def gerenciar_produtos(usuario_id):
    while True:
        print("\n--- MENU DE PRODUTOS E ESTOQUE ---")
        print("1. Cadastrar Novo Produto")
        print("2. Listar Estoque")
        print("3. Adicionar mais itens ao Estoque")
        print("4. Editar Produto")
        print("5. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_produto(usuario_id)
        elif opcao == '2':
            listar_produtos(usuario_id)
        elif opcao == '3':
            adicionar_estoque(usuario_id)
        elif opcao == '4':
            editar_produto(usuario_id)
        elif opcao == '5':
            break
        else:
            print("Opção inválida!")

def cadastrar_produto(usuario_id):
    print("\n--- NOVO PRODUTO ---")
    nome = input("Nome do Produto: ")
    tamanho = input("Tamanho (P, M, G ou 38, 40...): ")
    quantidade = int(input("Quantidade em Estoque: "))
    custo = float(input("Custo unitário: ").replace(",", "."))
    valor = float(input("Preço de venda: ").replace(",", "."))
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (usuario_id, nome, tamanho, quantidade_estoque, custo, valor_padrao) VALUES (?, ?, ?, ?, ?, ?)", 
                   (usuario_id, nome, tamanho, quantidade, custo, valor))
    conn.commit()
    conn.close()
    print("✅ Produto cadastrado!")

def listar_produtos(usuario_id):
    print("\n--- SEU ESTOQUE ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, tamanho, quantidade_estoque, custo, valor_padrao FROM produtos WHERE usuario_id = ?", (usuario_id,))
    produtos = cursor.fetchall()
    conn.close()
    
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return False
        
    for p in produtos:
        print(f"ID: {p[0]} | Produto: {p[1]} | Tam: {p[2]} | Estoque: {p[3]} un | Custo: R${p[4]:.2f} | Preço: R${p[5]:.2f}")
    return True

def adicionar_estoque(usuario_id):
    if listar_produtos(usuario_id):
        id_produto = int(input("\nDigite o ID do produto: "))
        qtd = int(input("Quantos itens chegaram? "))
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque + ? WHERE id = ? AND usuario_id = ?", (qtd, id_produto, usuario_id))
        conn.commit()
        conn.close()
        print("✅ Estoque atualizado!")

def editar_produto(usuario_id):
    if listar_produtos(usuario_id):
        id_produto = int(input("\nDigite o ID do produto que deseja editar: "))
        
        print("Digite os novos dados do produto:")
        nome = input("Novo Nome: ")
        tamanho = input("Novo Tamanho: ")
        quantidade = int(input("Novo Estoque Total: "))
        custo = float(input("Novo Custo: ").replace(",", "."))
        valor = float(input("Novo Preço de Venda: ").replace(",", "."))
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET nome=?, tamanho=?, quantidade_estoque=?, custo=?, valor_padrao=? WHERE id=? AND usuario_id=?", 
                       (nome, tamanho, quantidade, custo, valor, id_produto, usuario_id))
        conn.commit()
        conn.close()
        print("✅ Produto editado com sucesso!")


# ==========================================
#          MÓDULO DE VENDAS
# ==========================================

def criar_venda(usuario_id):
    print("\n--- REALIZAR VENDA ---")
    if not listar_produtos(usuario_id):
        return

    id_produto = int(input("\nDigite o ID do produto vendido: "))
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, tamanho, quantidade_estoque, custo, valor_padrao FROM produtos WHERE id = ? AND usuario_id = ?", (id_produto, usuario_id))
    produto = cursor.fetchone()
    
    if produto == None:
        print("❌ Produto não encontrado!")
        conn.close()
        return
        
    estoque_atual = produto[2]
    
    if estoque_atual <= 0:
        print("❌ Produto sem estoque!")
        conn.close()
        return

    quantidade_venda = int(input(f"Quantidade vendida (Máximo de {estoque_atual}): "))
    
    if quantidade_venda > estoque_atual:
        print("❌ Você não tem tudo isso no estoque!")
        conn.close()
        return
        
    # Salva a venda
    nome_completo = f"{produto[0]} (Tam: {produto[1]})"
    custo_un = produto[3]
    valor_un = produto[4]
    
    cursor.execute("INSERT INTO vendas (usuario_id, produto, quantidade, custo, valor) VALUES (?, ?, ?, ?, ?)", 
                   (usuario_id, nome_completo, quantidade_venda, custo_un, valor_un))
    
    # Subtrai do estoque
    cursor.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque - ? WHERE id = ?", (quantidade_venda, id_produto))
    
    conn.commit()
    conn.close()
    print("✅ Venda realizada e estoque descontado!")

def ler_vendas(usuario_id):
    print("\n--- LISTA DE VENDAS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, produto, quantidade, valor FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall()
    conn.close()
    
    if len(vendas) == 0:
        print("Nenhuma venda registrada.")
    else:
        for v in vendas:
            print(f"ID da Venda: {v[0]} | Produto: {v[1]} | Qtd: {v[2]} | Valor Unitário: R${v[3]:.2f}")

def deletar_venda(usuario_id):
    ler_vendas(usuario_id)
    id_venda = int(input("\nDigite o ID da venda que deseja excluir: "))
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vendas WHERE id = ? AND usuario_id = ?", (id_venda, usuario_id))
    conn.commit()
    conn.close()
    print("✅ Venda excluída!")

def calcular_financas(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT quantidade, custo, valor FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall()
    conn.close()
    
    if len(vendas) == 0:
        print("\n❌ Nenhuma venda para calcular.")
        return
        
    total_ganhos = sum(v[0] * v[2] for v in vendas)
    total_gastos = sum(v[0] * v[1] for v in vendas)
    lucro = total_ganhos - total_gastos
    
    print("\n==============================")
    print("      RESUMO FINANCEIRO")
    print("==============================")
    print(f"Dinheiro que entrou (Ganhos): R$ {total_ganhos:.2f}")
    print(f"Custo dos produtos (Gastos):  R$ {total_gastos:.2f}")
    print("------------------------------")
    print(f"LUCRO LÍQUIDO:                R$ {lucro:.2f}")
    print("==============================")