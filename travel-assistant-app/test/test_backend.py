from langchain_ollama import OllamaLLM

def test_generate_itinerary():
    model = OllamaLLM(model="llama3.2")
    destination = "Roma"
    dates = ["2025-01-12", "2025-01-12"]
    preferences = "cultura, cibo, storia"
    prompt = f"Crea un itinerario di viaggio personalizzato per {destination} dal {dates[0]} al {dates[1]} considerando le mie preferenze {preferences}."
    response = model.invoke(prompt)
    print("Generated Itinerary:")
    print(response)

def test_stream_itinerary():
    model = OllamaLLM(model="llama3.2")
    destination = "Roma"
    dates = ["2025-01-12", "2025-01-12"]
    preferences = "cultura, cibo, storia"
    prompt = f"Crea un itinerario di viaggio personalizzato per {destination} dal {dates[0]} al {dates[1]} considerando le mie preferenze {preferences}."
    print("Streaming Itinerary:")
    for chunk in model.stream(prompt):
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    print("Testing generate_itinerary function")
    test_generate_itinerary()
    print("\nTesting stream_itinerary function")
    test_stream_itinerary()