from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from ragas.llms import llm_factory

from ragas.metrics.collections import (
    ContextPrecision,
    ContextRecall,
    Faithfulness,
    AnswerCorrectness,
)

from app.core.config import settings
from app.services.rag.run_evaluation import run_evaluation


# ============================================================
# 1. Gemini client
# ============================================================

client = genai.Client(
    api_key=settings.google_api_key,
)


# ============================================================
# 2. Ragas evaluator LLM
# ============================================================

evaluator_llm = llm_factory(
    "gemini-2.5-flash",
    provider="google",
    client=client,
)


# ============================================================
# 3. Gemini embeddings
# ============================================================

evaluator_embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    google_api_key=settings.google_api_key,
)


# ============================================================
# 4. Ragas metrics
# ============================================================

context_precision = ContextPrecision(
    llm=evaluator_llm,
)

context_recall = ContextRecall(
    llm=evaluator_llm,
)

faithfulness = Faithfulness(
    llm=evaluator_llm,
)

answer_correctness = AnswerCorrectness(
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
)


# ============================================================
# 5. Run evaluation
# ============================================================

def evaluate_rag():

    print("\n")
    print("=" * 70)
    print("RUNNING RAG EVALUATION")
    print("=" * 70)

    results = run_evaluation()

    all_scores = []

    for index, result in enumerate(results, start=1):

        question = result["question"]
        answer = result["answer"]
        contexts = result["contexts"]
        reference = result["ground_truth"]

        print("\n")
        print("=" * 70)
        print(f"TEST CASE {index}")
        print("=" * 70)

        print("\nQUESTION:")
        print(question)

        print("\nANSWER:")
        print(answer)

        print("\nREFERENCE:")
        print(reference)

        # ====================================================
        # Context Precision
        # ====================================================

        precision = context_precision.score(
            user_input=question,
            retrieved_contexts=contexts,
            reference=reference,
        )

        # ====================================================
        # Context Recall
        # ====================================================

        recall = context_recall.score(
            user_input=question,
            retrieved_contexts=contexts,
            reference=reference,
        )

        # ====================================================
        # Faithfulness
        # ====================================================

        faithfulness_result = faithfulness.score(
            user_input=question,
            retrieved_contexts=contexts,
            response=answer,
        )

        # ====================================================
        # Answer Correctness
        # ====================================================

        correctness = answer_correctness.score(
            user_input=question,
            response=answer,
            reference=reference,
        )

        # ====================================================
        # Extract scores
        # ====================================================

        precision_score = precision.value
        recall_score = recall.value
        faithfulness_score = faithfulness_result.value
        correctness_score = correctness.value

        # ====================================================
        # Print scores
        # ====================================================

        print("\nSCORES:")

        print(
            f"Context Precision : {precision_score:.4f}"
        )

        print(
            f"Context Recall    : {recall_score:.4f}"
        )

        print(
            f"Faithfulness      : {faithfulness_score:.4f}"
        )

        print(
            f"Answer Correctness: {correctness_score:.4f}"
        )

        # ====================================================
        # Store scores
        # ====================================================

        all_scores.append(
            {
                "question": question,
                "context_precision": precision_score,
                "context_recall": recall_score,
                "faithfulness": faithfulness_score,
                "answer_correctness": correctness_score,
            }
        )

    # ========================================================
    # Overall scores
    # ========================================================

    print("\n")
    print("=" * 70)
    print("OVERALL RAGAS RESULTS")
    print("=" * 70)

    if not all_scores:

        print("No evaluation results.")

        return

    avg_precision = sum(
        result["context_precision"]
        for result in all_scores
    ) / len(all_scores)

    avg_recall = sum(
        result["context_recall"]
        for result in all_scores
    ) / len(all_scores)

    avg_faithfulness = sum(
        result["faithfulness"]
        for result in all_scores
    ) / len(all_scores)

    avg_correctness = sum(
        result["answer_correctness"]
        for result in all_scores
    ) / len(all_scores)

    print(
        f"\nAverage Context Precision : "
        f"{avg_precision:.4f}"
    )

    print(
        f"Average Context Recall    : "
        f"{avg_recall:.4f}"
    )

    print(
        f"Average Faithfulness      : "
        f"{avg_faithfulness:.4f}"
    )

    print(
        f"Average Answer Correctness: "
        f"{avg_correctness:.4f}"
    )


# ============================================================
# 6. Entry point
# ============================================================

if __name__ == "__main__":
    evaluate_rag()