# 🌍 TravelMate - Assistente AI per Itinerari di Viaggio

## 📝 Descrizione
TravelMate è un assistente di viaggio basato su AI che genera itinerari personalizzati in italiano. Utilizza Ollama come modello di linguaggio locale per creare esperienze di viaggio su misura.

## 🛠 Stack Tecnologico
- Frontend: Streamlit
- Backend: Flask
- AI: Ollama (LLM)
- Containerizzazione: Docker
- Integrazione AI: LangChain

## ⚙️ Prerequisiti
- macOS (Silicon/Intel)
- [Homebrew](https://brew.sh/index_it)
- Docker Desktop per Mac
- Python 3.9+
- 8GB RAM
- 20GB spazio disco


## 🚀 Installazione

### Installare Ollama
brew install ollama

# Clonare il repository
git clone https://github.com/tuousername/TravelMate.git
cd TravelMate

# Configurare l'ambiente
echo "OLLAMA_BASE_URL=http://host.docker.internal:11434" > .env

# Avviare Ollama
ollama serve

# Scaricare il modello
ollama pull llama3.2

# 🏃 Avvio
## Modalità Docker
docker compose up --build

# Modalità Sviluppo
# Terminal 1 - Backend
cd travel-assistant-app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py

# Terminal 2 - Frontend
cd travel-assistant-app/frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

# 🌐 Accesso
Frontend: http://localhost:8501
Backend API: http://localhost:5001

# ✅ Verifica Installazione
python travel-assistant-app/test/test_ollama_connection.py

# 🔧 Troubleshooting
## Il Backend non si Connette a Ollama
# Verifica Ollama
ps aux | grep ollama
# Riavvia se necessario
killall ollama && ollama serve

📖 Licenza
MIT

🤝 Contributi
Fork > Feature Branch > PR

💬 Supporto
Apri una Issue su GitHub 
