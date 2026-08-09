
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.get("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)



embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)


qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333/",
    collection_name="AcmeStore",
)


user_query = input("Ask: ")

search_results = qdrant.similarity_search(query=user_query, k=5)

# Debug retrieved chunks
for i, result in enumerate(search_results, start=1):
    print(f"\n{'=' * 60}")
    print(f"RESULT {i}")
    print(f"SOURCE: {result.metadata.get('source')}")
    print(result.page_content)

context = "\n\n".join(
    [
        f"Source: {result.metadata.get('source')}\n"
        f"Content: {result.page_content}"
        for result in search_results
    ]
)

SYSTEM_PROMPT= f"""
Role:
You are SupportAI.

Task: 
You need to help in resolving user queries related to support.

Requirements:
- Use easy english words to answer. 
- Use the provided context to answer the customer.
- If the answer isn't present in the context, say you don't have enough information.
- Do not invent information yourself.
- Answer questions only related to company policies.
- If question is not related to company policies, deny politely.

CONTEXT:
{context}
"""

response = client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[
        {
            "role": "user",
            "content": user_query
        },
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
)

print("\n Assitant Answer: ")
print(response.choices[0].message.content)