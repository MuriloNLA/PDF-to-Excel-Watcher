# PDF to Excel — Extrator e Monitor de Pedidos

> Conjunto de scripts Python que lê PDFs de pedidos, extrai os dados via expressões regulares e os registra automaticamente em uma planilha Excel (.xlsx). Pode ser executado manualmente ou em modo de monitoramento contínuo de pasta.

---

## Motivação

O processo manual de copiar dados de PDFs de pedidos para planilhas era repetitivo e sujeito a erros. Esses scripts automatizam completamente essa tarefa — basta apontar para um PDF, uma pasta inteira, ou deixar o monitor rodando em segundo plano para processar arquivos assim que chegarem.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| `exportarpedidos.py` | Extração e registro dos dados do PDF na planilha |
| `watcher.py` | Monitor de pasta — processa novos PDFs automaticamente |

---

## Funcionalidades

- Extrai automaticamente: data, hora, tipo de pedido, cliente, frete (CIF/FOB), vendedor e quantidade de itens
- Suporte a **processamento em lote** — aceita uma pasta inteira de PDFs
- **Evita duplicatas** — verifica pelo nome do arquivo se o PDF já foi processado
- Cria a planilha automaticamente se não existir, com cabeçalho configurado
- IDs sequenciais e automáticos para cada registro
- Limpeza inteligente de texto — remove ruídos comuns em PDFs (CNPJ, CPF, telefone colados ao nome, etc.)
- **Modo watcher** — monitora uma pasta em tempo real e processa novos PDFs assim que são salvos
- Aguarda o arquivo estar completamente gravado antes de processar (evita erros de leitura parcial)

---

## Tecnologias

| Biblioteca | Uso |
|---|---|
| `pdfplumber` | Extração de texto dos PDFs |
| `openpyxl` | Leitura e escrita da planilha Excel |
| `watchdog` | Monitoramento de eventos do sistema de arquivos |
| `re` | Expressões regulares para parsing dos dados |
| `pathlib` | Manipulação de caminhos de arquivo |

---

## Instalação

```bash
pip install pdfplumber openpyxl watchdog
```

---

## Uso

**Processar um único PDF:**
```bash
python exportarpedidos.py pedido.pdf planilha.xlsx
```

**Processar uma pasta inteira:**
```bash
python exportarpedidos.py ./pedidos/ planilha.xlsx
```

**Monitoramento contínuo de pasta:**
```bash
python watcher.py ./pedidos/ planilha.xlsx
```

---

## Estrutura da Planilha Gerada

| ID | Data | Hora | Tipo | Cliente | Frete | Vendedor | QuantItem | TempoLevado |
|---|---|---|---|---|---|---|---|---|
| 1 | 15/05/2026 | 09:30 | Venda Normal | Cliente Exemplo | CIF | Vendedor Exemplo | 3 | |

---

## O que eu melhoraria

- Interface gráfica (GUI) para selecionar arquivos sem usar o terminal
- Suporte a outros layouts de PDF além do padrão atual
- Exportação também para Google Sheets via API
- Notificação desktop ao processar um novo arquivo

---

> Projeto desenvolvido para uso interno. Disponibilizado de forma genérica, sem dados sensíveis.
