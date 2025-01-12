import requests
import time

def test_ollama_connection():
    max_retries = 5
    retry_delay = 2
    
    for i in range(max_retries):
        try:
            response = requests.get('http://localhost:5001/health')
            if response.status_code == 200:
                print("✅ Connessione a Ollama stabilita con successo")
                return True
            else:
                print(f"❌ Tentativo {i+1}/{max_retries}: Servizio non disponibile")
        except requests.exceptions.ConnectionError:
            print(f"❌ Tentativo {i+1}/{max_retries}: Impossibile connettersi al backend")
        
        if i < max_retries - 1:
            time.sleep(retry_delay)
    
    return False

if __name__ == "__main__":
    test_ollama_connection()