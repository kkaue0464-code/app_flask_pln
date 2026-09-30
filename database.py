import sqlite3

DB_NAME = "sentimentos.db"

def init_db():
    """Inicializa o banco de dados e cria a tabela se não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            sentimento TEXT NOT NULL,
            polaridade REAL NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def salvar_comentario(texto, sentimento, polaridade):
    """Salva a análise do comentário de forma segura no SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comentarios (texto, sentimento, polaridade) VALUES (?, ?, ?)",
        (texto, sentimento, polaridade)
    )
    conn.commit()
    conn.close()

def obter_historico():
    """Recupera os últimos comentários analisados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT texto, sentimento, polaridade, data FROM comentarios ORDER BY id DESC LIMIT 10")
    registros = cursor.fetchall()
    conn.close()
    return registros