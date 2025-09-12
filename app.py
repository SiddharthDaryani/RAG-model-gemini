from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import traceback
import modules  # your RAG-only modules.py

# Load env variables early
load_dotenv()

user_agent = os.getenv("USER_AGENT")
if user_agent:
    os.environ["USER_AGENT"] = user_agent
else:
    os.environ["USER_AGENT"] = "RAG-model/1.0 (siddharthdaryani49@gmail.com)"

print("USER_AGENT set to:", os.environ["USER_AGENT"])

app = FastAPI(title="Gemini RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

llm, embeddings, vector_store = modules.initialize_gemini_client()

class RAGRequest(BaseModel):
    urls: list[str]
    question: str

@app.post("/ask")
async def ask_rag(request: RAGRequest):
    try:
        modules.fetch_and_process_urls(request.urls, vector_store)
        answer = modules.retrieve_answer(request.question, vector_store, llm)
        return {"answer": answer}
    except Exception as e:
        print("Exception in /ask endpoint:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
