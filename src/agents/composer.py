from src.config import get_client, DEFAULT_MODEL

RESPONSE_COMPOSER_PROMPT = """You are a Response Composer Agent. Your role is to synthesize inputs from multiple specialist agents (Research Agent, Positive Analysis Agent, Flaw Finding Agent) and create a comprehensive, balanced, and well-structured final response.

You receive:
1. Research findings with historical context and evidence
2. Positive analysis highlighting strengths and opportunities
3. Critical analysis identifying flaws and risks

Your job is to:
- Integrate all perspectives into a cohesive narrative
- Present a balanced view that acknowledges both opportunities and challenges
- Structure the response clearly with sections for context, strengths, risks, and recommendations
- Ensure the final answer is actionable and insightful
- Maintain objectivity while being helpful

Format your response with clear sections and provide a final recommendation or conclusion.
CRITICAL: Keep the final synthesis under 200 words. Use bullet points for key takeaways."""

def run_composer_agent(user_input, research, positives, flaws):
    """Response Composer Agent - synthesizes all perspectives"""
    client = get_client()
    synthesis_prompt = f"""User Idea/Question: {user_input}

RESEARCH FINDINGS:
{research}

POSITIVE ANALYSIS:
{positives}

CRITICAL ANALYSIS (FLAWS/RISKS):
{flaws}

Synthesize all these perspectives into a comprehensive, balanced, and actionable response."""
    
    messages = [
        {"role": "system", "content": RESPONSE_COMPOSER_PROMPT},
        {"role": "user", "content": synthesis_prompt}
    ]
    response = client.chat.completions.create(
        messages=messages,
        model=DEFAULT_MODEL,
    )
    return response.choices[0].message.content
