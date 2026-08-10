from app.services.rag.retriever import qdrant
from app.services.llm import generate_response

question = "What should I do if my tracking says delivered but I cannot find my package?"

expected_source = "shipping.md"

expected_information = """
The customer should:
1. Check secondary entrance areas, patios, back porches, and leasing offices.
2. Check with household members or neighbors.
3. Wait another 24 hours because carriers may mark packages as delivered early.
4. If the package is still missing after 48 hours, contact AcmeStore Support.
5. AcmeStore will then start an investigation, which takes 5 to 7 business days.
"""


print("=" * 70)
print("RAG EVALUATION")
print("=" * 70)

print("\nQUESTION:")
print(question)

print("\nEXPECTED INFORMATION:")
print(expected_information)

print("\nEXPECTED SOURCE:")
print(expected_source)


# --------------------------------------------------
# 1. RETRIEVAL
# --------------------------------------------------

search_results = qdrant.similarity_search(
    query=question,
    k=5,
)


print("\n" + "=" * 70)
print("RETRIEVED CONTEXT")
print("=" * 70)

for i, result in enumerate(search_results, start=1):
    print(f"\n{'-' * 70}")
    print(f"RESULT {i}")

    print(f"SOURCE: {result.metadata.get('source')}")

    print("\nCONTENT:")
    print(result.page_content)

    # Simple manual relevance check
    if expected_source in result.metadata.get("source", ""):
        print("\nSOURCE CHECK: ✅ Expected source")
    else:
        print("\nSOURCE CHECK: ❌ Different source")


# --------------------------------------------------
# 2. RETRIEVAL SUMMARY
# --------------------------------------------------

expected_source_count = sum(
    1
    for result in search_results
    if expected_source in result.metadata.get("source", "")
)

print("\n" + "=" * 70)
print("RETRIEVAL SUMMARY")
print("=" * 70)

print(f"Expected source: {expected_source}")
print(f"Retrieved chunks: {len(search_results)}")
print(f"Chunks from expected source: {expected_source_count}")


# --------------------------------------------------
# 3. GENERATION
# --------------------------------------------------

context = "\n\n".join(
    [
        f"Source: {result.metadata.get('source')}\n"
        f"Content: {result.page_content}"
        for result in search_results
    ]
)

messages = [
    {
        "role": "user",
        "content": question,
    }
]

answer = generate_response(messages, context)

print("\n" + "=" * 70)
print("GENERATED ANSWER")
print("=" * 70)

print(answer)


print("\n" + "=" * 70)
print("CONTEXT SENT TO LLM")
print("=" * 70)

# print(context)


# --------------------------------------------------
# IMPORTANT:
# For now, don't automatically judge the answer.
# We will manually inspect it.
# --------------------------------------------------

print("\n" + "=" * 70)
print("MANUAL EVALUATION")
print("=" * 70)

print("""
After running this test, answer these questions:

1. Did retrieval find the correct document?
2. Did retrieval find all information required to answer the question?
3. How many retrieved chunks were actually useful?
4. How many retrieved chunks were irrelevant?
5. Does the generated answer contain information supported by the context?
6. Did the answer miss any important information?
7. Did the answer invent anything?
8. Is the final answer correct?
""")