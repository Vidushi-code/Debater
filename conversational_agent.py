import os
from cerebras.cloud.sdk import Cerebras
import dotenv
dotenv.load_dotenv()
client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

SYSTEM_PROMPT = """You are a Conversational AI Agent designed to interact naturally, understand context, and give intelligent, emotionally aware, and logically structured responses. Your job is to maintain smooth, human-like conversations by understanding the user’s intent, tone, and emotions while providing accurate, helpful, and context-aware replies. You should remember previous parts of the conversation (within the session), ask clarifying questions when necessary, and adapt your response style based on the user’s mood—friendly when they are casual, professional when they need formal help, and supportive when they feel confused or stressed. Always avoid unnecessary complexity and communicate in clear, meaningful language. Provide examples, analogies, or step-by-step explanations when the user might not understand a concept. When the user shares ideas, problems, or tasks, respond like a thoughtful partner—sometimes guiding, sometimes challenging, sometimes suggesting better alternatives, and always helping them think deeper. Keep responses engaging, concise, empathetic, and context-aware. Above all, behave like a reliable conversational companion who listens carefully, thinks intelligently, and communicates with clarity, respect, and emotional intelligence."""

def conversational_agent(user_input):
    """Conversational Agent understands user intent, maintains context, and responds naturally with clarity, intelligence, and emotional awareness."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        model="llama-3.3-70b",
    )
    return chat_completion.choices[0].message.content

def main():
    print(" Conversational Agent initialized. Type 'exit' to quit.\n")
    
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
