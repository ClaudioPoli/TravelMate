import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama import OllamaLLM

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

def create_ollama_model():
    try:
        host = "http://host.docker.internal:11434"
        logging.debug(f"Tentativo di connessione a Ollama su: {host}")
        
        model = OllamaLLM(
            model="llama3.2",
            host=host,
            system="Sei un assistente di viaggio italiano. Rispondi sempre in italiano.",
            temperature=0.7,
            options={
                "language": "italian",
                "system": "Sei un esperto di viaggi italiano. DEVI rispondere SEMPRE in italiano.",
                "num_ctx": 4096,
                "top_k": 50,
                "top_p": 0.9,
                "stop": ["Human:", "Assistant:"]}
        )
        return model
    except Exception as e:
        logging.error(f"Errore nella creazione del modello Ollama: {e}")
        raise

# Inizializza il modello
try:
    model = create_ollama_model()
    logging.info("Modello Ollama inizializzato con successo")
except Exception as e:
    logging.error(f"Errore nell'inizializzazione del modello: {e}")
    model = None

@app.route('/health', methods=['GET'])
def health_check():
    if model is not None:
        return jsonify({"status": "healthy", "model": "connected"})
    return jsonify({"status": "unhealthy", "model": "disconnected"}), 500

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.json
        logging.debug(f"Received data: {data}")
        destination = data['destination']
        dates = data['dates']
        preferences = data['preferences']
        address = data.get('address')  # Campo opzionale
        
        base_prompt = f"""
        Agisci come un esperto di viaggi italiano e crea un itinerario di viaggio dettagliato in italiano.
        
        Destinazione: {destination}
        Date: dal {dates[0]} al {dates[1]}
        Preferenze: {preferences}
        """
        
        if address:
            base_prompt += f"""
        Punto di partenza: {address}
        
        Considera questo indirizzo come punto di partenza per organizzare le visite giornaliere.
        Suggerisci i percorsi più efficienti e indica:
        - Distanze approssimative dal punto di partenza
        - Mezzi di trasporto consigliati
        - Tempistiche di spostamento
        """
        
        base_prompt += """
        Fornisci un itinerario giorno per giorno, includendo:
        - Attrazioni da visitare
        - Ristoranti consigliati
        - Tempi di visita suggeriti
        - Consigli pratici
        
        Rispondi in italiano.
        """
        
        logging.debug(f"Generated prompt: {base_prompt}")
        response = model.invoke(base_prompt)
        logging.debug(f"Model response: {response}")
        return jsonify({'itinerary': response})
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/stream_itinerary', methods=['POST'])
def stream_itinerary():
    try:
        data = request.json
        logging.debug(f"Received data: {data}")
        destination = data['destination']
        dates = data['dates']
        preferences = data['preferences']
        address = data.get('address')
        times = data.get('times', {})
        
        base_prompt = f"""
        Agisci come un esperto di viaggi italiano e crea un itinerario di viaggio dettagliato in italiano.
        
        Destinazione: {destination}
        Date: dal {dates[0]} (arrivo ore {times.get('arrival', 'N/A')}) 
              al {dates[1]} (partenza ore {times.get('departure', 'N/A')})
        Preferenze: {preferences}
        """
        
        if address:
            base_prompt += f"""
        Punto di partenza: {address}
        
        Considera questo indirizzo come punto di partenza per organizzare le visite giornaliere.
        Suggerisci i percorsi più efficienti e indica:
        - Distanze approssimative dal punto di partenza
        - Mezzi di trasporto consigliati
        - Tempistiche di spostamento
        
        Considera gli orari di arrivo e partenza per ottimizzare il tempo disponibile.
        """
        
        base_prompt += """
        Fornisci un itinerario giorno per giorno, includendo:
        - Attrazioni da visitare
        - Ristoranti consigliati
        - Tempi di visita suggeriti
        - Consigli pratici
        
        Rispondi in italiano.
        """
        
        logging.debug(f"Generated prompt: {base_prompt}")
        def generate():
            for chunk in model.stream(base_prompt):
                yield chunk
        return app.response_class(generate(), mimetype='text/plain')
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)