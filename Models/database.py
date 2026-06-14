import sqlite3

# O banco de dados será salvo na mesma pasta do projeto
DB_PATH = 'banco.db'

def conectar():
    return sqlite3.connect(DB_PATH)

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Tabela de Usuários
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE NOT NULL, senha TEXT NOT NULL)")
    
    # 2. Tabela de Produtos (Estoque)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            quantidade_estoque INTEGER NOT NULL,
            custo REAL NOT NULL,
            valor_padrao REAL NOT NULL
        )
    """)

    # 3. Tabela de Vendas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            custo REAL NOT NULL,
            valor REAL NOT NULL
        )
    """)
    
    # Cria o admin se não existir
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ("admin", "1234"))
        
    conn.commit()
    conn.close()