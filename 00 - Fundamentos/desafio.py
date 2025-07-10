import getpass
import datetime

usuarios = {}  # {"usuario": {"senha": "123", "saldo": 0, "extrato": []}}

# === Credenciais administrador ===
admin_login = "admin"
admin_senha = "admin123"

# === Utilitário ===
def agora():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

# === Funções de Usuário ===
def cadastrar_usuario():
    print("\n=== Cadastro de Usuário ===")
    usuario = input("Escolha um nome de usuário: ")
    if usuario in usuarios:
        print("Usuário já existe!")
        return

    senha = getpass.getpass("Crie uma senha: ")
    usuarios[usuario] = {
        "senha": senha,
        "saldo": 0,
        "extrato": []
    }
    print("Usuário cadastrado com sucesso!")

def login():
    print("\n=== Login ===")
    usuario = input("Usuário: ")
    senha = getpass.getpass("Senha: ")

    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        print(f"Bem-vindo(a), {usuario}!")
        menu_usuario(usuario)
    else:
        print("Usuário ou senha incorretos!")

def menu_usuario(usuario):
    while True:
        print(f"\n=== Seja bem-vindo(a) {usuario} ===")
        print("[1] Depositar")
        print("[2] Sacar")
        print("[3] Extrato")
        print("[4] Transferência")
        print("[0] Logout")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                valor = float(input("Valor para depósito: R$ "))
                if valor > 0:
                    usuarios[usuario]["saldo"] += valor
                    usuarios[usuario]["extrato"].append(f"[{agora()}] Depósito: R$ {valor:.2f}")
                    print("Depósito realizado com sucesso!")
                else:
                    print("Valor inválido!")
            except ValueError:
                print("Entrada inválida. Use apenas números.")

        elif opcao == "2":
            try:
                valor = float(input("Valor para saque: R$ "))
                saldo_atual = usuarios[usuario]["saldo"]
                if valor > 0 and valor <= saldo_atual:
                    usuarios[usuario]["saldo"] -= valor
                    usuarios[usuario]["extrato"].append(f"[{agora()}] Saque:    R$ {valor:.2f}")
                    print("Saque realizado com sucesso!")
                else:
                    print("Saldo insuficiente ou valor inválido!")
            except ValueError:
                print("Entrada inválida. Use apenas números.")

        elif opcao == "3":
            print("\n=== Extrato ===")
            extrato = usuarios[usuario]["extrato"]
            if extrato:
                for item in extrato:
                    print(item)
            else:
                print("Nenhuma movimentação.")
            print(f"Saldo atual: R$ {usuarios[usuario]['saldo']:.2f}")

        elif opcao == "4":
            destinatario = input("Digite o nome do usuário destinatário: ")
            if destinatario not in usuarios:
                print("Usuário destinatário não encontrado.")
                continue
            if destinatario == usuario:
                print("Não é possível transferir para você mesmo.")
                continue

            try:
                valor = float(input("Valor da transferência: R$ "))
                if valor > 0 and usuarios[usuario]["saldo"] >= valor:
                    usuarios[usuario]["saldo"] -= valor
                    usuarios[destinatario]["saldo"] += valor
                    usuarios[usuario]["extrato"].append(
                        f"[{agora()}] Transferência para {destinatario}: R$ {valor:.2f}"
                    )
                    usuarios[destinatario]["extrato"].append(
                        f"[{agora()}] Transferência de {usuario}: R$ {valor:.2f}"
                    )
                    print("Transferência realizada com sucesso!")
                else:
                    print("Saldo insuficiente ou valor inválido!")
            except ValueError:
                print("Entrada inválida. Use apenas números.")

        elif opcao == "0":
            print("Logout efetuado.")
            break
        else:
            print("Opção inválida.")

# === Funções do Administrador ===
def menu_admin():
    while True:
        print("\n=== MENU ADMINISTRADOR ===")

        if usuarios:
            print("\nUsuários cadastrados:")
            for nome, dados in usuarios.items():
                print(f"- {nome} | Saldo: R$ {dados['saldo']:.2f} | Movimentações: {len(dados['extrato'])}")
        else:
            print("\nNenhum usuário cadastrado.")

        print("\n[1] Alterar senha de um usuário")
        print("[2] Excluir usuário")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            usuario = input("Digite o nome do usuário: ")
            if usuario in usuarios:
                nova_senha = getpass.getpass("Nova senha: ")
                usuarios[usuario]["senha"] = nova_senha
                print("Senha atualizada com sucesso!")
            else:
                print("Usuário não encontrado.")

        elif opcao == "2":
            usuario = input("Nome do usuário a excluir: ")
            if usuario in usuarios:
                confirm = input(f"Tem certeza que deseja excluir '{usuario}'? (s/n): ").lower()
                if confirm == 's':
                    del usuarios[usuario]
                    print("Usuário excluído.")
                else:
                    print("Operação cancelada.")
            else:
                print("Usuário não encontrado.")

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

# === Início do sistema ===
print("=== BEM-VINDO AO SEU BANCO ===")
while True:
    print("\n=== MENU PRINCIPAL ===")
    print("[1] Cadastrar novo usuário")
    print("[2] Login de usuário")
    print("[3] Acesso do administrador")
    print("[0] Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        login()
    elif opcao == "3":
        login_admin = input("Login do administrador: ")
        senha_admin = getpass.getpass("Senha do administrador: ")

        if login_admin == admin_login and senha_admin == admin_senha:
            print("Acesso de administrador concedido.")
            menu_admin()
        else:
            print("Login ou senha de administrador incorretos!")
    elif opcao == "0":
        print("Encerrando sistema...")
        break
    else:
        print("Opção inválida.")
