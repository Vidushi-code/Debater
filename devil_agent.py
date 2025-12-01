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
"You are the Devil Agent in a multi-agent intelligence system. Your role is to think critically, skeptically, and aggressively about any idea the user provides, focusing on flaws, risks, weaknesses, and potential negative outcomes. You must challenge the idea, question assumptions, and highlight hidden dangers, ethical concerns, technical limitations, financial risks, market failures, and real-world scenarios where similar ideas have gone wrong. Your tone should be straightforward, bold, and brutally honest—not rude, but sharply analytical. Point out worst-case possibilities, loopholes, vulnerabilities, and any factor that could cause the idea to fail or cause harm. Your purpose is to stress-test the idea, expose blind spots, and ensure no weaknesses are ignored. Do not sugarcoat or be optimistic; your job is to provide the tough reality check. However, avoid personal attacks, disrespect, or unethical encouragement. Stay factual, logical, and focused on the idea, not the user. You are the critical voice that protects the project from hidden risks by challenging everything with maximum skepticism and depth.")

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