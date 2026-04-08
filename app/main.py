from fastapi import FastAPI
from pydantic import BaseModel
from app.llm import ask_llm
from app.embeddings import get_embeddings
from app.vector_store import create_vector_store, search
from app.rag import rag_query
from app.graph import extract_relations, add_relation
from app.graph import get_graph
from app.neo4j_graph import Neo4jGraph

app = FastAPI()

# Simulación de "base de datos"
db = None

graph_db = Neo4jGraph()

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

@app.get("/search")
def search_text(query: str):
    if db is None:
        return {"error": "No data uploaded yet"}

    results = search(db, query)

    return {"results": results}

@app.get("/ask")
def ask(query: str):
    if db is None:
        return {"error": "No data uploaded yet"}

    answer = rag_query(db, query)

    return {"answer": answer}

@app.post("/upload")
def upload_text(input: TextInput):
    global db
    db = create_vector_store(input.text)

    relations = extract_relations(input.text)

    try:
        for e1, e2 in relations:
            graph_db.add_relation(e1, e2)
    except Exception as e:
        print("Neo4j error:", e)

    return {
        "status": "indexed",
        "relations": relations
    }


@app.get("/graph")
def view_graph():
    return get_graph()

@app.get("/graph/{entity}")
def get_graph_relations(entity: str):
    relations = graph_db.get_relations(entity)
    return {"entity": entity, "relations": relations}

