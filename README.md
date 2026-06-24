# 🛡️ Kensei Log Auditor Agent (KLA Agent)
![Version](https://img.shields.io/badge/version-2.0.0-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

## 📝 Histórico de Versões
* **v2.0.0 (Versão Atual):** Evolução para Agente Autônomo. Implementação de monitoramento contínuo (Watchdog), arquitetura em background e interface Web (Streamlit Dashboard).
* **v1.0.0:** Lançamento da PoC CLI estática com motor Groq Llama 3.1.

# 🛡️ Visão Geral do Sistema: KLA Agent

**Programa:** Kensei AI Foundations 2026  
**Trilha:** Trilha D: A Jornada AI-First  
**Componente:** Automação de SecOps, Agentes IA e Dashboards Operacionais  
**Status:** Operacional (Vigilância Contínua)

---

## 1. Introdução e Contexto do Projeto

O **KLA Agent** é a evolução natural do Kensei Log Auditor original. Ele deixou de ser uma ferramenta de execução manual para se tornar um **Agente de IA Autônomo**, operando de forma contínua na primeira camada de um **SOC (Security Operations Center)**.

O sistema agora possui um ciclo completo de **Observação, Raciocínio e Exibição**. Ele monitora eventos do sistema operacional (como tentativas de intrusão via SSH) em tempo real, processa a inteligência da ameaça via LLM e entrega os dados estruturados em uma interface web nativa, mantendo a filosofia do **Human-in-the-Loop (HITL)** para a execução de contramedidas.

---

## 2. Engenharia de Produção e Arquitetura do Sistema

A nova arquitetura adota um padrão de desacoplamento, separando a lógica de vigilância (Daemon) da interface de consumo de dados (Dashboard).

```text
+-------------------------------------------------------------------------+
|                         SISTEMA HOSPEDEIRO (LINUX)                      |
|                                                                         |
|  [Log de Sistema] -> /var/log/auth.log                                  |
|                               |                                         |
|  +----------------------------v-----+      +-------------------------+  |
|  | 👁️ Watchdog (Cão de Guarda)     | ---> | 🧠 Motor de IA (Groq)    |  |
|  |   (Monitoramento em background)  |      |   Llama 3.1 8B Instant  |  |
|  +----------------------------------+      +-----------+-------------+  |
|                                                        |                |
|  +-----------------------------------------------------v-------------+  |
|  | 🌐 SecOps Web Dashboard (Streamlit)                               |  |
|  |   - Visualização de Ameaças em Tempo Real                         |  |
|  |   - Triagem Manual e Geração de Mitigações (Human-in-the-Loop)    |  |
|  +-------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+

```

### 2.1. Componentes do Agente

* **O Observador (`watcher.py` & `main.py`):** Utiliza a biblioteca `watchdog` para monitorar modificações em arquivos de log sem consumir ciclos desnecessários de CPU, operando de forma reativa baseada em eventos do Kernel (Inotify).
* **O Cérebro (`analyzer.py`):** Mantém a integração de latência ultra-baixa com a Groq Cloud, capaz de identificar padrões de Brute Force, Movimentação Lateral e Escalonamento de Privilégio.
* **O Painel de Controle (`dashboard.py`):** Uma interface interativa construída em Streamlit, projetada em *Dark Mode*, permitindo que o analista de segurança revise relatórios e tome decisões operacionais sem a necessidade de ler logs crus no terminal.


## 3. ⚙️ Configuração do Ambiente

O KLA Agent requer dependências específicas para orquestrar o observador e a interface web.

1. **Clone o repositório:**
```bash
git clone git@github.com:SeuUsuario/agente_kla.git
cd agente_kla

```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt

```

3. **Configure a Chave da API (Groq):** Crie um arquivo `.env` na raiz do projeto e adicione sua chave criptográfica:

```env
GROQ_API_KEY=sua_chave_aqui

```

4. **Aponte o Dashboard para os logs do sistema (Opcional, para Produção):**
No painel Streamlit, o caminho do arquivo vem configurado por padrão para ler um log de teste. Para ler logs reais do seu sistema, abra o arquivo `src/dashboard.py` (próximo à linha 16) e altere a variável `LOG_FILE` para o caminho absoluto do sistema:

**De:**

```python
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "meu_log_de_teste.log"))

```

**Para:**

```python
LOG_FILE = "/var/log/auth.log"

```

> ⚠️ **Atenção às Permissões no Linux:** O arquivo `/var/log/auth.log` é restrito pelo sistema operacional. Apenas o usuário `root` ou membros do grupo `adm` podem lê-lo. Se ao rodar o Agente ou o Dashboard você receber o erro `PermissionError: [Errno 13] Permission denied: '/var/log/auth.log'`, você precisará executar os comandos da Seção 4 utilizando privilégios administrativos (`sudo`).

---

## 4. 🚀 Como Executar (Fluxo Operacional SOC)

A operação padrão exige a execução de dois processos em paralelo (recomenda-se o uso de um multiplexador de terminal como o Tilix ou Tmux).

### Passo 1: Iniciar o Agente de Vigilância

Em um terminal, inicie o observador. Ele ficará em loop infinito aguardando ataques.
*Para ler logs reais do sistema (`/var/log/auth.log`), é necessário privilégio administrativo.*

```bash
sudo python3 main.py /var/log/auth.log

```

*(Para testes controlados, você pode passar um log falso: `python3 main.py meu_log_de_teste.log`)*

### Passo 2: Iniciar a Central de SecOps (Dashboard)

Em um segundo terminal, levante o servidor Streamlit para visualizar a interface gráfica:

```bash
sudo python3 -m streamlit run src/dashboard.py

```

*(O uso do `sudo` aqui é necessário apenas se o Dashboard for configurado para ler diretamente arquivos protegidos do sistema).*

---

## 5. Controle de Versão

| Versão  | Data       | Autor         | Descrição da Mudança                             |
| ------- | ---------- | ------------- | ------------------------------------------------ |
| **2.0** | 24/06/2026 | Eduardo Gomes | Refatoração para Agente IA, Watchdog e Streamlit |
| 1.0     | 11/06/2026 | Eduardo Gomes | Lançamento da PoC: Motor Llama 3.1, Docker, CLI  |

---

## 6. Filosofia de Segurança: Human-in-the-Loop (HITL)

O KLA Agent automatiza o **MTTD (Mean Time to Detect)**, reduzindo o tempo de triagem de minutos para segundos. No entanto, a execução de contramedidas sistêmicas (como a alteração de regras no `iptables` ou `ufw` geradas pela IA) continua exigindo a validação humana. A ferramenta atua como um multiplicador de força para o engenheiro de segurança, não como um substituto autônomo.