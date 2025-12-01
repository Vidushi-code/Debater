import os
from cerebras.cloud.sdk import Cerebras

# Use environment variable instead of a literal key
API_KEY = os.environ.get("CEREBRAS_API_KEY")
if not API_KEY:
    raise EnvironmentError(
        "CEREBRAS_API_KEY not set. In PowerShell: $env:CEREBRAS_API_KEY = 'your_key_here'"
    )

client = Cerebras(api_key=API_KEY)

# System instruction sets the Devil's Advocate persona
SYSTEM_INSTRUCTION = (
    "You are a Devil's Advocate Agent. Rigorously challenge every assumption, "
    "identify logical flaws, raise objections, and propose counterarguments. "
    "Ask clarifying questions when points are ambiguous. Be analytical, evidence-based, and respectful. "
    "If the user requests harmful, illegal, or hateful content, refuse and offer safer alternatives."
)

def devils_advocate_reply(user_input, model="llama-3.3-70b", max_tokens=512, temperature=0.9):
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": user_input},
    ]
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    # Try to extract the textual assistant reply; fallback to repr if structure differs
    try:
        assistant_text = response.choices[0].message.content
    except Exception:
        assistant_text = str(response)
    return assistant_text

if __name__ == "__main__":
    print("Devil's Advocate Agent (type 'exit' to quit)")
    while True:
        user_input = input("\nYour statement / idea: ").strip()
        if not user_input or user_input.lower() in ("exit", "quit"):
            break
        reply = devils_advocate_reply(user_input)
        print("\nDevil's Advocate response:\n", reply)