from Models.database import inicializar_banco
from login.auth import realizar_login, cadastrar_usuario
from CRUD.operacoes import criar_venda, ler_vendas, deletar_venda, calcular_financas, gerenciar_produtos

def menu_principal(usuario_id, username):
    while True:
        print(f"\n=== BEM-VINDO, {username} ===")
        print("1. Gerenciar Produtos e Estoque")
        print("2. Realizar Venda")
        print("3. Listar Vendas Feitas")
        print("4. Excluir uma Venda")
        print("5. Ver Resumo de Lucros")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            gerenciar_produtos(usuario_id)
        elif opcao == '2':
            criar_venda(usuario_id)
        elif opcao == '3':
            ler_vendas(usuario_id)
        elif opcao == '4':
            deletar_venda(usuario_id)
        elif opcao == '5':
            calcular_financas(usuario_id)
        elif opcao == '6':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    inicializar_banco()
    
    while True:
        print("\n--- TELA INICIAL ---")
        print("1. Fazer Login")
        print("2. Criar Conta")
        print("3. Fechar")
        
        inicio = input("Opção: ")
        
        if inicio == '1':
            resultado = realizar_login()
            if resultado: 
                usuario_id, nome = resultado
                menu_principal(usuario_id, nome)
        elif inicio == '2':
            cadastrar_usuario()
        elif inicio == '3':
            break
        else:
            print("Opção inválida!")