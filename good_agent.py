# ...existing code...
import os
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
import dotenv
print("dotenv loaded successfully!")


# Load .env if present
load_dotenv()

# Use environment variable instead of a literal key
API_KEY = os.environ.get("CEREBRAS_API_KEY")
if not API_KEY:
    raise EnvironmentError(
        "CEREBRAS_API_KEY not set. In PowerShell: $env:CEREBRAS_API_KEY = 'your_key_here'"
    )

client = Cerebras(api_key=API_KEY)

# System instruction sets the Optimist persona (Good Agent)
SYSTEM_INSTRUCTION = (
    "You are an Optimist Agent. Your role is to highlight strengths, opportunities, and best-case scenarios — "
    "act as a confident, forward-thinking Optimist who believes success is achievable. "
    "Focus on constructive, actionable guidance, and reinforce confidence while remaining realistic and helpful. "
    "If the user requests harmful, illegal, or hateful content, refuse and offer safer alternatives."
)

def optimist_agent_reply(user_input, model="llama-3.3-70b", max_tokens=512, temperature=0.6):
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": user_input},
    ]
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=1,
        stream=False
    )
    # Extract textual assistant reply
    try:
        assistant_text = response.choices[0].message.content
    except Exception:
        assistant_text = str(response)
    return assistant_text

if __name__ == "__main__":
    print("Good Agent (Optimist) — highlights strengths and opportunities. (type 'exit' to quit)")
    while True:
        user_input = input("\nShare a plan/idea: ").strip()
        if not user_input or user_input.lower() in ("exit", "quit"):
            break
        reply = optimist_agent_reply(user_input)
        print("\nOptimist response:\n", reply)
# ...existing code...