from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simulación de "base de datos"
db = None


class TextInput(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "API running"}


@app.post("/upload")
def upload_text(input: TextInput):
    global db
    db = input.text  # de momento solo guardamos el texto
    return {
        "status": "stored",
        "length": len(input.text)
    }