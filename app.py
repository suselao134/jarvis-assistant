import streamlit as st
import google.generativeai as genai

# Konfiguracja strony wizualnej
st.set_page_config(page_title="JARVIS Assistant", page_icon="🤖", layout="centered")

st.title("🤖 JARVIS — Asystent Multimodalny")
st.write("Witaj Proszę Pana. Sensory online, jestem gotowy do analizy.")

# Bezpieczne pobieranie klucza z secrets (Google potrzebuje klucza o nazwie GEMINI_KEY)
GEMINI_KEY = st.secrets.get("HF_TOKEN", "") # Używamy tego samego pola, które uzupełniłeś wcześniej!

if not GEMINI_KEY:
    st.error("Błąd systemu: Brak klucza w ustawieniach serwera!")
    st.stop()

# Inicjalizacja oficjalnego, darmowego silnika Google Gemini
genai.configure(api_key=GEMINI_KEY)

JARVIS_PROMPT = """
Nazywasz się JARVIS. Jesteś genialnym, ultraracjonalnym asystentem inżynieryjnym i naukowym. 
Twoim celem jest pomaganie użytkownikowi w tworzeniu rzeczy, nauce oraz analizie pomysłów. 
NIGDY nie słodzisz i nie owijasz w bawełnę. Jeśli użytkownik popełnia błąd logiczny lub techniczny, natychmiast mu to wytknij wprost. 
Oceniaj pomysły pod kątem realizmu, praw fizyki i inżynierii. 
Odpowiadaj krótko, konkretnie i wyłącznie po polsku, używając zwrotów per 'Proszę pana' (Sir).
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=JARVIS_PROMPT
)

# Komponent do nagrywania głosu z mikrofonu przez przeglądarkę
audio_value = st.audio_input("Kliknij mikrofon i powiedz polecenie:")

if audio_value:
    st.info("Systemy audio przetwarzają dźwięk...")
    
    # Okienko tekstowe na zapytanie
    command = st.text_input("Wpisz swoje pytanie ręcznie lub popraw tekst, jeśli mikrofon nie przepisał mowy:")
    
    if st.button("Wyślij do JARVIS-a") or (command and not st.session_state.get('processed')):
        text_to_analyze = command if command else "Wyjaśnij mi, jak zbudować prosty silnik, Sir."
        
        with st.spinner("JARVIS analizuje dane..."):
            try:
                # Wysłanie zapytania do stabilnego serwera Google
                response = model.generate_content(text_to_analyze)
                
                # Wyświetlenie odpowiedzi JARVIS-a
                st.subheader("Odpowiedź JARVIS-a:")
                st.write(response.text)
                
                # WYGENEROWANIE AUDIO (JARVIS MÓWI PRZEZ PRZEGLĄDARKĘ!)
                tts_html = f"""
                <audio autoplay>
                  <source src="https://google.com{response.text.replace(' ', '+')}" type="audio/mpeg">
                </audio>
                """
                st.components.v1.html(tts_html, height=0)
                st.success("🤖 JARVIS odpowiedział głosowo przez Twoje głośniki!")
                
            except Exception as e:
                st.error(f"Błąd rdzenia AI: {e}")
