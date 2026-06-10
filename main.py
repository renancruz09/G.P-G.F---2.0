from Models.database import inicializar_banco
from login.auth import realizar_login, cadastrar_usuario
from CRUD.operacoes import criar_venda, ler_vendas, atualizar_venda, deletar_venda, calcular_financas

def menu_principal(usuario_id, username):
    while True:
        print(f"\nSISTEMA G.P-G.F - USUÁRIO: {username}")
        print("1. Cadastrar | 2. Listar | 3. Editar | 4. Excluir | 5. Finanças | 6. Sair")
        opcao = input("Opção: ").strip()
        if opcao == '1': criar_venda(usuario_id)
        elif opcao == '2': ler_vendas(usuario_id)
        elif opcao == '3': atualizar_venda(usuario_id)
        elif opcao == '4': deletar_venda(usuario_id)
        elif opcao == '5': calcular_financas(usuario_id)
        elif opcao == '6': break
        else: print("❌ Inválida!")

if __name__ == "__main__":
    inicializar_banco()
    while True:
        print("\n1. Login | 2. Cadastro | 3. Sair")
        inicio = input("Opção: ").strip()
        if inicio == '1':
            uid, uname = realizar_login()
            if uid: menu_principal(uid, uname); break
        elif inicio == '2': cadastrar_usuario()
        elif inicio == '3': break
