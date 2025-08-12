from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(
    chroma_server_host="localhost",
    chroma_server_http_port=8001,  # integer, NOT string

    # chroma_server_host="chromadb",
    # chroma_server_http_port=8000,
))

COLLECTION_NAME = "advisor_context"


def get_or_create_collection():
    return client.get_or_create_collection(COLLECTION_NAME)


def add_to_chroma(user_id: str, question: str, answer: str):
    collection = get_or_create_collection()
    collection.add(
        ids=[f"{user_id}_{question[:16]}"],  # keep IDs unique-ish
        documents=[question + "\n\n" + answer],  # store both Q and A
        metadatas=[{"user_id": user_id}]
    )


def get_context(user_id: str, question: str) -> str:
    collection = get_or_create_collection()
    results = collection.query(
        query_texts=[question],
        n_results=3,
        where={"user_id": user_id}
    )
    docs = results.get("documents", [[]])[0]
    return "\n".join(docs)


def get_all_prompts():
    """
    Fetch all stored Q/A pairs from ChromaDB and return as a list of (prompt, response) tuples,
    reversed so the newest entries come first.
    """
    collection = get_or_create_collection()
    results = collection.get()  # fetches all documents

    prompts_and_responses = []
    for doc in results.get("documents", []):
        parts = doc.split("\n\n", 1)
        prompt = parts[0] if parts else ""
        response = parts[1] if len(parts) > 1 else ""
        prompts_and_responses.append((prompt, response))

    # Reverse the list so latest entries appear first
    return list(reversed(prompts_and_responses))
