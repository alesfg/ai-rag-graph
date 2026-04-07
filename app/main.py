from fastapi import FastAPI
from pydantic import BaseModel
from app.llm import ask_llm
from app.embeddings import get_embeddings

app = FastAPI()

# Simulación de "base de datos"
db = None


class TextInput(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/test-llm")
def test_llm():
    response = ask_llm("Explain what RAG is in one sentence")
    return {"response": response}

@app.get("/test-embeddings")
def test_embeddings():
    embeddings = get_embeddings()
    vector = embeddings.embed_query("Hello world")

    return {
        "vector_length": len(vector),
        "sample": vector[:5]  # primeros valores
    }

@app.post("/upload")
def upload_text(input: TextInput):
    global db
    db = input.text  # de momento solo guardamos el texto
    return {
        "status": "stored",
        "length": len(input.text)
    }