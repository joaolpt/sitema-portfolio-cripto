import sqlite3

DB_NAME = "portfolio.db"

def get_db_connection():
    """Função responsável por criar uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Função para criar a tabela principal do banco de dados, caso ela não exista."""
    conn = get_db_connection()
    comando_sql = '''
    CREATE TABLE IF NOT EXISTS ativos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_moeda TEXT NOT NULL,
        sigla TEXT NOT NULL,
        quantidade REAL NOT NULL,
        valor_investido REAL NOT NULL,
        data_aporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    conn.execute(comando_sql)
    conn.commit()
    conn.close()

    print("Banco de dados e tabelas inicializados com sucesso!!")

if __name__ == "__main__":
    init_db()