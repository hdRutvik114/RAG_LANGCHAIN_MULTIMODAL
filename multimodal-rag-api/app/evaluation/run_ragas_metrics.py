
import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from litellm import OpenAI as LiteLLMClient
from litellm import OpenAI as LiteLLMClient
from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
)


# --------------------------------------------------
# 1. Project paths and environment
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "app/evaluation/ragas_dataset.json"
OUTPUT_PATH = PROJECT_ROOT / "app/evaluation/ragas_scores.json"

load_dotenv(PROJECT_ROOT / ".env")


# --------------------------------------------------
# 2. Initialize Gemini evaluator and embeddings
# --------------------------------------------------

def initialize_evaluator():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found in the project .env file"
        )

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite",
    )

    # Client for Gemini LLM evaluation through LiteLLM
    llm_client = LiteLLMClient(
        api_key=api_key,
        # model=model_name -> no need to send model name here, as it will be specified in llm_factory
    )

    llm = llm_factory(
        model_name,
        client=llm_client,
        adapter="litellm",
    )

    # Google GenAI client for embedding generation
    google_client = genai.Client(api_key=api_key)

    embeddings = GoogleEmbeddings(
        client=google_client,
        model="gemini-embedding-001",
    )

    return llm, embeddings


# --------------------------------------------------
# 3. Run RAGAS evaluation
# --------------------------------------------------

async def evaluate_records():

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {INPUT_PATH}"
        )

    with INPUT_PATH.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not records:
        raise ValueError("The evaluation dataset is empty.")

    print(f"Loaded {len(records)} evaluation records.")

    llm, embeddings = initialize_evaluator()

    # Initialize metrics
    faithfulness = Faithfulness(llm=llm)

    answer_relevancy = AnswerRelevancy(
        llm=llm,
        embeddings=embeddings,
    )

    context_precision = ContextPrecision(llm=llm)

    all_scores = []

    # Evaluate each record
    for index, record in enumerate(records, start=1):

        print(f"\n{'=' * 50}")
        print(f"Evaluating {index}/{len(records)}")
        print(f"Question: {record['user_input']}")

        # 1. Faithfulness
        faith_result = await faithfulness.ascore(
            user_input=record["user_input"],
            response=record["response"],
            retrieved_contexts=record["retrieved_contexts"],
        )

        # 2. Answer Relevancy
        relevancy_result = await answer_relevancy.ascore(
            user_input=record["user_input"],
            response=record["response"],
        )

        # 3. Context Precision
        precision_result = await context_precision.ascore(
            user_input=record["user_input"],
            reference=record["reference"],
            retrieved_contexts=record["retrieved_contexts"],
        )

        # Store results
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

    # --------------------------------------------------
    # 4. Save evaluation results
    # --------------------------------------------------

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            all_scores,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"\n{'=' * 50}")
    print("RAGAS EVALUATION COMPLETED")
    print(f"Records evaluated: {len(all_scores)}")
    print(f"Scores saved to: {OUTPUT_PATH}")


# --------------------------------------------------
# 5. Entry point
# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(evaluate_records())
