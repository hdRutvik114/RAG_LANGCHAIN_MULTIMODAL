import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
)


load_dotenv()

INPUT_PATH = Path("app/evaluation/ragas_dataset.json")
OUTPUT_PATH = Path("app/evaluation/ragas_scores.json")


def initialize_evaluator():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY was not found in .env")

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite",
    )

    client = genai.Client(api_key=api_key)

    llm = llm_factory(
        model_name,
        provider="google",
        client=client,
    )

    embeddings = GoogleEmbeddings(
        client=client,
        model="gemini-embedding-001",
    )

    return llm, embeddings


async def evaluate_records():

    with INPUT_PATH.open("r", encoding="utf-8") as file:
        records = json.load(file)

    llm, embeddings = initialize_evaluator()

    faithfulness = Faithfulness(llm=llm)

    answer_relevancy = AnswerRelevancy(
        llm=llm,
        embeddings=embeddings,
    )

    context_precision = ContextPrecision(llm=llm)

    all_scores = []

    for index, record in enumerate(records, start=1):

        print(f"\nEvaluating {index}/{len(records)}")
        print(record["user_input"])

        faith_result = await faithfulness.ascore(
            user_input=record["user_input"],
            response=record["response"],
            retrieved_contexts=record["retrieved_contexts"],
        )

        relevancy_result = await answer_relevancy.ascore(
            user_input=record["user_input"],
            response=record["response"],
        )

        precision_result = await context_precision.ascore(
            user_input=record["user_input"],
            reference=record["reference"],
            retrieved_contexts=record["retrieved_contexts"],
        )

        scores = {
            "question": record["user_input"],
            "faithfulness": faith_result.value,
            "answer_relevancy": relevancy_result.value,
            "context_precision": precision_result.value,
        }

        all_scores.append(scores)

        print(f"Faithfulness: {faith_result.value:.3f}")
        print(f"Answer Relevancy: {relevancy_result.value:.3f}")
        print(f"Context Precision: {precision_result.value:.3f}")

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(all_scores, file, indent=4, ensure_ascii=False)

    print(f"\nScores saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(evaluate_records())