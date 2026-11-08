import sqlite3
from pathlib import Path

caminho = Path(__file__).parent / "boardgames.db"
conexao = sqlite3.connect(caminho)

conexao.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id TEXT PRIMARY KEY NOT NULL
    )
""")

conexao.commit()
conexao.close()

print("Tabela alunos pronta!")