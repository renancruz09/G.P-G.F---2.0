from Models.database import inicializar_banco
from login.auth import realizar_login, cadastrar_usuario
from CRUD.operacoes import criar_venda, ler_vendas, atualizar_venda, deletar_venda, calcular_financas

def menu_principal(usuario_id, username):
    while True:
        print(f"\n{'='*30}")
        print(f"SISTEMA G.P-G.F - USUÁRIO: {username}")
        print(f"{'='*30}")
        print("1. Cadastrar Venda")
        print("2. Listar Vendas")
        print("3. Editar Venda")
        print("4. Excluir Venda")
        print("5. Resumo Financeiro")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        # ... lógica do menu ...
