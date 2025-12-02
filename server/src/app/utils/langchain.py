from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict, List
from config.config import GEMINI_API_KEY, TAVILY_API_KEY
import requests


def initializeAppWorkflow(langchainModel):

    def callModel(state: MessagesState):
        response = langchainModel.invoke(state["messages"])
        return {"messages": response}

    workflow = StateGraph(state_schema=MessagesState)
    workflow.add_edge(START, "model")
    workflow.add_node("model", callModel)

    # Add memory
    memory = MemorySaver()

    return workflow.compile(checkpointer=memory)


class GeminiDocumentRAG:
    def __init__(self, model="gemini-2.5-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model, api_key=GEMINI_API_KEY)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"  # ✔ Works with API key
        )
        self.vector_store = None
        self.graph = None

    def load_document(self, file_path):
        # Load the document
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        # Build vector store
        self.vector_store = InMemoryVectorStore.from_documents(chunks, self.embeddings)

        # Build RAG graph
        self.build_graph()

    def build_graph(self):
        def retrieve_and_generate(state: MessagesState):
            history = "\n".join(
                f"{('user' if isinstance(msg, HumanMessage) else 'assistant')}: {msg.content}"
                for msg in state["messages"][
                    :-1
                ]  # everything except latest user question
            )

            user_message = state["messages"][-1].content

            # 1. Retrieve PDF chunks
            docs = self.vector_store.similarity_search(user_message)
            context = "\n\n".join([d.page_content for d in docs])

            # 2. Build prompt
            prompt = f"""
You are a chatbot with two sources of information:
1. The user's conversation history
2. The uploaded document context

RULES:
- If the user's question is about the document, answer using ONLY the document context.
- If the user's question is about the conversation, memory, previous messages, or is general chat, IGNORE the document and answer normally.
- If the question is about the document but the answer is not present in the document, say:
  "Information not available in uploaded document."

Conversation History:
{history}

Document Context:
{context}

User Question:
{user_message}

Provide the best answer.
"""

            # 3. LLM call
            response = self.llm.invoke(prompt)

            # 4. Append assistant message to history
            return {"messages": [AIMessage(response.content)]}

        graph = StateGraph(MessagesState)
        graph.add_node("rag", retrieve_and_generate)
        graph.add_edge(START, "rag")

        memory = MemorySaver()

        self.graph = graph.compile(checkpointer=memory)

    def get_answer(self, text, chatId):
        input_messages = [HumanMessage(text)]
        config = {"configurable": {"thread_id": str(chatId)}}

        response = self.graph.invoke({"messages": input_messages}, config)

        return response["messages"][-1].content


class CRAGState(MessagesState):
    context: list
    web_context: str


class GeminiDocumentCRAG:
    def __init__(self, model="gemini-2.5-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model, api_key=GEMINI_API_KEY)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"
        )
        self.vector_store = None
        self.graph = None

    def load_document(self, file_path):
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        self.vector_store = InMemoryVectorStore.from_documents(chunks, self.embeddings)

        self.build_graph()

    def judge_relevance(self, question, docs):
        if not docs:
            return 0.0

        scores = []

        for d in docs:
            prompt = f"""
You are an AI relevance judge.
Given the question and the retrieved text chunk, rate relevance from 0 to 1.

Question: {question}

Chunk:
{d.page_content}

Respond ONLY with a number between 0 and 1.
"""
            res = self.llm.invoke(prompt).content.strip()

            # Convert string → float safely
            try:
                score = float(res)
            except:
                score = 0.0

            scores.append(score)

        return sum(scores) / len(scores)

    def web_search(self, query):

        url = "https://api.tavily.com/search"
        payload = {"api_key": TAVILY_API_KEY, "query": query, "max_results": 5}

        try:
            response = requests.post(url, json=payload).json()
            results = "\n\n".join([r["content"] for r in response.get("results", [])])
        except:
            results = ""

        return results or "No relevant info found on the web."

    def build_graph(self):

        def retrieve(state: CRAGState):
            question = state["messages"][-1].content
            docs = self.vector_store.similarity_search(question)
            relevance = self.judge_relevance(question, docs)

            print(f"Relevance score: {relevance}")

            if relevance < 0.2:
                return {"context": [], "web_context": "USE_WEB"}
            else:
                return {"context": docs, "web_context": ""}

        def web_lookup(state: CRAGState):
            question = state["messages"][-1].content

            if state["web_context"] == "USE_WEB":
                result = self.web_search(question)
                return {"web_context": result}

            return state

        def generate(state: CRAGState):
            # --- Build chat history ---
            history = "\n".join(
                f"{('user' if isinstance(msg, HumanMessage) else 'assistant')}: {msg.content}"
                for msg in state["messages"][
                    :-1
                ]  # everything except latest user question
            )

            current_question = state["messages"][-1].content

            # --- Build context ---
            if state["context"]:
                ctx = "\n\n".join([d.page_content for d in state["context"]])
            else:
                ctx = state["web_context"]

            # --- Final prompt ---
            prompt = f"""
You are a helpful assistant.

# Chat History:
{history}

# Context:
{ctx}

# User Question:
{current_question}

Answer using BOTH chat history and context.
If neither contains the answer, reply:
"Information not available."
"""
            response = self.llm.invoke(prompt)
            return {"messages": [AIMessage(content=response.content)]}

        graph = StateGraph(CRAGState)
        graph.add_node("retrieve", retrieve)
        graph.add_node("web_lookup", web_lookup)
        graph.add_node("generate", generate)

        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "web_lookup")
        graph.add_edge("web_lookup", "generate")

        memory = MemorySaver()
        self.graph = graph.compile(checkpointer=memory)

    def get_answer(self, question, thread_id):
        return self.graph.invoke(
            {"messages": [HumanMessage(content=question)]},
            {"configurable": {"thread_id": str(thread_id)}},
        )["messages"][-1].content
