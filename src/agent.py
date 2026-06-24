import datetime
from src.analyzer import analyze_log


def handle_new_log_event(file_path):
    """
    Função executada sempre que uma modificação é detectada.
    """
    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\n[{hora_atual}] 🚨 ALERTA: Modificação detectada em {file_path}")

    try:
        # Lê apenas as últimas 10 linhas do log para não reanalisar o histórico inteiro
        with open(file_path, "r", errors="ignore") as f:
            lines = f.readlines()
            recent_logs = "".join(lines[-10:])

        if recent_logs.strip():
            print("[⏳] Acionando inteligência para triagem do evento...")
            analyze_log(recent_logs)
        else:
            print("[-] Evento vazio ignorado.")

    except Exception as e:
        print(f"[✗] Falha no processamento local do Agente: {e}")
