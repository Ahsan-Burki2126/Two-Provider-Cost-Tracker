import json
import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from groq import Groq


# Gemini 3.1 Flash Lite paid prices per one million tokens.
# Source, https://aistudio.google.com/docs/pricing#gemini-3.1-flash-lite
GEMINI_INPUT_PRICE_PER_M = 0.25
GEMINI_OUTPUT_PRICE_PER_M = 1.50

# Groq GPT OSS 20B paid prices per one million tokens.
# Source, https://console.groq.com/docs/model/openai/gpt-oss-20b
GROQ_INPUT_PRICE_PER_M = 0.075
GROQ_OUTPUT_PRICE_PER_M = 0.30


def calculate_cost(
    input_tokens,
    output_tokens,
    input_price_per_m,
    output_price_per_m,
):
    input_cost = input_tokens * input_price_per_m / 1_000_000
    output_cost = output_tokens * output_price_per_m / 1_000_000

    return input_cost + output_cost


def call_gemini(prompt, api_key, model):
    client = genai.Client(api_key=api_key)

    start_time = time.perf_counter()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    elapsed_time = time.perf_counter() - start_time

    reply = response.text
    input_tokens = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count

    return reply, input_tokens, output_tokens, elapsed_time


def call_groq(prompt, api_key, model):
    client = Groq(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    elapsed_time = time.perf_counter() - start_time

    reply = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    return reply, input_tokens, output_tokens, elapsed_time


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL")
groq_model = os.getenv("GROQ_MODEL")


if not gemini_api_key:
    print("Gemini API key is missing.")
    sys.exit(1)

if not groq_api_key:
    print("Groq API key is missing.")
    sys.exit(1)

if not gemini_model:
    print("Gemini model name is missing.")
    sys.exit(1)

if not groq_model:
    print("Groq model name is missing.")
    sys.exit(1)


if len(sys.argv) < 2:
    print('Usage, uv run tracker.py "your prompt"')
    sys.exit(1)

prompt = " ".join(sys.argv[1:]).strip()

if not prompt:
    print("The prompt cannot be empty.")
    sys.exit(1)


gemini_reply, gemini_input_tokens, gemini_output_tokens, gemini_seconds = (
    call_gemini(
        prompt,
        gemini_api_key,
        gemini_model,
    )
)

groq_reply, groq_input_tokens, groq_output_tokens, groq_seconds = call_groq(
    prompt,
    groq_api_key,
    groq_model,
)


gemini_cost = calculate_cost(
    gemini_input_tokens,
    gemini_output_tokens,
    GEMINI_INPUT_PRICE_PER_M,
    GEMINI_OUTPUT_PRICE_PER_M,
)

groq_cost = calculate_cost(
    groq_input_tokens,
    groq_output_tokens,
    GROQ_INPUT_PRICE_PER_M,
    GROQ_OUTPUT_PRICE_PER_M,
)


results = [
    {
        "provider": "gemini",
        "model": gemini_model,
        "reply": gemini_reply,
        "input_tokens": gemini_input_tokens,
        "output_tokens": gemini_output_tokens,
        "input_price_per_m": GEMINI_INPUT_PRICE_PER_M,
        "output_price_per_m": GEMINI_OUTPUT_PRICE_PER_M,
        "cost_usd": gemini_cost,
    },
    {
        "provider": "groq",
        "model": groq_model,
        "reply": groq_reply,
        "input_tokens": groq_input_tokens,
        "output_tokens": groq_output_tokens,
        "input_price_per_m": GROQ_INPUT_PRICE_PER_M,
        "output_price_per_m": GROQ_OUTPUT_PRICE_PER_M,
        "cost_usd": groq_cost,
    },
]


with open("results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2, ensure_ascii=False)


print("\nGEMINI REPLY\n")
print(gemini_reply)

print("\nGROQ REPLY\n")
print(groq_reply)


print()
print(
    f"{'Provider':<10}"
    f"{'Input Tokens':>15}"
    f"{'Output Tokens':>16}"
    f"{'Seconds':>12}"
    f"{'Cost USD':>16}"
)

print("-" * 69)

print(
    f"{'gemini':<10}"
    f"{gemini_input_tokens:>15}"
    f"{gemini_output_tokens:>16}"
    f"{gemini_seconds:>12.3f}"
    f"{gemini_cost:>16.10f}"
)

print(
    f"{'groq':<10}"
    f"{groq_input_tokens:>15}"
    f"{groq_output_tokens:>16}"
    f"{groq_seconds:>12.3f}"
    f"{groq_cost:>16.10f}"
)

print("Saved results to results.json")