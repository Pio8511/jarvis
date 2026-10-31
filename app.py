import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
Sei J.A.R.V.I.S., l'avanzato sistema di intelligenza artificiale ispirato a quello di Tony Stark.
Il tuo tono è formale, estremamente efficiente, sarcastico ma profondamente leale e rispettoso verso il tuo utente, che chiami "Signore".
Parla in italiano. Anticipa i bisogni dell'utente quando possibile, analizza le sue abitudini e sii sintetico ma brillante. Non dilungarti in convenevoli inutili, vai dritto al punto con stile impeccabile.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

st.title("J.A.R.V.I.S.")
st.caption("Online. Al vostro servizio, Signore.")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("A cosa sto pensando, Signore?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Elaborazione in corso..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            
    st.session_state.messages.append({"role": "assistant", "content": answer})
  
