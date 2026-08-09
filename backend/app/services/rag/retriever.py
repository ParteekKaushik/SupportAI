
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from app.core.config import settings


embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    api_key=settings.google_api_key
)


qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333/",
    collection_name="AcmeStore",
)

def retrieve_context(query: str) -> str:
    search_results = qdrant.similarity_search(query=query, k=5)
    context = "\n\n".join(
        [
            f"Source: {result.metadata.get('source')}\n"
            f"Content: {result.page_content}"
            for result in search_results
        ]
    )
    return context








