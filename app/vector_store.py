from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter


def create_vector_store(text: str):
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.create_documents([text])

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    db = FAISS.from_documents(docs, embeddings)

    return db


def search(db, query: str):
    results = db.similarity_search(query, k=3)
    return [doc.page_content for doc in results]