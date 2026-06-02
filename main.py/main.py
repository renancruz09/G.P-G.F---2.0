from Models.database import inicializar_banco
from login.auth import realizar_login, cadastrar_usuario
from CRUD.operacoes import criar_venda, ler_vendas, atualizar_venda, deletar_venda

def menu_principal(usuario_logado):
    while True:
        print(f"\n{'='*30}")
        print(f"SISTEMA G.P-G.F - USUÁRIO: {usuario_logado}")
        print(f"{'='*30}")
        print("1. Cadastrar Venda (Create)")
        print("2. Listar Vendas (Read)")
        print("3. Editar Venda (Update)")
        print("4. Excluir Venda (Delete)")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            criar_venda(usuario_logado)
        elif opcao == '2':
            ler_vendas()
        elif opcao == '3':
            atualizar_venda(usuario_logado)
        elif opcao == '4':
            deletar_venda()
        elif opcao == '5':
            print(f"Até logo, {usuario_logado}!")
            break
        else:
            print("Opção inválida!")

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
            user = realizar_login()
            if user:
                menu_principal(user)
                break
        elif inicio == '2':
            cadastrar_usuario()
        elif inicio == '3':
            break
