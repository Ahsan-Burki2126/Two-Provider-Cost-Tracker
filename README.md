## Setup

1. Run `uv sync` to install the required Python packages.

2. Copy `.env.example` and rename the copy to `.env`.

3. Open `.env` and provide values for `GEMINI_API_KEY`, `GROQ_API_KEY`, `GEMINI_MODEL`, and `GROQ_MODEL`.

4. Keep `.env` private because it contains secret API keys. Never commit it to GitHub.

## Run

Run the tracker from the repository root and provide your prompt inside quotation marks.

`uv run tracker.py "What is machine learning, answer briefly"`

## Sample Output

The generated replies appear first, followed by a comparison table.

| Provider | Input Tokens | Output Tokens | Seconds |     Cost USD |
| -------- | -----------: | ------------: | ------: | -----------: |
| gemini   |            8 |            49 |   7.073 | 0.0000755000 |
| groq     |           78 |           161 |   0.877 | 0.0000541500 |

The exact replies, token counts, response times, and costs may differ between runs.

## What I Learned

I learned how APIs allow a Python program to communicate with different LLM providers. I also learned how to protect API keys, read real token usage, measure response time, and calculate the estimated cost of each model call. This assignment showed me that different providers can use different numbers of tokens and have different speeds and costs for the same prompt.
