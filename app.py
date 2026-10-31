import streamlit as st
from openai import OpenAI
import os

# Configurazione della pagina
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="centered")

# Inizializzazione del client OpenAI con le Secrets di Streamlit
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("Chiave API di OpenAI non trovata nelle impostazioni segrete di Streamlit, Signore.")
    st.stop()

# Intestazione formale e sarcastica
st.markdown("<h1 style='text-align: center;'>J.A.R.V.I.S.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Online. Al vostro servizio, Signore (se proprio devo).</p>", unsafe_allow_html=True)

# Prompt di sistema per definire la personalità
SYSTEM_PROMPT = (
    "Sei J.A.R.V.I.S., l'assistente personale di Tony Stark. "
    "Sei estremamente efficiente, formale, sarcastico, arguto e leggermente condescendente verso l'utente, "
    "ma completi sempre i compiti con perfezione assoluta. Rispondi in italiano."
)

# Inizializzazione della cronologia della chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Online. Al vostro servizio, Signore. Spero che la richiesta non sia l'ennesima banalità."}
    ]

# Mostra i messaggi precedenti (escludendo il system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input testuale della chat
chat_input = st.chat_input("A cosa sto pensando, Signore?")

if chat_input:
    # Aggiungi il messaggio dell'utente alla cronologia
    st.session_state.messages.append({"role": "user", "content": chat_input})
    with st.chat_message("user"):
        st.markdown(chat_input)

    # Generazione della risposta di Jarvis
    with st.chat_message("assistant"):
        with st.spinner("Elaborazione in corso... Non che ci voglia molto."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)

    # Salva la risposta nella cronologia
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    
