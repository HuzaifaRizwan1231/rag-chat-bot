from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict, List
from config.config import (
    GEMINI_API_KEY,
)


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
    def __init__(self, model="gemini-1.5-flash"):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", api_key=GEMINI_API_KEY
        )
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
        prompt = """Use ONLY the provided document context to answer.
        If answer is not found, say 'Information not available in uploaded document.'

        Question:
        {question}

        Context:
        {context}
        """

        class State(TypedDict):
            question: str
            context: List[Document]
            answer: str

        def retrieve(state: State):
            docs = self.vector_store.similarity_search(state["question"])
            return {"context": docs}

        def generate(state: State):
            ctx = "\n\n".join([d.page_content for d in state["context"]])
            final_prompt = prompt.format(question=state["question"], context=ctx)

            response = self.llm.invoke(final_prompt)
            return {"answer": response.content}

        graph = StateGraph(State)
        graph.add_node("retrieve", retrieve)
        graph.add_node("generate", generate)
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "generate")

        self.graph = graph.compile()

    def get_answer(self, question):
        return self.graph.invoke({"question": question})["answer"]
