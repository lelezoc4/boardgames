import sqlite3
from pathlib import Path

caminho = Path(__file__).parent / "boardgames.db"

if not caminho.exists():
    raise FileNotFoundError("O banco boardgames.db não foi encontrado.")

with sqlite3.connect(caminho) as conexao:
    # Ativa a verificação dos vínculos entre as tabelas.
    conexao.execute("PRAGMA foreign_keys = ON")

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            aluno_id TEXT NOT NULL,
            disciplina_id INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            bimestre INTEGER NOT NULL
                CHECK (bimestre BETWEEN 1 AND 4),
            nota REAL NOT NULL,
            pontuacao_maxima REAL NOT NULL
                CHECK (pontuacao_maxima > 0),

            PRIMARY KEY (
                aluno_id, disciplina_id, ano, bimestre
            ),

            FOREIGN KEY (aluno_id) REFERENCES alunos(id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),

            CHECK (nota >= 0 AND nota <= pontuacao_maxima)
        )
    """)

print("Tabela notas criada!")