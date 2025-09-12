# 🚀 Gemini RAG Question Answering System

Welcome to the **Gemini RAG** project! This system lets you ask questions based on the content of URLs using a Retrieval-Augmented Generation (RAG) pipeline powered by Google's Gemini model. It fetches, processes, and indexes web pages, then answers your natural language queries referencing only that context.

---

## 📋 Features (Current)

- Load and split URL contents for indexing
- Embed and store documents in-memory for quick retrieval
- Query question-answering using Gemini LLM with contextual grounding
- Simple FastAPI backend providing `/ask` POST endpoint
- Minimal static UI for entering URLs and questions
- Utilizes LangChain ecosystem libraries

---

## 💻 Getting Started

### Quick start — Clone and Setup

1. **Clone this repository:**

```
https://github.com/SiddharthDaryani/RAG-model-gemini.git
cd RAG-model-gemini
```


2. **Run the setup script:**

```
source init.setup
```

This will create a virtual environment, install all dependencies, and prepare your environment.

3. **Add your API keys:**

### Create a `.env` file in the project root with your credentials:

### GOOGLE_API_KEY=your_google_api_key_here
### USER_AGENT=RAG-model/1.0 (your_email@example.com)


4. **Open your browser and visit:**

```
http://127.0.0.1:8000/
```

---

## 📬 Contact & Support

### Questions or feedback? Open an issue or contact:

### ✉️ siddharthdaryani49@gmail.com
### [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://in.linkedin.com/in/siddharth-daryani-4339b31b9)


---

Happy querying! 🤖✨
