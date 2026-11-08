from pathlib import Path
import re
import pdfplumber

caminho = (
    Path(__file__).parent
    / "dados_restritos (projeto)"
    / "pdfs"
    / "fisica_2026.pdf"
)

with pdfplumber.open(caminho) as pdf:
    for numero, pagina in enumerate(pdf.pages, start=1):
        texto = pagina.extract_text(x_tolerance=1) or ""

        linhas = [
            linha
            for linha in texto.splitlines()
            if re.match(r"^\s*\d{11}(?!\d)", linha)
        ]

        print(f"Página {numero}: {len(linhas)} registros encontrados.")

        for indice, linha in enumerate(linhas, start=1):
            restante = re.sub(r"^\s*\d{11}", "", linha).strip()

            # Retira o nome antes de procurar números e traços.
            inicio = re.search(r"\d+,\d+|(?<!\S)--?(?!\S)", restante)

            if inicio is None:
                raise ValueError("Não foi possível localizar as notas.")

            trecho = restante[inicio.start():]
            campos = re.findall(r"\d+,\d+|--?", trecho)

            if len(campos) < 15:
                raise ValueError(
                    f"Registro {indice}: apenas {len(campos)} campos reconhecidos."
                )

            totais = [
                "indisponível" if campos[posicao] in ("-", "--")
                else campos[posicao]
                for posicao in (4, 9, 14)
            ]

            print(f"Registro {indice}: estrutura de notas conferida.")