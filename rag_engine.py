from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)

class FinancialRAG:
    def __init__(self, collection_name="financial_docs"):
        self.collection_name = collection_name
        self.client = QdrantClient(":memory:") 
        
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )
        
        self.vector_store = QdrantVectorStore(
            client=self.client, 
            collection_name=self.collection_name, 
            embedding=embeddings
        )

    def index_document(self, text, doc_id):
        chunks = text_splitter.split_text(text)
        metadatas = [{"document_id": doc_id} for _ in chunks]
        self.vector_store.add_texts(chunks, metadatas=metadatas)

    def search_pipeline(self, query):
      
        initial_results = self.vector_store.similarity_search(query, k=20)
        return initial_results[:5]

    def remove_document(self, doc_id):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter(
                must=[models.FieldCondition(key="metadata.document_id", match=models.MatchValue(value=doc_id))]
            )
        )