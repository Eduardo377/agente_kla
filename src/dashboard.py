import sys
import os
import streamlit as st

# Aponta para o Python que a raiz do projeto está uma pasta para trás (..)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analyzer import analyze_log

# Configuração da página
st.set_page_config(page_title="KLA Agent Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ KLA - Central de SecOps")
st.markdown("Interface de triagem de ameaças orquestrada por Llama 3.1")

# Caixa de texto para análise manual
log_input = st.text_area("Insira as linhas de log suspeitas:", height=150)

if st.button("Analisar Ameaça", type="primary"):
    if log_input:
        with st.spinner("Consultando inteligência da Groq..."):
            resultado = analyze_log(log_input)
            st.success("Análise concluída!")
            st.markdown(resultado)
    else:
        st.warning("Insira um log para analisar.")
