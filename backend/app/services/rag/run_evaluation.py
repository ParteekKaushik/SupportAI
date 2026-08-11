from app.services.rag.retriever import retrieve_context
from app.services.llm import generate_response
from app.services.rag.evaluation_dataset import evaluation_dataset


def run_evaluation():

    results = []

    for test_case in evaluation_dataset:

        question = test_case["question"]
        expected_answer = test_case["expected_answer"]

        # ----------------------------------------------------
        # 1. Retrieve context
        # ----------------------------------------------------

        context = retrieve_context(question)

        # ----------------------------------------------------
        # 2. Generate answer
        # ----------------------------------------------------

        messages = [
            {
                "role": "user",
                "content": question,
            }
        ]

        answer = generate_response(
            messages,
            context,
        )

        # ----------------------------------------------------
        # 3. Store result
        # ----------------------------------------------------

        result = {
            "question": question,
            "contexts": context,
            "answer": answer,
            "ground_truth": expected_answer,
        }

        results.append(result)

        # ----------------------------------------------------
        # 4. Display test case
        # ----------------------------------------------------

        print("\n" + "=" * 70)

        print("QUESTION:")
        print(question)

        print("\nRETRIEVED CONTEXT:")
        print(context)

        print("\nGENERATED ANSWER:")
        print(answer)

        print("\nEXPECTED ANSWER:")
        print(expected_answer)

    return results


if __name__ == "__main__":
    run_evaluation()