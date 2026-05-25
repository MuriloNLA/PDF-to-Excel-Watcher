# watcher.py
# Monitora uma pasta e processa automaticamente novos PDFs,
# sem duplicar entradas ja existentes na planilha.
#
# Dependencias:
#     pip install pdfplumber openpyxl watchdog
#
# Uso no terminal:
#     python watcher.py <pasta_pedidos> <planilha.xlsx>

import sys
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exportarpedidos import processar_pdf


def aguardar_arquivo_pronto(caminho, tentativas=10, intervalo=2):
    """Aguarda o arquivo estar completamente salvo e acessivel."""
    for i in range(tentativas):
        try:
            tamanho_antes = os.path.getsize(caminho)
            time.sleep(intervalo)
            tamanho_depois = os.path.getsize(caminho)
            if tamanho_antes == tamanho_depois and tamanho_depois > 0:
                with open(caminho, "rb"):
                    pass
                return True
        except (OSError, PermissionError):
            print(f"  [AGUARDANDO] Arquivo ainda nao pronto, tentativa {i + 1}/{tentativas}...")
            time.sleep(intervalo)
    return False


class PDFHandler(FileSystemEventHandler):
    def __init__(self, caminho_xlsx):
        self.caminho_xlsx = caminho_xlsx

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(".pdf"):
            nome = Path(event.src_path).name
            print(f"\n[DETECTADO] Novo arquivo: {nome}")

            if aguardar_arquivo_pronto(event.src_path):
                try:
                    processar_pdf(event.src_path, self.caminho_xlsx)
                except Exception as e:
                    print(f"  [ERRO] {e}")
            else:
                print(f"  [ERRO] Arquivo nao ficou pronto a tempo: {nome}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python watcher.py <pasta_pedidos> <planilha.xlsx>")
        return

    pasta    = sys.argv[1]
    planilha = sys.argv[2]

    if not os.path.isdir(pasta):
        print(f"[ERRO] Pasta nao encontrada: {pasta}")
        return

    print("=" * 60)
    print("  PDF WATCHER — Monitoramento Automatico de Pedidos")
    print("=" * 60)
    print(f"  Pasta:    {pasta}")
    print(f"  Planilha: {planilha}")
    print("  Aguardando novos PDFs... (Ctrl+C para parar)")
    print("=" * 60)

    handler  = PDFHandler(planilha)
    observer = Observer()
    observer.schedule(handler, pasta, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[INFO] Monitoramento encerrado.")
    observer.join()


if __name__ == "__main__":
    main()
