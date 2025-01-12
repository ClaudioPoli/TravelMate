
# 🌍 TravelMate - AI-Powered Travel Itinerary Assistant

## 📝 Description
TravelMate is an AI-based travel assistant that generates personalized itineraries in Italian. It uses Ollama as a local language model to create tailored travel experiences.

## 🛠 Tech Stack
- Frontend: Streamlit
- Backend: Flask
- AI: Ollama (LLM)
- Containerization: Docker
- AI Integration: LangChain

## ⚙️ Prerequisites
- macOS (Silicon/Intel)
- [Homebrew](https://brew.sh)
- Docker Desktop for Mac
- Python 3.9+
- 8GB RAM
- 20GB disk space

## 🚀 Installation

### Install Ollama
```bash
brew install ollama
```

### Clone the repository
```bash
git clone https://github.com/yourusername/TravelMate.git
cd TravelMate
```

### Configure the environment
```bash
echo "OLLAMA_BASE_URL=http://host.docker.internal:11434" > .env
```

### Start Ollama
```bash
ollama serve
```

### Download the model
```bash
ollama pull llama3.2
```

## 🏃 Startup
### Docker Mode
```bash
docker compose up --build
```

### Development Mode
#### Terminal 1 - Backend
```bash
cd travel-assistant-app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

#### Terminal 2 - Frontend
```bash
cd travel-assistant-app/frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Access
- Frontend: [http://localhost:8501](http://localhost:8501)
- Backend API: [http://localhost:5001](http://localhost:5001)

## ✅ Installation Verification
```bash
python travel-assistant-app/test/test_ollama_connection.py
```

## 🔧 Troubleshooting
### Backend does not connect to Ollama
#### Check Ollama
```bash
ps aux | grep ollama
```
#### Restart if necessary
```bash
killall ollama && ollama serve
```

## 📖 License
MIT

## 🤝 Contributions
Fork > Feature Branch > PR

## 💬 Support
Open an Issue on GitHub
