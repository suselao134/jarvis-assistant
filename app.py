import streamlit as st
from huggingface_hub import InferenceClient

# Konfiguracja strony wizualnej
st.set_page_config(page_title="JARVIS Assistant", page_icon="🤖", layout="centered")

st.title("🤖 JARVIS — Asystent Głosowy")
st.write("Witaj Proszę Pana. Jestem gotowy do analizy i pomocy naukowej.")

# Prawidłowe pobieranie darmowego klucza Hugging Face z secrets
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

if not HF_TOKEN:
    st.error("Błąd systemu: Brak klucza HF_TOKEN w ustawieniach serwera!")
    st.stop()

# Inicjalizacja darmowego modelu od Microsoftu
client = InferenceClient(model="Qwen/Qwen2.5-Coder-7B-Instruct", token=HF_TOKEN)

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
    
    # Awaryjne pole tekstowe
    command = st.text_input("Popraw tekst lub wpisz polecenie ręcznie, jeśli mikrofon nie przepisał mowy:")
    
    if st.button("Wyślij do JARVIS-a") or (command and not st.session_state.get('processed')):
        text_to_analyze = command if command else "Wyjaśnij mi, jak zbudować prosty silnik, Sir."
        
        # Zbudowanie oficjalnej, czystej struktury konwersacyjnej (wymaganej przez serwery!)
        messages = [
            {"role": "system", "content": JARVIS_PROMPT},
            {"role": "user", "content": text_to_analyze}
        ]
        
        with st.spinner("JARVIS analizuje dane..."):
            try:
                # Używamy stabilnego czatu zbierając dane w locie
                response = ""
                for message in client.chat_completion(messages, max_tokens=400, stream=True):
                    token = message.choices.delta.content
                    if token:
                        response += token
                
                # Wyświetlenie odpowiedzi JARVIS-a
                st.subheader("Odpowiedź JARVIS-a:")
                st.write(response)
                
                # WYGENEROWANIE AUDIO (JARVIS MÓWI PRZEZ PRZEGLĄDARKĘ!)
                tts_html = f"""
                <audio autoplay>
                  <source src="https://google.com{response.replace(' ', '+')}" type="audio/mpeg">
                </audio>
                """
                st.components.v1.html(tts_html, height=0)
                st.success("🤖 JARVIS odpowiedział głosowo przez Twoje głośniki!")
                
            except Exception as e:
                st.error(f"Błąd rdzenia AI: {e}")
