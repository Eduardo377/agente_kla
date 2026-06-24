import os
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Instancia o cliente da Groq
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("[!] Erro crítico: GROQ_API_KEY não encontrada no arquivo .env")
    exit(1)

client = Groq(api_key=API_KEY)


def analyze_log(log_snippet):
    """Envia o fragmento do log para a IA analisar."""

    prompt = f"""
    Você é um agente autônomo especialista em SecOps focado em sistemas Linux.
    Acaba de ocorrer um evento no sistema. Analise as linhas de log abaixo e identifique:
    
    1. A gravidade (Baixa, Média, Crítica).
    2. O que este evento significa (ex: brute force, alteração de permissão, rotina do sistema).
    3. Qual comando de mitigação (se houver) deve ser aplicado no terminal.
    
    Logs:
    {log_snippet}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Seja direto, técnico e utilize formato Markdown para organizar a resposta.",
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2,  # Temperatura baixa para focar em precisão técnica
        )
        print("\n[✓] RELATÓRIO DO AGENTE AUTÔNOMO:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        print(
            "[*] Agente retornou ao estado de vigilância (Aguardando novos eventos...)\n"
        )

    except Exception as e:
        print(f"[✗] Erro de comunicação com a IA: {e}")
