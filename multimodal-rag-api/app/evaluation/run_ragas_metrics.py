# import asyncio
# import json
# import os
# import sys
# from pathlib import Path
# from statistics import mean

# from dotenv import load_dotenv
# from google import genai
# from openai import AsyncOpenAI
# from ragas.llms import llm_factory
# from ragas.embeddings import GoogleEmbeddings
# from ragas.metrics.collections import (
#     Faithfulness,
#     AnswerRelevancy,
#     ContextPrecision,
# )


# # --------------------------------------------------
# # 1. Paths and configuration
# # --------------------------------------------------

# ROOT_DIR = Path(__file__).resolve().parents[2]

# DATASET_PATH = ROOT_DIR / "app" / "evaluation" / "ragas_dataset.json"
# OUTPUT_PATH = ROOT_DIR / "app" / "evaluation" / "ragas_results.json"

# # Load environment variables from the project's .env
# load_dotenv(ROOT_DIR / ".env")

# API_KEY = os.getenv("GEMINI_API_KEY")

# # Prefer a dedicated evaluation model if configured.
# # Otherwise, use the same model configured for your application.
# MODEL_NAME = (
#     os.getenv("RAGAS_GEMINI_MODEL")
#     or os.getenv("GEMINI_MODEL")
#     or "gemini-2.0-flash"
# )

# EMBEDDING_MODEL = "gemini-embedding-001"


# # --------------------------------------------------
# # 2. Validate dataset
# # --------------------------------------------------

# def load_dataset():
#     if not DATASET_PATH.exists():
#         raise FileNotFoundError(
#             f"Dataset not found: {DATASET_PATH}"
#         )

#     with open(DATASET_PATH, "r", encoding="utf-8") as file:
#         dataset = json.load(file)

#     if not isinstance(dataset, list) or not dataset:
#         raise ValueError("RAGAS dataset is empty or invalid.")

#     required_fields = [
#         "user_input",
#         "retrieved_contexts",
#         "response",
#         "reference",
#     ]

#     for index, record in enumerate(dataset):
#         for field in required_fields:
#             if field not in record:
#                 raise ValueError(
#                     f"Record {index + 1} is missing '{field}'."
#                 )

#         if not isinstance(record["retrieved_contexts"], list):
#             raise ValueError(
#                 f"Record {index + 1}: retrieved_contexts must be a list."
#             )

#     return dataset


# # --------------------------------------------------
# # 3. Initialize Gemini evaluator
# # --------------------------------------------------

# def initialize_evaluator():

#     api_key = os.getenv("GEMINI_API_KEY")

#     if not api_key:
#         raise ValueError("GEMINI_API_KEY was not found in .env")

#     model_name = os.getenv(
#         "GEMINI_MODEL",
#         "gemini-2.5-flash",
#     )

#     # Gemini through Google's OpenAI-compatible endpoint
#     llm_client = AsyncOpenAI(
#         api_key=api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

#     # Use Instructor's OpenAI adapter
#     llm = llm_factory(
#         model_name,
#         provider="openai",
#         client=llm_client,
#         adapter="instructor",
#     )

#     # Separate Google client for embeddings
#     google_client = genai.Client(api_key=api_key)

#     embeddings = GoogleEmbeddings(
#         client=google_client,
#         model="gemini-embedding-001",
#     )

#     return llm, embeddings

# # --------------------------------------------------
# # 4. Evaluate one record
# # --------------------------------------------------

# async def evaluate_record(
#     record,
#     faithfulness_metric,
#     relevancy_metric,
#     context_precision_metric,
# ):
#     user_input = record["user_input"]
#     response = record["response"]
#     retrieved_contexts = record["retrieved_contexts"]
#     reference = record["reference"]

#     # Faithfulness:
#     # Is the generated answer supported by retrieved context?
#     faithfulness_result = await faithfulness_metric.ascore(
#         user_input=user_input,
#         response=response,
#         retrieved_contexts=retrieved_contexts,
#     )

#     # Answer Relevancy:
#     # Does the generated answer address the question?
#     relevancy_result = await relevancy_metric.ascore(
#         user_input=user_input,
#         response=response,
#     )

#     # Context Precision:
#     # Are relevant retrieved contexts ranked higher?
#     context_precision_result = await context_precision_metric.ascore(
#         user_input=user_input,
#         reference=reference,
#         retrieved_contexts=retrieved_contexts,
#     )

#     return {
#         "question": user_input,
#         "faithfulness": faithfulness_result.value,
#         "answer_relevancy": relevancy_result.value,
#         "context_precision": context_precision_result.value,
#     }


# # --------------------------------------------------
# # 5. Main evaluation workflow
# # --------------------------------------------------

# async def main():
#     print("\nLoading RAGAS dataset...")

#     dataset = load_dataset()

#     print(f"Loaded {len(dataset)} records.")

#     print("\nInitializing Gemini evaluator...")

#     llm, embeddings = initialize_evaluator()

#     # Initialize RAGAS metrics
#     faithfulness_metric = Faithfulness(llm=llm)

#     relevancy_metric = AnswerRelevancy(
#         llm=llm,
#         embeddings=embeddings,
#     )

#     context_precision_metric = ContextPrecision(llm=llm)

#     print(f"Evaluator model: {MODEL_NAME}")
#     print(f"Embedding model: {EMBEDDING_MODEL}")

#     print("\nStarting RAGAS evaluation...\n")

#     results = []

#     for index, record in enumerate(dataset, start=1):
#         print(f"Evaluating question {index}/{len(dataset)}...")

#         result = await evaluate_record(
#             record=record,
#             faithfulness_metric=faithfulness_metric,
#             relevancy_metric=relevancy_metric,
#             context_precision_metric=context_precision_metric,
#         )

#         results.append(result)

#         print(f"Faithfulness:      {result['faithfulness']:.4f}")
#         print(f"Answer Relevancy:  {result['answer_relevancy']:.4f}")
#         print(f"Context Precision: {result['context_precision']:.4f}")
#         print("-" * 45)

#     # --------------------------------------------------
#     # 6. Calculate average scores
#     # --------------------------------------------------

#     summary = {
#         metric: mean(item[metric] for item in results)
#         for metric in [
#             "faithfulness",
#             "answer_relevancy",
#             "context_precision",
#         ]
#     }

#     output = {
#         "evaluator_model": MODEL_NAME,
#         "embedding_model": EMBEDDING_MODEL,
#         "total_questions": len(results),
#         "individual_results": results,
#         "average_scores": summary,
#     }

#     # --------------------------------------------------
#     # 7. Save results
#     # --------------------------------------------------

#     with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
#         json.dump(output, file, indent=4, ensure_ascii=False)

#     print("\n========== RAGAS EVALUATION SUMMARY ==========")

#     for metric, score in summary.items():
#         print(f"{metric}: {score:.4f}")

#     print("\nResults saved to:")
#     print(OUTPUT_PATH)


# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import json
import os
from pathlib import Path
from statistics import mean

from dotenv import load_dotenv
from google import genai
from openai import AsyncOpenAI

from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
)


# --------------------------------------------------
# 1. Paths and configuration
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = ROOT_DIR / "app" / "evaluation" / "ragas_dataset.json"
OUTPUT_PATH = ROOT_DIR / "app" / "evaluation" / "ragas_results.json"
CHECKPOINT_PATH = ROOT_DIR / "app" / "evaluation" / "ragas_checkpoint.json"

load_dotenv(ROOT_DIR / ".env")

MODEL_NAME = (
    os.getenv("RAGAS_GEMINI_MODEL")
    or os.getenv("GEMINI_MODEL")
    or "gemini-2.0-flash"
)

EMBEDDING_MODEL = "gemini-embedding-001"

METRIC_NAMES = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
]


# --------------------------------------------------
# 2. Load API keys
# --------------------------------------------------

def load_api_keys():

    keys = []

    for index in range(1, 5):
        key = os.getenv(f"GEMINI_API_KEY_{index}")

        if key and key.strip():
            keys.append(key.strip())

    # Backward compatibility with the old .env variable
    if not keys:
        old_key = os.getenv("GEMINI_API_KEY")

        if old_key and old_key.strip():
            keys.append(old_key.strip())

    if not keys:
        raise ValueError(
            "No Gemini API keys found. Configure GEMINI_API_KEY_1, "
            "GEMINI_API_KEY_2, etc. in .env"
        )

    print(f"Loaded {len(keys)} Gemini API key(s).")

    return keys


# --------------------------------------------------
# 3. Validate dataset
# --------------------------------------------------

def load_dataset():

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list) or not dataset:
        raise ValueError("RAGAS dataset is empty or invalid.")

    required_fields = [
        "user_input",
        "retrieved_contexts",
        "response",
        "reference",
    ]

    for index, record in enumerate(dataset):

        for field in required_fields:
            if field not in record:
                raise ValueError(
                    f"Record {index + 1} is missing '{field}'."
                )

        if not isinstance(record["retrieved_contexts"], list):
            raise ValueError(
                f"Record {index + 1}: retrieved_contexts must be a list."
            )

    return dataset


# --------------------------------------------------
# 4. Initialize evaluator for each API key
# --------------------------------------------------

def initialize_evaluator(api_key):

    # Gemini through Google's OpenAI-compatible endpoint
    llm_client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    llm = llm_factory(
        MODEL_NAME,
        provider="openai",
        client=llm_client,
        adapter="instructor",
    )

    # Separate Google client for embeddings
    google_client = genai.Client(api_key=api_key)

    embeddings = GoogleEmbeddings(
        client=google_client,
        model=EMBEDDING_MODEL,
    )

    return {
        "faithfulness": Faithfulness(llm=llm),

        "answer_relevancy": AnswerRelevancy(
            llm=llm,
            embeddings=embeddings,
        ),

        "context_precision": ContextPrecision(llm=llm),
    }


# --------------------------------------------------
# 5. Detect HTTP 429 errors
# --------------------------------------------------

def is_rate_limit_error(error):

    # Inspect the exception and any wrapped exceptions.
    pending = [error]
    visited = set()

    while pending:

        current = pending.pop()

        if current is None or id(current) in visited:
            continue

        visited.add(id(current))

        status_code = getattr(current, "status_code", None)

        if status_code is None:
            response = getattr(current, "response", None)
            status_code = getattr(response, "status_code", None)

        if status_code == 429:
            return True

        pending.append(getattr(current, "__cause__", None))
        pending.append(getattr(current, "__context__", None))

    return False


# --------------------------------------------------
# 6. Run a metric with API key rotation
# --------------------------------------------------

async def run_metric_with_rotation(
    metric_name,
    record,
    evaluators,
    start_index,
):

    total_keys = len(evaluators)

    for attempt in range(total_keys):

        key_index = (start_index + attempt) % total_keys

        metric = evaluators[key_index][metric_name]

        try:

            if metric_name == "faithfulness":

                result = await metric.ascore(
                    user_input=record["user_input"],
                    response=record["response"],
                    retrieved_contexts=record["retrieved_contexts"],
                )

            elif metric_name == "answer_relevancy":

                result = await metric.ascore(
                    user_input=record["user_input"],
                    response=record["response"],
                )

            elif metric_name == "context_precision":

                result = await metric.ascore(
                    user_input=record["user_input"],
                    reference=record["reference"],
                    retrieved_contexts=record["retrieved_contexts"],
                )

            else:
                raise ValueError(f"Unknown metric: {metric_name}")

            return result.value, key_index

        except Exception as error:

            if not is_rate_limit_error(error):
                raise

            print(
                f"\nHTTP 429 on API key {key_index + 1}. "
                "Trying another key..."
            )

    raise RuntimeError(
        f"All {total_keys} API keys returned HTTP 429 "
        f"while evaluating {metric_name}. "
        "Check their quotas and try again later."
    )


# --------------------------------------------------
# 7. Checkpoint management
# --------------------------------------------------

def save_checkpoint(checkpoint):

    CHECKPOINT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = CHECKPOINT_PATH.with_suffix(".tmp")

    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(
            checkpoint,
            file,
            indent=4,
            ensure_ascii=False,
        )

    temporary_path.replace(CHECKPOINT_PATH)


def load_checkpoint(dataset):

    if CHECKPOINT_PATH.exists():

        with open(CHECKPOINT_PATH, "r", encoding="utf-8") as file:
            checkpoint = json.load(file)

        saved_results = checkpoint.get("individual_results", [])

        # Reuse checkpoint only when its dataset still matches.
        if (
            len(saved_results) == len(dataset)
            and all(
                saved_results[i].get("question") == dataset[i]["user_input"]
                for i in range(len(dataset))
            )
        ):
            print("Existing checkpoint found. Resuming evaluation.")

            return checkpoint

        print("Dataset changed. Starting a fresh evaluation.")

    return {
        "individual_results": [
            {
                "question": record["user_input"],
                "faithfulness": None,
                "answer_relevancy": None,
                "context_precision": None,
            }
            for record in dataset
        ]
    }


# --------------------------------------------------
# 8. Main evaluation workflow
# --------------------------------------------------

async def main():

    print("\nLoading RAGAS dataset...")

    dataset = load_dataset()

    print(f"Loaded {len(dataset)} records.")

    api_keys = load_api_keys()[:1]

    print("\nInitializing Gemini evaluators...")

    # One evaluator bundle per API key
    evaluators = [
        initialize_evaluator(key)
        for key in api_keys
    ]

    print(f"Evaluator model: {MODEL_NAME}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"Available API keys: {len(api_keys)}")

    checkpoint = load_checkpoint(dataset)

    results = checkpoint["individual_results"]

    current_key_index = 0

    print("\nStarting RAGAS evaluation...\n")

    for index, record in enumerate(dataset):

        saved_result = results[index]

        print(
            f"\nEvaluating question {index + 1}/{len(dataset)}..."
        )

        for metric_name in METRIC_NAMES:

            # Skip metrics already saved in checkpoint
            if saved_result[metric_name] is not None:

                print(
                    f"{metric_name}: already evaluated. Skipping."
                )
                continue

            score, current_key_index = await run_metric_with_rotation(
                metric_name=metric_name,
                record=record,
                evaluators=evaluators,
                start_index=current_key_index,
            )

            saved_result[metric_name] = score

            # Save immediately after every successful metric
            save_checkpoint(checkpoint)

            print(f"{metric_name}: {score:.4f}")

        print("-" * 45)

    # --------------------------------------------------
    # 9. Calculate average scores
    # --------------------------------------------------

    summary = {
        metric: mean(
            item[metric]
            for item in results
        )
        for metric in METRIC_NAMES
    }

    output = {
        "evaluator_model": MODEL_NAME,
        "embedding_model": EMBEDDING_MODEL,
        "total_questions": len(results),
        "individual_results": results,
        "average_scores": summary,
    }

    # --------------------------------------------------
    # 10. Save final results
    # --------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\n========== RAGAS EVALUATION SUMMARY ==========")

    for metric, score in summary.items():
        print(f"{metric}: {score:.4f}")

    print("\nResults saved to:")
    print(OUTPUT_PATH)

    print("\nCheckpoint saved to:")
    print(CHECKPOINT_PATH)


if __name__ == "__main__":
    asyncio.run(main())
