import streamlit as st
from huggingface_hub import InferenceClient

# Konfiguracja strony wizualnej
st.set_page_config(page_title="JARVIS Assistant", page_icon="🤖", layout="centered")

st.title("🤖 JARVIS — Asystent Głosowy")
st.write("Witaj Proszę Pana. Jestem gotowy do analizy i pomocy naukowej.")

# Prawidłowe pobieranie klucza z secrets
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

if not HF_TOKEN:
    st.error("Błąd systemu: Brak klucza HF_TOKEN w ustawieniach serwera!")
    st.stop()

# Inicjalizacja modelu od Microsoftu
client = InferenceClient(model="microsoft/Phi-3-mini-4k-instruct", token=HF_TOKEN)

JARVIS_PROMPT = """
Nazywasz się JARVIS. Jesteś genialnym, ultraracjonalnym asystentem inżynieryjnym i naukowym. 
Twoim celem jest pomaganie użytkownikowi w tworzeniu rzeczy, nauce oraz analizie pomysłów. 
NIGDY nie słodzisz i nie owijasz w bawełnę. Jeśli użytkownik popełnia błąd logiczny lub techniczny, natychmiast mu to wytknij wprost. 
Oceniaj pomysły pod kątem realizmu, praw fizyki i inżynierii. 
Odpowiadaj krótko, konkretnie i wyłącznie po polsku, używając zwrotów per 'Proszę pana' (Sir).
"""

# Komponent do nagrywania głosu z mikrofonu przez przeglądarkę
audio_value = st.audio_input("Kliknij mikrofon i powiedz polecenie:")

if audio_value:
    st.info("Systemy audio przetwarzają dźwięk...")
    
    # Awaryjne pole tekstowe na wypadek problemów z transkrypcją
    command = st.text_input("Popraw tekst lub wpisz polecenie ręcznie, jeśli mikrofon nie przepisał mowy:")
    
    if st.button("Wyślij do JARVIS-a") or (command and not st.session_state.get('processed')):
        text_to_analyze = command if command else "Wyjaśnij mi, jak zbudować prosty silnik, Sir."
        
        # WYMUSZONE PRZEZ SERWER: Oficjalna struktura czatu dla funkcji conversational
        messages = [
            {"role": "system", "content": JARVIS_PROMPT},
            {"role": "user", "content": text_to_analyze}
        ]
        
        with st.spinner("JARVIS analizuje dane..."):
            try:
                # Używamy oficjalnej metody chat_completion, zbierając odpowiedź kawałek po kawałku
                response = ""
                for message in client.chat_completion(messages, max_tokens=400, stream=True):
                    token = message.choices.delta.content
                    if token:
                        response += token
                
                # Wyświetlenie odpowiedzi JARVIS-a
                st.subheader("Odpowiedź JARVIS-a:")
                st.write(response)
                
                # POPRAWIONE AUDIO: Poprawny link do syntezatora mowy Google
                tts_html = f"""
                <audio autoplay>
                  <source src="https://google.com{response.replace(' ', '+')}" type="audio/mpeg">
                </audio>
                """
                st.components.v1.html(tts_html, height=0)
                st.success("🤖 JARVIS odpowiedział głosowo przez Twoje głośniki!")
                
            except Exception as e:
                st.error(f"Błąd rdzenia AI: {e}")
