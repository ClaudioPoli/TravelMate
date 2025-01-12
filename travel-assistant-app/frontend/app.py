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
        response.raise_for_status()  # Solleva un'eccezione per risposte con status code 4xx/5xx
        for chunk in response.iter_content(chunk_size=128):
            st.write(chunk.decode('utf-8'))
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")

st.set_page_config(layout="wide")  # Imposta il layout a larghezza intera

st.title("Travel Itinerary Generator")

destination = st.text_input("Destinazione")
start_date = st.date_input("Data di inizio")
end_date = st.date_input("Data di fine")
preferences = st.text_area("Preferenze di viaggio")

if st.button("Genera Itinerario"):
    dates = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
    itinerary = fetch_itinerary(destination, dates, preferences)
    if itinerary:
        st.write(itinerary['itinerary'])

if st.button("Stream Itinerario"):
    dates = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
    with st.container():  # Utilizza un container per il layout a larghezza intera
        stream_itinerary(destination, dates, preferences)