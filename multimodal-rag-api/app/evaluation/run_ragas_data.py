import json
from pathlib import Path

from app.api.dependencies import get_rag_service


DOCUMENT_ID = "91372821b401012093d6ef43a2bc6f87a1073fbcd4c2e64fb00217b3e1a0f052"

INPUT_PATH = Path("app/evaluation/question_enriched.json")
OUTPUT_PATH = Path("app/evaluation/ragas_dataset.json")

# Start small. We'll increase this to 15 after testing.
MAX_QUESTIONS = 2


def generate_evaluation_data():

    with INPUT_PATH.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    rag_service = get_rag_service()

    evaluation_records = []

    for index, item in enumerate(questions[:MAX_QUESTIONS], start=1):

        question = item["question"]

        print(f"\nProcessing question {index}/{MAX_QUESTIONS}")
        print(f"Question: {question}")

        result = rag_service.answer(
            question=question,
            top_k=5,
            candidate_k=20,
            document_id=DOCUMENT_ID,
        )

        record = {
            "user_input": question,
            "retrieved_contexts": result["retrieval_context"],
            "response": result["answer"],
            "reference": item["expected_answer"],
            "reference_contexts": item["reference_context"],
        }

        evaluation_records.append(record)

        print(f"Retrieved contexts: {len(result['retrieval_context'])}")
        print(f"Generated answer: {result['answer'][:250]}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            evaluation_records,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"\nEvaluation data saved to: {OUTPUT_PATH}")
    print(f"Total records: {len(evaluation_records)}")


if __name__ == "__main__":
    generate_evaluation_data()