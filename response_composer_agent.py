import os
from cerebras.cloud.sdk import Cerebras
import dotenv
dotenv.load_dotenv()

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

# Import specialist agents
from research_agent import SYSTEM_PROMPT as RESEARCH_PROMPT
from good_agent import SYSTEM_INSTRUCTION as OPTIMIST_PROMPT
from devil_agent import SYSTEM_INSTRUCTION as DEVILS_ADVOCATE_PROMPT
from conversational_agent import SYSTEM_PROMPT as CONVERSATIONAL_PROMPT

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

Format your response with clear sections and provide a final recommendation or conclusion."""


class MultiAgentSystem:
    def __init__(self):
        self.conversation_history = []
        self.session_context = {}
        # Initialize conversational agent history with system prompt
        self.conversational_history = [{"role": "system", "content": CONVERSATIONAL_PROMPT}]
    
    def research_agent(self, user_input):
        """Research Agent - provides historical context and evidence"""
        messages = [
            {"role": "system", "content": RESEARCH_PROMPT},
            {"role": "user", "content": user_input}
        ]
        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b",
        )
        return response.choices[0].message.content
    
    def positive_analysis_agent(self, user_input, research_context):
        """Positive Analysis Agent - highlights strengths and opportunities"""
        prompt = f"""Based on this idea and research context, provide a positive analysis:

Idea: {user_input}

Research Context: {research_context}

Focus on strengths, opportunities, and success potential."""
        
        messages = [
            {"role": "system", "content": OPTIMIST_PROMPT},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b",
        )
        return response.choices[0].message.content
    
    def flaw_finding_agent(self, user_input, research_context):
        """Flaw Finding Agent - identifies risks and challenges"""
        prompt = f"""Based on this idea and research context, provide critical analysis:

Idea: {user_input}

Research Context: {research_context}

Identify flaws, risks, challenges, and potential failures."""
        
        messages = [
            {"role": "system", "content": DEVILS_ADVOCATE_PROMPT},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b",
        )
        return response.choices[0].message.content
    
    def response_composer_agent(self, user_input, research, positives, flaws):
        """Response Composer Agent - synthesizes all perspectives"""
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
            model="llama-3.3-70b",
        )
        return response.choices[0].message.content
    
    def conversational_agent(self, user_input, final_response):
        """Conversational Agent - manages the interaction and maintains context"""
        # Store in session context
        self.session_context['last_query'] = user_input
        self.session_context['last_response'] = final_response
        
        # Add to conversation history
        self.conversation_history.append({
            "user": user_input,
            "response": final_response
        })
        
        # Process through conversational agent for natural, context-aware delivery
        self.conversational_history.append({"role": "user", "content": user_input})
        self.conversational_history.append({"role": "assistant", "content": final_response})
        
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
        
        self.conversational_history.append({"role": "user", "content": context_prompt})
        
        conversational_response = client.chat.completions.create(
            messages=self.conversational_history,
            model="llama-3.3-70b",
        )
        
        final_conversational = conversational_response.choices[0].message.content
        self.conversational_history.append({"role": "assistant", "content": final_conversational})
        
        return final_conversational
    
    def process_user_input(self, user_input):
        """Main workflow - orchestrates all agents"""
        print("\n🔍 Research Agent analyzing...")
        research = self.research_agent(user_input)
        
        print("👍 Positive Analysis Agent evaluating...")
        positives = self.positive_analysis_agent(user_input, research)
        
        print("⚠️  Flaw Finding Agent critiquing...")
        flaws = self.flaw_finding_agent(user_input, research)
        
        print("📝 Response Composer Agent synthesizing...")
        final_response = self.response_composer_agent(user_input, research, positives, flaws)
        
        print("💬 Conversational Agent delivering response...")
        # Pass through conversational agent for context management and natural delivery
        return self.conversational_agent(user_input, final_response)


def main():
    print("=" * 80)
    print("MULTI-AGENT ANALYSIS WORKFLOW")
    print("=" * 80)
    print("\nThis system analyzes your ideas through multiple perspectives:")
    print("  • Research Agent: Historical context & evidence")
    print("  • Positive Analysis: Strengths & opportunities")
    print("  • Flaw Finding: Risks & challenges")
    print("  • Response Composer: Balanced synthesis")
    print("  • Conversational Agent: Natural, context-aware delivery")
    print("\nType 'exit' to quit.\n")
    print("=" * 80)
    
    system = MultiAgentSystem()
    
    while True:
        user_input = input("\n💭 Your idea/question: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\n👋 Goodbye! Session ended.")
            break
        
        if not user_input:
            continue
        
        print("\n" + "=" * 80)
        final_response = system.process_user_input(user_input)
        print("\n" + "=" * 80)
        print("\n📊 FINAL ANALYSIS:\n")
        print(final_response)
        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
