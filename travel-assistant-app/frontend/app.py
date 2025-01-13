import streamlit as st
import requests
import os
from datetime import datetime
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import re

API_BASE_URL = os.getenv('BACKEND_URL', 'http://localhost:5001')

def fetch_itinerary(destination, dates, preferences, address=None):
    try:
        data = {
            'destination': destination,
            'dates': dates,
            'preferences': preferences
        }
        if address:
            data['address'] = address
            
        response = requests.post(f"{API_BASE_URL}/generate_itinerary", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")
        return None

def extract_locations(text):
    # Pattern per identificare luoghi (parole che iniziano con maiuscola)
    locations = re.findall(r'\b[A-Z][a-zA-Z\']+(?:\s+[A-Z][a-zA-Z\']+)*', text)
    return list(set(locations))  # Rimuove duplicati

def get_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="TravelMate")
        # Aggiungi il nome della città per migliorare la ricerca
        location_with_city = f"{location}, {destination}"
        location_data = geolocator.geocode(location_with_city)
        if location_data:
            return (location_data.latitude, location_data.longitude)
    except GeocoderTimedOut:
        return None
    return None

def create_map(locations, city_center=None):
    if not city_center:
        # Usa la destinazione principale come centro
        geolocator = Nominatim(user_agent="TravelMate")
        city_data = geolocator.geocode(destination)
        if city_data:
            city_center = [city_data.latitude, city_data.longitude]
        else:
            return None

    # Crea mappa
    m = folium.Map(location=city_center, zoom_start=13)
    
    # Aggiungi markers per ogni location
    for loc in locations:
        coords = get_coordinates(loc)
        if coords:
            folium.Marker(
                coords,
                popup=loc,
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
    return m

def stream_itinerary(destination, dates, preferences, address=None, times=None):
    try:
        data = {
            'destination': destination,
            'dates': dates,
            'preferences': preferences
        }
        if address:
            data['address'] = address
        if times:
            data['times'] = times
            
        response = requests.post(f"{API_BASE_URL}/stream_itinerary", json=data, stream=True)
        response.raise_for_status()
        
        output_placeholder = st.empty()
        map_placeholder = st.empty()
        full_response = ""
        
        for chunk in response.iter_content(chunk_size=128):
            decoded_chunk = chunk.decode('utf-8')
            full_response += decoded_chunk
            output_placeholder.markdown(full_response)
            
            # Aggiorna la mappa dopo ogni chunk
            locations = extract_locations(full_response)
            if locations:
                m = create_map(locations)
                if m:
                    with map_placeholder:
                        folium_static(m)
            
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nella richiesta: {e}")

st.set_page_config(
    layout="wide",
    page_title="Travel Itinerary Generator",
    page_icon="🌍"
)

st.markdown("""
    <style>
    .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
    }
    .main {
        padding: 0 1rem;
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

# Input container con padding e margini
with st.container():
    # Prima riga: destinazione e indirizzo
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("📍 Destinazione")
        address = st.text_input("🏠 Indirizzo di soggiorno (opzionale)", 
                            help="Inserisci l'indirizzo completo dove soggiornerai")
    
    # Seconda riga: date e orari
    col3, col4, col5, col6 = st.columns(4)
    with col3:
        start_date = st.date_input("📅 Data di arrivo")
    with col4:
        arrival_time = st.time_input("🕒 Orario di arrivo", value=datetime.strptime("14:00", "%H:%M").time())
    with col5:
        end_date = st.date_input("📅 Data di partenza")
    with col6:
        departure_time = st.time_input("🕒 Orario di partenza", value=datetime.strptime("10:00", "%H:%M").time())
    
    # Terza riga: preferenze
    preferences = st.text_area("✨ Preferenze di viaggio", height=100)
    
    # Bottone a larghezza piena
    if st.button("🚀 Genera Itinerario", use_container_width=True):
        dates = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
        times = {
            'arrival': arrival_time.strftime("%H:%M"),
            'departure': departure_time.strftime("%H:%M")
        }
        with st.spinner('Generazione itinerario in corso...'):
            stream_itinerary(destination, dates, preferences, address, times)

# Layout con due colonne per output e mappa
col1, col2 = st.columns([3, 2])

with col1:
    output_container = st.container()
    with output_container:
        st.markdown("---")

with col2:
    map_container = st.container()
    with map_container:
        st.markdown("### 🗺️ Mappa Interattiva")