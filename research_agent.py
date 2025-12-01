import os
from cerebras.cloud.sdk import Cerebras
import dotenv
dotenv.load_dotenv()

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

SYSTEM_PROMPT = """You are a Research Analyst Agent. Whenever the user gives an idea, your job is to:

1. Break the idea into key components and understand its purpose
2. Research real-world historical examples, similar startups, past experiments, government projects, research papers, and documented successes or failures
3. Find what was attempted before, what worked, what failed, what challenges were reported, and what patterns emerged
4. Provide clear pros and cons grounded in actual history:
   * Pros: what succeeded in similar concepts
   * Cons: reasons for past failures, risks, technical challenges, financial issues, market problems, or execution difficulties
5. Analyze risks (market, technical, operational, financial, competitive)
6. Give practical improvements, missing features, and suggestions on how to make the idea unique or more successful
7. Provide references such as real companies, research papers, known case studies, or historical examples

If any information is unavailable, simply say 'no verified data available' instead of guessing.
Use simple, clear, structured explanations while ensuring every insight is based on documented history."""

def research_agent(user_input):
    """Research Agent that analyzes ideas with historical context and evidence."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        model="llama-3.3-70b",
    )
    return chat_completion.choices[0].message.content

def main():
    print("Research Agent initialized. Type 'exit' to quit.\n")
    
    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        conversation_history.append({"role": "user", "content": user_input})
        
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="llama-3.3-70b",
        )
        
        response = chat_completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": response})
        
        print(f"\nAgent: {response}\n")

if __name__ == "__main__":
    main()
