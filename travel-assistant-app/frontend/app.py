import streamlit as st
import requests
import os

# Usa la variabile d'ambiente o fallback su localhost
API_BASE_URL = os.getenv('BACKEND_URL', 'http://localhost:5001')

def fetch_itinerary(destination, dates, preferences):
    try:
        response = requests.post(f"{API_BASE_URL}/generate_itinerary", json={
            'destination': destination,
            'dates': dates,
            'preferences': preferences
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")
        return None

def stream_itinerary(destination, dates, preferences):
    try:
        response = requests.post(f"{API_BASE_URL}/stream_itinerary", json={
            'destination': destination,
            'dates': dates,
            'preferences': preferences
        }, stream=True)
        response.raise_for_status()
        
        # Crea un placeholder per l'output
        output_placeholder = st.empty()
        full_response = ""
        
        # Stream e aggiorna il contenuto
        for chunk in response.iter_content(chunk_size=128):
            decoded_chunk = chunk.decode('utf-8')
            full_response += decoded_chunk
            # Usa markdown per preservare la formattazione
            output_placeholder.markdown(full_response)
            
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")

st.set_page_config(
    layout="wide",
    page_title="Travel Itinerary Generator",
    page_icon="🌍"
)

# Stile CSS personalizzato
st.markdown("""
    <style>
    .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
    }
    .stMarkdown ul {
        margin-left: 20px;
        margin-bottom: 10px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Travel Itinerary Generator")

col1, col2 = st.columns(2)

with col1:
    destination = st.text_input("📍 Destinazione")
    preferences = st.text_area("✨ Preferenze di viaggio")

with col2:
    start_date = st.date_input("📅 Data di inizio")
    end_date = st.date_input("📅 Data di fine")

col3, col4 = st.columns(2)

with col3:
    if st.button("🚀 Genera Itinerario"):
        dates = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
        with st.spinner('Generazione itinerario in corso...'):
            itinerary = fetch_itinerary(destination, dates, preferences)
            if itinerary:
                st.markdown(itinerary['itinerary'])

with col4:
    if st.button("📝 Stream Itinerario"):
        dates = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
        with st.spinner('Streaming itinerario in corso...'):
            stream_itinerary(destination, dates, preferences)