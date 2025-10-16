from dotenv import load_dotenv
import os
from typing import List
from typing_extensions import TypedDict

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain import hub

from langgraph.graph import StateGraph, START

# Load .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

prompt = hub.pull("rlm/rag-prompt")

def initialize_gemini_client():
    llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = InMemoryVectorStore(embeddings)
    return llm, embeddings, vector_store

def fetch_and_process_urls(urls: List[str], vector_store):
    loader = WebBaseLoader(web_paths=tuple(urls))
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    vector_store.add_documents(documents=all_splits)
    return all_splits

def compile_rag_graph(retrieve_fn, generate_fn):
    graph_builder = StateGraph(State).add_sequence([retrieve_fn, generate_fn])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    return graph

def retrieve_answer(question: str, vector_store, llm):
    def retrieve(state: State):
        retrieved_docs = vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}
    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}
    graph = compile_rag_graph(retrieve, generate)
    response = graph.invoke({"question": question})
    return response["answer"]
