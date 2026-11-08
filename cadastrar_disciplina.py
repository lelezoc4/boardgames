import sqlite3
from pathlib import Path

caminho = Path(__file__).parent / "boardgames.db"

if not caminho.exists():
    raise FileNotFoundError("O banco boardgames.db não foi encontrado.")

with sqlite3.connect(caminho) as conexao:
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    conexao.execute("""
        INSERT INTO disciplinas (nome)
        VALUES (?)
        ON CONFLICT(nome) DO NOTHING
    """, ("LABORATÓRIO DE LINGUAGEM DE PROGRAMAÇÃO II",))

print("Disciplina cadastrada!")