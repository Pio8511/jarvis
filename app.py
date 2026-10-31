import streamlit as st
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
import os
import base64

# Configurazione della pagina
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="centered")

# Inizializzazione del client OpenAI con le Secrets di Streamlit
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("Chiave API di OpenAI non trovata nelle impostazioni segrete di Streamlit, Signore.")
    st.stop()

# Intestazione formale e leggermente sarcastica
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

# --- GESTIONE VOCALE (Registrazione simulata / Input audio) ---
st.markdown("---")
st.subheader("Interazione Vocale")

# Streamlit audio input nativo (disponibile nelle versioni recenti per mobile/desktop)
audio_bytes = st.audio_input("Parla con J.A.R.V.I.S.")

user_input = None

if audio_bytes is not None:
    # Salviamo temporaneamente l'audio registrato
    audio_file_path = "temp_audio.wav"
    with open(audio_file_path, "wb") as f:
        f.write(audio_bytes.read())
    
    # Riconoscimento vocale tramite SpeechRecognition
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = r.record(source)
            text_recognized = r.recognize_google(audio_data, language="it-IT")
            user_input = text_recognized
            st.success(recognized_text := f"Avete detto: \"{text_recognized}\"")
    except sr.UnknownValueError:
        st.warning("Non ho udito alcuna parola intelligibile, Signore. Forse dovreste articolare meglio.")
    except sr.RequestError:
        st.error("Il servizio di riconoscimento vocale non è al momento disponibile.")
    
    # Pulizia del file temporaneo
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

# Input testuale tradizionale come alternativa
chat_input = st.chat_input("A cosa sto pensando, Signore?")

if chat_input:
    user_input = chat_input

# Se c'è un input valido (vocale o testuale)
if user_input:
    # Aggiungi il messaggio dell'utente alla cronologia
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

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
            assistant_reply = response.choices.message.content
            st.markdown(assistant_reply)
            
            # Sintesi vocale (gTTS)
            tts = gTTS(text=assistant_reply, lang='it')
            speech_file = "jarvis_reply.mp3"
            tts.save(speech_file)
            
            # Riproduzione audio automatica
            audio_file = open(speech_file, 'rb')
            audio_bytes_out = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes_out).decode()
            audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
            st.markdown(audio_tag, unsafe_allow_html=True)
            audio_file.close()
            
            if os.path.exists(speech_file):
                os.remove(speech_file)

    # Salva la risposta nella cronologia
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

  
