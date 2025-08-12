import requests
import json
from django.http import JsonResponse
from .chroma_client import add_to_chroma, get_context

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # or "mistral", etc.


def generate_response(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Request to Ollama failed: {e}")
        print(f"Payload: {payload}")
        if response is not None:
            print(f"Response content: {response.content}")
        raise

def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
        prompt = data.get("prompt", "").strip()
        user_id = data.get("user_id", "anonymous")

        if not prompt:
            return JsonResponse({"error": "Empty prompt"}, status=400)

        # Get stored context for this user
        context = get_context(user_id, prompt)

        # Merge context with user prompt
        final_prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}"

        # Generate answer using Ollama
        answer = generate_response(final_prompt)

        # Store question + answer in ChromaDB
        add_to_chroma(user_id, prompt, answer)

        return JsonResponse({"response": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


    #! to pull in the container specific model:  docker-compose exec ollama ollama pull llama3 