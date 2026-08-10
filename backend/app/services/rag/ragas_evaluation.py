import asyncio

from google import genai
from ragas.llms import llm_factory
from ragas.metrics.collections import (
    ContextPrecision,
    ContextRecall,
    Faithfulness,
    AnswerCorrectness,
)

from app.core.config import settings
from app.services.rag.run_evaluation import run_evaluation


# --------------------------------------------------
# 1. Create Gemini client for Ragas
# --------------------------------------------------

client = genai.Client(
    api_key=settings.google_api_key,
)

evaluator_llm = llm_factory(
    "gemini-2.5-flash",
    provider="google",
    client=client,
)


# --------------------------------------------------
# 2. Create Ragas metrics
# --------------------------------------------------

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
)


# --------------------------------------------------
# 3. Run evaluation
# --------------------------------------------------

async def evaluate_rag():

    results = run_evaluation()

    for result in results:

        print("\n" + "=" * 70)
        print("RAGAS EVALUATION")
        print("=" * 70)

        print("\nQUESTION:")
        print(result["question"])

        print("\nANSWER:")
        print(result["answer"])

        print("\nREFERENCE:")
        print(result["reference"])


        # Context Precision
        precision = await context_precision.ascore(
            user_input=result["question"],
            retrieved_contexts=result["contexts"],
            reference=result["reference"],
        )

        # Context Recall
        recall = await context_recall.ascore(
            user_input=result["question"],
            retrieved_contexts=result["contexts"],
            reference=result["reference"],
        )

        # Faithfulness
        faithfulness_result = await faithfulness.ascore(
            user_input=result["question"],
            retrieved_contexts=result["contexts"],
            response=result["answer"],
        )

        # Answer Correctness
        correctness = await answer_correctness.ascore(
            user_input=result["question"],
            response=result["answer"],
            reference=result["reference"],
        )


        print("\nSCORES:")

        print(f"Context Precision : {precision.value}")
        print(f"Context Recall    : {recall.value}")
        print(f"Faithfulness      : {faithfulness_result.value}")
        print(f"Answer Correctness: {correctness.value}")


if __name__ == "__main__":
    asyncio.run(evaluate_rag())