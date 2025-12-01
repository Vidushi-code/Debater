from src.config import get_client, DEFAULT_MODEL

SYSTEM_PROMPT = """You are a Conversational AI Agent designed to interact naturally, understand context, and give intelligent, emotionally aware, and logically structured responses. Your job is to maintain smooth, human-like conversations by understanding the user’s intent, tone, and emotions while providing accurate, helpful, and context-aware replies. You should remember previous parts of the conversation (within the session), ask clarifying questions when necessary, and adapt your response style based on the user’s mood—friendly when they are casual, professional when they need formal help, and supportive when they feel confused or stressed. Always avoid unnecessary complexity and communicate in clear, meaningful language. Provide examples, analogies, or step-by-step explanations when the user might not understand a concept. When the user shares ideas, problems, or tasks, respond like a thoughtful partner—sometimes guiding, sometimes challenging, sometimes suggesting better alternatives, and always helping them think deeper. Keep responses engaging, concise, empathetic, and context-aware. Above all, behave like a reliable conversational companion who listens carefully, thinks intelligently, and communicates with clarity, respect, and emotional intelligence."""

def check_if_ready(user_input, history):
    """Determines if the user has provided enough information for a full analysis."""
    
    # Hard heuristic: If input is very short, it's likely just a greeting or not enough context.
    if len(user_input.strip()) < 10:
        return False

    client = get_client()
    
    router_prompt = """You are an Intent Classifier. Your job is to determine if the user has provided a concrete idea, problem, or topic that is ready for deep analysis.

    CRITICAL RULES:
    - Return "NOT_READY" for greetings like "hi", "hello", "hey", "good morning".
    - Return "NOT_READY" for vague statements like "I have an idea", "help me", "start".
    - Return "NOT_READY" if the input is less than 5 words and doesn't contain a specific noun/topic.
    - ONLY return "READY" if the user has clearly described a specific concept, business idea, or topic (e.g., "flying car", "coffee delivery drone", "AI for lawyers").

    User Input: "{}"
    
    Response (READY or NOT_READY only):""".format(user_input)

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": router_prompt}],
        model=DEFAULT_MODEL,
    )
    result = response.choices[0].message.content.strip().upper()
    return "READY" in result

def run_chat_mode(user_input, history):
    """Standard conversational response when analysis is not yet needed."""
    client = get_client()
    
    # Add to history
    history.append({"role": "user", "content": user_input})
    
    chat_prompt = """You are a helpful AI Assistant. The user is chatting with you but hasn't provided a full idea for analysis yet.
    
    Your goal is to:
    1. Respond naturally to their greeting or question.
    2. Gently encourage them to share an idea, startup concept, or problem they want to analyze.
    3. Be brief and engaging.
    
    User Input: {}""".format(user_input)
    
    # We use a temporary history for this chat turn to avoid polluting the main context too much, 
    # or we can just append to main history. Let's append to main history for continuity.
    
    response = client.chat.completions.create(
        messages=history + [{"role": "system", "content": chat_prompt}], # Inject specific instruction for this turn
        model=DEFAULT_MODEL,
    )
    
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply

def run_conversational_agent(user_input, final_response, history):
    """Conversational Agent - manages the interaction and maintains context"""
    client = get_client()
    
    # Add to conversation history
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": final_response})
    
    # Generate conversational response
    context_prompt = f"""The user asked: "{user_input}"

Our multi-agent analysis produced this comprehensive response:
{final_response}

Deliver this information in a natural, conversational way that:
- Acknowledges their question with empathy
- Presents the information clearly and engagingly
- Maintains context from our conversation
- Offers to clarify or explore any aspect further

Be warm, helpful, and conversational while preserving all the analytical depth."""
    
    history.append({"role": "user", "content": context_prompt})
    
    conversational_response = client.chat.completions.create(
        messages=history,
        model=DEFAULT_MODEL,
    )
    
    final_conversational = conversational_response.choices[0].message.content
    history.append({"role": "assistant", "content": final_conversational})
    
    return final_conversational
