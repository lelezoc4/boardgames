from pathlib import Path
import random
import re
import sqlite3
import unicodedata

import pdfplumber
from openpyxl import load_workbook

def normalizar(nome):
    texto = unicodedata.normalize("NFKD", str(nome))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.upper().split())


pasta = Path(__file__).parent
restritos = pasta / "dados_restritos (projeto)"
banco = pasta / "boardgames.db"

if not banco.exists():
    raise FileNotFoundError("Banco não encontrado.")

# Relaciona os nomes aos IDs somente na memória.
planilha = load_workbook(
    restritos / "identificacao_alunos.xlsx",
    read_only=True
)
aba = planilha.active

colunas = {
    str(c.value).strip().lower(): c.column
    for c in aba[1]
    if c.value is not None
}

alunos = {}

for linha in range(2, aba.max_row + 1):
    nome = aba.cell(linha, colunas["nome"]).value
    identificador = aba.cell(linha, colunas["id"]).value

    if nome and str(nome).strip():
        chave = normalizar(nome)

        if chave in alunos:
            raise ValueError("Nome repetido na planilha.")

        if identificador is None or not str(identificador).strip():
            raise ValueError("Aluno sem ID na planilha.")

        alunos[chave] = str(identificador).strip()

planilha.close()

if len(alunos) != 33 or len(set(alunos.values())) != 33:
    raise ValueError("A planilha precisa conter 33 alunos com IDs únicos.")

arquivos = [
    ("fisica_2026.pdf", 31),
]

registros = []
encontrados = set()
maximos = (20, 30, 20)

# Extrai e valida todos os dados antes de abrir a transação.
for arquivo, quantidade_esperada in arquivos:
    quantidade = 0

    with pdfplumber.open(restritos / "pdfs" / arquivo) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text(x_tolerance=1) or ""

            for linha in texto.splitlines():
                if not re.match(r"^\s*\d{11}(?!\d)", linha):
                    continue

                restante = re.sub(r"^\s*\d{11}", "", linha).strip()
                primeira_nota = re.search(r"\d+,\d+", restante)

                if primeira_nota is None:
                    raise ValueError("Linha sem notas reconhecidas.")

                nome = normalizar(restante[:primeira_nota.start()])
                trecho = restante[primeira_nota.start():]
                valores = re.findall(r"\d+,\d+|--?", trecho)

                if nome not in alunos:
                    raise ValueError(
                        "Aluno do PDF sem correspondência na planilha restrita."
                    )
                
                identificador = alunos[nome]

                if identificador in encontrados:
                    raise ValueError("Aluno repetido nos PDFs.")

                if len(valores) < 15:
                    raise ValueError("Menos de 15 campos reconhecidos.")

                for bimestre, posicao in enumerate((4, 9, 14), start=1):
                    valor = valores[posicao]

                    if valor in ("-", "--"):
                        continue

                    nota = float(valor.replace(",", "."))
                    maximo = maximos[bimestre - 1]

                    if not 0 <= nota <= maximo:
                        raise ValueError("Nota fora do limite do bimestre.")

                    registros.append(
                        (identificador, 2026, bimestre, nota, maximo)
                    )

                encontrados.add(identificador)
                quantidade += 1

    if quantidade != quantidade_esperada:
        raise ValueError(
            f"{arquivo}: esperados {quantidade_esperada} alunos, "
            f"processados {quantidade}."
        )

if len(encontrados) != 31 or len(registros) != 93:
    raise ValueError("Esperávamos 31 alunos e 93 notas.")

# Evita preservar a ordem dos PDFs na inserção.
random.SystemRandom().shuffle(registros)

conexao = sqlite3.connect(banco)

try:
    conexao.execute("PRAGMA foreign_keys = ON")

    with conexao:

        conexao.execute("""
            INSERT INTO disciplinas (nome)
            VALUES (?)
            ON CONFLICT(nome) DO NOTHING
        """, ("FÍSICA",))

        disciplina = conexao.execute(
            "SELECT id FROM disciplinas WHERE nome = ?",
            ("FÍSICA",)
        ).fetchone()

        if disciplina is None:
            raise ValueError("Disciplina não cadastrada.")

        disciplina_id = disciplina[0]

        for aluno_id, ano, bimestre, nota, maximo in registros:
            existente = conexao.execute("""
                SELECT nota, pontuacao_maxima
                FROM notas
                WHERE aluno_id = ? AND disciplina_id = ?
                  AND ano = ? AND bimestre = ?
            """, (aluno_id, disciplina_id, ano, bimestre)).fetchone()

            if existente is not None:
                if existente != (nota, maximo):
                    raise ValueError(
                        "Existe uma nota diferente no banco. "
                        "Importação cancelada para conferência."
                    )
                continue

            conexao.execute("""
                INSERT INTO notas (
                    aluno_id, disciplina_id, ano, bimestre,
                    nota, pontuacao_maxima
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                aluno_id, disciplina_id, ano, bimestre, nota, maximo
            ))

        total = conexao.execute("""
            SELECT COUNT(*) FROM notas
            WHERE disciplina_id = ? AND ano = ? AND bimestre IN (1, 2, 3)
        """, (disciplina_id, 2026)).fetchone()[0]

finally:
    conexao.close()

print("Importação concluída!")
print(f"Alunos reconhecidos nos PDFs: {len(encontrados)}")
print(f"Notas conferidas nos PDFs: {len(registros)}")
print(f"Notas da disciplina no banco nos três bimestres: {total}")

