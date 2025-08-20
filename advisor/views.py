import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import logging

from .ollama_client import generate_response
# You'll add get_all_prompts
from .chroma_client import get_context, add_to_chroma, get_all_prompts


logger = logging.getLogger(__name__)


def chat_page(request):
    """Generator page."""
    context = {
        'show_chat_widget': False,
    }
    return render(request, "chat.html", context)


def prompts_page(request):
    """History page."""
    try:
        prompts_and_responses = get_all_prompts()  # Returns list of (prompt, response)
        print(f"Retrieved {len(prompts_and_responses)} {prompts_and_responses} prompts and responses from ChromaDB")
        # Reverse order so latest comes first
        prompts_and_responses.reverse()
    except Exception as e:
        prompts_and_responses = []
    return render(request, "prompts.html", {"prompts_and_responses": prompts_and_responses})

@csrf_exempt
def chat_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    prompt = data.get("prompt")
    user_id = data.get("user_id", "anonymous")

    if not prompt:
        return JsonResponse({"error": "Missing prompt"}, status=400)

    try:
        # Step 1: Get context from ChromaDB
        context = get_context(user_id, prompt)
        full_prompt = f"{context}\n\nUser: {prompt}" if context else prompt

        # Step 2: Generate response from Ollama (or your LLM service)
        response = generate_response(full_prompt)
        if not response:
            # Defensive: Make sure response is never None or empty string
            response = "No response generated."

        # Step 3: Save Q/A to ChromaDB
        add_to_chroma(user_id, prompt, response)

        # Always return response
        return JsonResponse({"response": response})

    except Exception as e:
        # Log the error for diagnostics
        logger.exception("Error in chat_view")
        return JsonResponse({"error": "Internal server error"}, status=500)

# @csrf_exempt
# def chat_view(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid method"}, status=405)

#     data = json.loads(request.body)
#     prompt = data.get("prompt")
#     user_id = data.get("user_id", "anonymous")

#     if not prompt:
#         return JsonResponse({"error": "Missing prompt"}, status=400)

#     try:
#         # Step 1: Get context from ChromaDB
#         context = get_context(user_id, prompt)
#         full_prompt = f"{context}\n\nUser: {prompt}" if context else prompt

#         # Step 2: Generate response from Ollama
#         response = generate_response(full_prompt)

#         # Step 3: Save Q/A to ChromaDB
#         add_to_chroma(user_id, prompt, response)

#         return JsonResponse({"response": response})

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
