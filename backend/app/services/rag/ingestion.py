
from langchain_community.document_loaders import  DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

loader = DirectoryLoader(
    path="../../../data/knowledge",
    glob="**/*.md",
    loader_cls=TextLoader,
    show_progress=False
)
documents=loader.load()


text_splitter = MarkdownTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    add_start_index=True
)

chunks = text_splitter.split_documents(documents)
# print(chunks)



embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)


qdrant = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333/",
    collection_name="AcmeStore",
)

print("Indexing of documents done using langchain")
