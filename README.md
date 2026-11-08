# BoardGames — Organização de Dados

Sistema em Python e SQLite desenvolvido para apoiar o projeto **BoardGames: Desenvolvendo o Raciocínio Lógico e Quantitativo de Meninas por meio de Jogos de Tabuleiro**.

O sistema organiza dados acadêmicos por identificadores aleatórios, permitindo relacionar informações de um mesmo estudante sem armazenar nomes no banco.

## Estado atual

- Geração de IDs aleatórios e únicos.
- Cadastro dos alunos por ID.
- Cadastro de disciplinas.
- Extração de notas de PDFs.
- Importação de notas por disciplina, ano e bimestre.
- Verificação de correspondências e duplicações.
- Consultas de quantidade de notas e valores mínimos e máximos.

A base local reúne 33 alunos cadastrados e 867 notas de nove disciplinas, referentes aos três primeiros bimestres de 2026. A quantidade de alunos com notas varia por disciplina devido a dispensas e dados indisponíveis.

Os dados reais não estão incluídos neste repositório.

## Tecnologias

- Python
- SQLite, pelo módulo `sqlite3` do Python
- OpenPyXL
- pdfplumber

## Organização do banco

| Tabela | Conteúdo |
|---|---|
| `alunos` | Identificadores dos estudantes |
| `disciplinas` | Identificadores e nomes das disciplinas |
| `notas` | Aluno, disciplina, ano, bimestre, nota e pontuação máxima |

A tabela `notas` impede registros duplicados para a mesma combinação de aluno, disciplina, ano e bimestre.

## Organização dos scripts

| Arquivo | Função |
|---|---|
| `criar_banco.py` | Cria o banco e a tabela de alunos |
| `cadastrar_disciplina.py` | Cria a tabela de disciplinas e cadastra uma disciplina |
| `criar_tabela_notas.py` | Cria a tabela de notas |
| `gerar_ids.py` | Preenche IDs vazios na planilha restrita |
| `cadastrar_alunos.py` | Insere os IDs no banco em ordem embaralhada |
| `ler_pdf.py` | Verifica a estrutura dos campos extraídos do PDF |
| `conferir_alunos_pdfs.py` | Compara os alunos dos PDFs com a planilha |
| `importar_notas.py` | Valida e importa as notas |
| `consultar_banco.py` | Consulta a estrutura da tabela de alunos |
| `conferir_notas.py` | Consulta contagens, mínimos e máximos por bimestre |

## Instalação

No terminal, dentro da pasta do projeto:

```powershell
python -m venv .venv
```

Instale as dependências no ambiente virtual:

```powershell
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
```

No VS Code, selecione o interpretador localizado em `.venv\Scripts\python.exe`.

## Preparação do banco

Execute nesta ordem:

```powershell
& '.\.venv\Scripts\python.exe' .\criar_banco.py
& '.\.venv\Scripts\python.exe' .\cadastrar_disciplina.py
& '.\.venv\Scripts\python.exe' .\criar_tabela_notas.py
```

Esses comandos preparam as tabelas, mas não fornecem os dados restritos necessários às importações.

## Arquivos locais necessários

Para uso autorizado com dados reais, os scripts esperam:

- Uma pasta `dados_restritos (projeto)` na pasta do projeto.
- Dentro dela, a planilha `identificacao_alunos.xlsx`.
- Na primeira aba da planilha, as colunas `nome` e `id`.
- Uma subpasta `pdfs`, contendo os documentos de notas.

A planilha de correspondência entre nomes e IDs deve permanecer restrita. Os IDs existentes devem ser preservados nas atualizações.

## Importação de notas

Os scripts ainda possuem configurações específicas para a turma e para cada formato de PDF.

Na versão atual:

- `importar_notas.py` está configurado para Física.
- `cadastrar_disciplina.py` e `conferir_notas.py` estão configurados para Laboratório de Linguagem de Programação II.
- A planilha de alunos é validada considerando 33 estudantes.

Antes de importar outra disciplina, ajuste o nome da disciplina, os PDFs, as quantidades esperadas e as posições dos totais dos bimestres.

O fluxo de trabalho é:

1. Conferir o cabeçalho e a estrutura do PDF.
2. Testar a leitura com `ler_pdf.py`.
3. Comparar os totais extraídos com o documento original.
4. Conferir os alunos com `conferir_alunos_pdfs.py`.
5. Gerar IDs apenas para alunos ainda sem identificador.
6. Cadastrar os IDs no banco.
7. Executar a importação.
8. Conferir os dados gravados.

A importação preserva registros iguais já existentes. Caso encontre uma nota diferente para um registro já cadastrado, cancela a transação para permitir a conferência.

## Tratamento das notas

| Bimestre | Pontuação máxima |
|---|---:|
| 1º | 20 |
| 2º | 30 |
| 3º | 20 |
| 4º | 30 |

No levantamento atual, apenas os três primeiros bimestres foram importados, totalizando 70 pontos possíveis.

- Notas zero são preservadas.
- Totais indisponíveis, indicados por traços, não são convertidos em zero.
- Não são calculados totais ausentes a partir das atividades.
- Alunos dispensados permanecem cadastrados, sem notas na disciplina.
- As dispensas ainda não possuem um campo próprio no banco.

## Privacidade

Os nomes são substituídos por IDs aleatórios, e a ordem dos registros é embaralhada antes da inserção.

Esse procedimento constitui pseudonimização: não garante, sozinho, que os dados sejam anônimos.

Não fazem parte deste repositório:

- Nomes e matrículas dos estudantes.
- Planilhas de correspondência entre nomes e IDs.
- PDFs originais.
- Banco SQLite com dados reais.
- Relatórios individuais.

O `.gitignore` ajuda a evitar o versionamento desses arquivos pelo Git. No upload pelo site do GitHub, os arquivos devem ser selecionados e revisados manualmente.

## Próximas etapas

- Registrar dispensas e situações de dados ausentes.
- Incorporar respostas de formulários.
- Registrar encontros e participações.
- Organizar as configurações das importações por disciplina.
- Desenvolver análises descritivas com Pandas.
- Criar gráficos com Matplotlib e Seaborn.
- Preparar exemplos fictícios para demonstração.

As análises deverão considerar dados ausentes e diferentes escalas de pontuação. Comparações entre participantes e não participantes não demonstram, por si só, que os jogos causaram diferenças de desempenho.
