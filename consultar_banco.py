import sqlite3
from pathlib import Path

caminho = Path(__file__).parent / "boardgames.db"
conexao = sqlite3.connect(caminho)

colunas = conexao.execute("PRAGMA table_info(alunos)").fetchall()

for coluna in colunas:
    print(coluna)

conexao.close()