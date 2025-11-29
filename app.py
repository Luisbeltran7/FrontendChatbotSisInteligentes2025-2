import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

st.set_page_config(page_title="Chatbot Sistemas Inteligentes", page_icon="🤖", layout="wide")

# --- CONFIGURACIÓN ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BACKEND_ENDPOINT = os.getenv("BACKEND_ENDPOINT", "/question")
API_URL = f"{BACKEND_URL}{BACKEND_ENDPOINT}"

# --- CARGAR CSS ---
with open("styles.css", "r", encoding="utf-8") as css_file:
    css_content = css_file.read()

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# HEADER
st.markdown("<header>Chatbot Sistemas Inteligentes</header>", unsafe_allow_html=True)

# --- CONTROLES DE MODELO, MODO Y TOP_K ---
model_providers = ["openai", "groq"]
modes = ["breve", "detallada"]
col1, col2, col3 = st.columns(3)



with st.sidebar:
    selected_model = st.selectbox("Modelo", model_providers, index=0)
    selected_mode = st.selectbox("Modo", modes, index=1)
    top_k = st.slider("top_k", 1, 10, 3)


# HISTORIAL
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"sender": "bot", "text": "Hola, soy tu asistente inteligente. ¿En qué puedo ayudarte?"}
    ]

    

# --- MOSTRAR CHAT ---
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["text"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["text"])

            
# INPUT
user_prompt = st.chat_input("Escribe tu pregunta...", key="input")




if user_prompt and user_prompt.strip():
    st.session_state.messages.append({"sender": "user", "text": user_prompt})
    payload = {
        "question": user_prompt,
        "model_provider": selected_model,
        "mode": selected_mode,
        "top_k": top_k
    }
    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            respuesta = data.get("answer", "No se encontró respuesta en el backend.")
        else:
            respuesta = f"Error {response.status_code}: {response.text}"
    except Exception as e:
        respuesta = f"Error al conectar con el backend: {e}"
    st.session_state.messages.append({"sender": "bot", "text": respuesta})
    st.rerun()