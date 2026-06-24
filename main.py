import sys
import os
from src.watcher import start_watching
from src.agent import handle_new_log_event


def print_banner():
    banner = """
    =========================================
      🛡️  AGENTE KLA - MONITORAMENTO ATIVO
    =========================================
    [✓] Sistemas online.
    [✓] Cérebro IA (Groq) conectado.
    """
    print(banner)


if __name__ == "__main__":
    print_banner()

    # Opcional: passa o nome do log por argumento, ou usa um padrão
    log_file = sys.argv[1] if len(sys.argv) > 1 else "meu_log_de_teste.log"

    if not os.path.exists(log_file):
        print(f"[!] Aviso: Criando arquivo de log vazio para monitoramento: {log_file}")
        open(log_file, "a").close()

    print(f"[*] Modo vigia ativado em: {os.path.abspath(log_file)}")
    print("Pressione Ctrl+C para encerrar.\n")

    start_watching(log_file, handle_new_log_event)
