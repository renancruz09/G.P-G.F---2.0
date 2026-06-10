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
        
        if opcao == '1':
            criar_venda(usuario_id)
        elif opcao == '2':
            ler_vendas(usuario_id)
        elif opcao == '3':
            atualizar_venda(usuario_id)
        elif opcao == '4':
            deletar_venda(usuario_id)
        elif opcao == '5':
            calcular_financas(usuario_id)
        elif opcao == '6':
            print(f"Até logo, {username}!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    inicializar_banco()
    
    while True:
        print("\n" + "#"*30)
        print("   BEM-VINDO AO SISTEMA")
        print("#"*30)
        print("1. Login")
        print("2. Primeiro Acesso (Cadastrar)")
        print("3. Fechar Programa")
        
        inicio = input("\nOpção: ").strip()
        
        if inicio == '1':
            uid, uname = realizar_login()
            if uid and uname:
                menu_principal(uid, uname)
                break # Sai do loop inicial após o uso
        elif inicio == '2':
            cadastrar_usuario()
        elif inicio == '3':
            print("Encerrando sistema...")
            break
