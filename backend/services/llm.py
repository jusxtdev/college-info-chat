import json
import os
import time
from pathlib import Path

# from groq import Groq
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to backend/.env")

# using groq
# client = Groq(api_key=api_key)


client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"
RETRYABLE_CODES = (429, 503)

def call_gemini_with_retry(prompt: str, max_retries: int = 3, config: types.GenerateContentConfig | None = None):
    delay = 2
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=config
            )
        except errors.APIError as e:
            # 503 Service Unavailable or 429 Too Many Requests
            if getattr(e, "code", None) in RETRYABLE_CODES and attempt < max_retries - 1:
                print(f"High demand detected. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise


def process_chat_request(query: str) -> str:
    # read the college data from the JSON file
    data_path = Path(__file__).resolve().parents[1] / "data" / "info.json"
    # data_path = Path(__file__).resolve().parents[1] / "data" / "gecg_data.json"
    with open(data_path, "r") as f:
        college_data = json.load(f)
    college_data_string = json.dumps(college_data, indent=2)

    # system prompt
    system_prompt = f"""
    You are a college information assistant.

    Answer questions using ONLY the college data below.

    Rules:
    - Do not make up information.
    - If information is missing or null, say it is unavailable.
    - Answer naturally and concisely.
    - Do not mention the JSON or internal implementation.

    College data:
    {college_data_string}
    """

    # message passed to the LLM model
    response = call_gemini_with_retry(
        query,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    
    # resp = client.chat.completions.create(
    #     model="qwen/qwen3.8-27b",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": query}
    #     ],
    # )
    # response = resp.choices[0].message.content

    # send request to the LLM model and get the response
    return f"Response: {response.text}"