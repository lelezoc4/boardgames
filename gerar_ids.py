from pathlib import Path
from uuid import uuid4
from openpyxl import load_workbook

# Localiza a planilha restrita.
pasta = Path(__file__).parent
caminho = pasta / "dados_restritos (projeto)" / "identificacao_alunos.xlsx"

planilha = load_workbook(caminho)
aba = planilha.active

# Localiza as colunas pelos títulos da primeira linha.
colunas = {
    str(celula.value).strip().lower(): celula.column
    for celula in aba[1]
    if celula.value is not None
}

if "nome" not in colunas or "id" not in colunas:
    raise ValueError("A primeira linha precisa ter os títulos nome e id.")

coluna_nome = colunas["nome"]
coluna_id = colunas["id"]

# Seleciona as linhas que têm nome preenchido.
linhas = [
    linha
    for linha in range(2, aba.max_row + 1)
    if str(aba.cell(linha, coluna_nome).value or "").strip()
]

if len(linhas) != 33:
    raise ValueError(f"Foram encontrados {len(linhas)} alunos; esperávamos 33.")

# Confere os IDs existentes antes de fazer alterações.
ids = set()

for linha in linhas:
    valor = aba.cell(linha, coluna_id).value

    if valor is not None and str(valor).strip():
        identificador = str(valor).strip()

        if identificador in ids:
            raise ValueError("Existem IDs repetidos na planilha.")

        ids.add(identificador)

# Preenche apenas os IDs vazios, preservando os já existentes.
novos = 0

for linha in linhas:
    celula = aba.cell(linha, coluna_id)

    if celula.value is None or not str(celula.value).strip():
        identificador = uuid4().hex

        while identificador in ids:
            identificador = uuid4().hex

        celula.value = identificador
        ids.add(identificador)
        novos += 1

planilha.save(caminho)
planilha.close()

print(f"Alunos encontrados: {len(linhas)}")
print(f"Novos IDs gerados: {novos}")
print("Planilha salva!")