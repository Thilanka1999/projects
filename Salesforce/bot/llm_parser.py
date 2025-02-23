import json
import os
import groq


groq_api_key = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=groq_api_key)


def extract_function_using_llm(message):
    """Uses Groq LLM to extract function and arguments from the message."""
    prompt = (
        f"Extract the function name and arguments from the following message:\n\n"
        f'Message: "{message}"\n\n'
        f"Instructions:\n"
        f"- Identify the operation (e.g., add, subtract, multiply, divide).\n"
        f"- Extract numbers in the order they appear.\n"
        f"- Output **only** a JSON object without any explanations.\n"
        f'- **Correct Format:** {{"function": "function_name", "args": [arg1, arg2]}}\n\n'
        f"Example:\n"
        f"- Input: 'add 2 and 3'\n"
        f'- Output: {{"function": "add", "args": [2, 3]}}\n\n'
        f"Now, extract and return the JSON object for the given message."
    )

    response = client.chat.completions.create(
        model="llama-3.2-3b-preview",  # llm model
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that extracts function calls from messages. "
                "Output only a valid JSON object with 'function' and 'args' keys. No extra text.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    try:
        data = json.loads(response.choices[0].message.content.strip())
        return data["function"], data["args"]
    except Exception as e:
        return None, None
