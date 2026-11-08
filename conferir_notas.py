import sqlite3
from pathlib import Path

caminho = Path(__file__).parent / "boardgames.db"

if not caminho.exists():
    raise FileNotFoundError("Banco não encontrado.")

conexao = sqlite3.connect(caminho)

try:
    resultados = conexao.execute("""
        SELECT
            notas.bimestre,
            COUNT(*),
            MIN(notas.nota),
            MAX(notas.nota),
            notas.pontuacao_maxima
        FROM notas
        JOIN disciplinas
            ON disciplinas.id = notas.disciplina_id
        WHERE disciplinas.nome = ?
          AND notas.ano = 2026
        GROUP BY notas.bimestre, notas.pontuacao_maxima
        ORDER BY notas.bimestre
    """, ("LABORATÓRIO DE LINGUAGEM DE PROGRAMAÇÃO II",)).fetchall()

    for bimestre, quantidade, menor, maior, maximo in resultados:
        print(
            f"{bimestre}º bimestre: {quantidade} notas | "
            f"menor: {menor} | maior: {maior} | "
            f"pontos possíveis: {maximo}"
        )

finally:
    conexao.close()