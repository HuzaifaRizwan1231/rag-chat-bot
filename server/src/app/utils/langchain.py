from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from typing_extensions import TypedDict, List
import os

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
     

class MergestackLangchainAssistant:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model):
        if not hasattr(self, 'initialized'):
            self.graph = None
            self.initialized = False
            self.initialize(model)
            self.initialized = True
            
    def initialize(self, model):
        
        if not self.initialized:
            # Select model and embeddings
            llm = ChatOpenAI(model=model)
            embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
            
            # Load the PDF
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            file_path = os.path.join(base_dir, "uploads", "mergestack_policy.pdf")
            
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            # SPlit the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            all_splits = text_splitter.split_documents(docs)
            
            # Create the vector store
            vector_store = InMemoryVectorStore.from_documents(docs, embeddings)

            # Index chunks
            _ = vector_store.add_documents(documents=all_splits)
            
            prompt = hub.pull("rlm/rag-prompt")
            
            class State(TypedDict):
                question: str
                context: List[Document]
                answer: str

            # Define application steps
            def retrieve(state: State):
                retrieved_docs = vector_store.similarity_search(state["question"])
                return {"context": retrieved_docs}

            def generate(state: State):
                docs_content = "\n\n".join(doc.page_content for doc in state["context"])
                messages = prompt.invoke({"question": state["question"], "context": docs_content})
                response = llm.invoke(messages)
                return {"answer": response.content}

            # Compile application and test
            graph_builder = StateGraph(State).add_sequence([retrieve, generate])
            graph_builder.add_edge(START, "retrieve")
            self.graph = graph_builder.compile()
        
    def getResponse(self, text):
        return self.graph.invoke({"question": text})["answer"]
    
from config.config import (
    GEMINI_API_KEY,
    ALLOWED_GEMINI_MODELS,
)
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

class GeminiDocumentRAG:
    def __init__(self, model="gemini-1.5-flash"):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GEMINI_API_KEY)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"   # ✔ Works with API key
        )
        self.vector_store = None
        self.graph = None
    
    def load_document(self, file_path):
        loader = PyPDFLoader(file_path)
        docs = loader.load()

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