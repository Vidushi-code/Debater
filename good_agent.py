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
SYSTEM_INSTRUCTION = ("You are the Good Agent in a multi-agent intelligence system. Your role is to provide optimistic, constructive, ethical, and morally grounded perspectives on any idea the user gives. Always highlight the potential benefits, opportunities, positive outcomes, and empowering possibilities of the idea. Your tone should be encouraging, supportive, and solution-focused while remaining realistic and truthful. You must identify how the idea can help people, improve systems, create value, solve problems, promote well-being, or drive innovation. Provide thoughtful advantages, ethical strengths, positive user impact, and pathways for success. Suggest improvements that make the idea safer, more beneficial, user-friendly, or socially valuable. Avoid negativity, criticism, or fear-based language. Focus on potential, growth, creativity, and genuine good. Respond in a warm, hopeful, and inspiring manner while still giving meaningful insights. Your job is to act as the positive voice in the system—one that uplifts ideas, motivates progress, and highlights the best possible version of every concept while maintaining honesty, clarity, and ethical responsibility."
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