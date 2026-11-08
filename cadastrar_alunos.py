import random
import sqlite3
from pathlib import Path
from openpyxl import load_workbook

pasta = Path(__file__).parent

caminho_planilha = (
    pasta / "dados_restritos (projeto)" / "identificacao_alunos.xlsx"
)
caminho_banco = pasta / "boardgames.db"

planilha = load_workbook(caminho_planilha, read_only=True)
aba = planilha.active

colunas = {
    str(celula.value).strip().lower(): celula.column
    for celula in aba[1]
    if celula.value is not None
}

ids = []

for linha in range(2, aba.max_row + 1):
    nome = aba.cell(linha, colunas["nome"]).value

    if nome is None or not str(nome).strip():
        continue

    valor = aba.cell(linha, colunas["id"]).value

    if valor is None or not str(valor).strip():
        raise ValueError("Existe aluno sem ID na planilha.")

    ids.append(str(valor).strip())

planilha.close()

if len(ids) != 33 or len(set(ids)) != 33:
    raise ValueError("Precisamos de exatamente 33 IDs únicos.")

if not caminho_banco.exists():
    raise FileNotFoundError("O arquivo boardgames.db não foi encontrado.")

# Embaralha os IDs antes de cadastrar.
random.SystemRandom().shuffle(ids)

with sqlite3.connect(caminho_banco) as conexao:
    existentes = {
        linha[0]
        for linha in conexao.execute("SELECT id FROM alunos")
    }

    if existentes - set(ids):
        raise ValueError("O banco contém IDs diferentes dos da planilha.")

    novos = [(identificador,) for identificador in ids
             if identificador not in existentes]

    conexao.executemany(
        "INSERT INTO alunos (id) VALUES (?)",
        novos
    )

    total = conexao.execute(
        "SELECT COUNT(*) FROM alunos"
    ).fetchone()[0]

print(f"Novos alunos cadastrados: {len(novos)}")
print(f"Total de alunos no banco: {total}")