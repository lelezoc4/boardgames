from pathlib import Path
from collections import Counter
import re
import unicodedata

import pdfplumber
from openpyxl import load_workbook


def normalizar(nome):
    # Ignora diferenças de acentos, maiúsculas e espaços.
    texto = unicodedata.normalize("NFKD", str(nome))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.upper().split())


pasta = Path(__file__).parent
restritos = pasta / "dados_restritos (projeto)"

# Lê os nomes da planilha.
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

nomes_planilha = {}

for linha in range(2, aba.max_row + 1):
    nome = aba.cell(linha, colunas["nome"]).value

    if nome and str(nome).strip():
        chave = normalizar(nome)

        if chave in nomes_planilha:
            raise ValueError("Há nomes iguais na planilha. Precisamos conferir.")

        nomes_planilha[chave] = str(nome).strip()

planilha.close()

# Lê os PDFs configurados.
arquivos = [
    "fisica_2026.pdf",
]

nomes_pdfs = []

for arquivo in arquivos:
    with pdfplumber.open(restritos / "pdfs" / arquivo) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text(x_tolerance=1) or ""

            for linha in texto.splitlines():
                if not re.match(r"^\s*\d{11}(?!\d)", linha):
                    continue

                # Remove a matrícula e separa o nome das notas.
                restante = re.sub(r"^\s*\d{11}", "", linha).strip()
                primeira_nota = re.search(r"\d+,\d+", restante)

                if primeira_nota is None:
                    raise ValueError("Uma linha de aluno ficou sem notas reconhecidas.")

                nome = restante[:primeira_nota.start()].strip()
                nomes_pdfs.append(normalizar(nome))

contagem = Counter(nomes_pdfs)

faltantes = set(nomes_planilha) - set(contagem)
desconhecidos = set(contagem) - set(nomes_planilha)
repetidos = {nome for nome, total in contagem.items() if total > 1}

print(f"Alunos na planilha: {len(nomes_planilha)}")
print(f"Registros nos PDFs: {len(nomes_pdfs)}")
print(f"Alunos distintos nos PDFs: {len(contagem)}")
print(f"Nomes repetidos nos PDFs: {len(repetidos)}")
print(f"Nomes dos PDFs sem correspondência na planilha: {len(desconhecidos)}")
print(f"Alunos da planilha ausentes nos PDFs: {len(faltantes)}")

