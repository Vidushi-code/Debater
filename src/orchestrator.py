from src.agents.research import run_research_agent
from src.agents.optimist import run_optimist_agent
from src.agents.devil import run_devil_agent
from src.agents.composer import run_composer_agent
from src.agents.conversational import run_conversational_agent, SYSTEM_PROMPT as CONVERSATIONAL_PROMPT
from concurrent.futures import ThreadPoolExecutor

class MultiAgentSystem:
    def __init__(self):
        self.conversation_history = []
        self.session_context = {}
        # Initialize conversational agent history with system prompt
        self.conversational_history = [{"role": "system", "content": CONVERSATIONAL_PROMPT}]
    
    def process_user_input(self, user_input):
        """Main workflow - orchestrates all agents"""
        
        # 0. Check Intent
        from src.agents.conversational import check_if_ready, run_chat_mode
        
        if not check_if_ready(user_input, self.conversational_history):
            print("💬 Conversational Agent chatting...")
            return run_chat_mode(user_input, self.conversational_history)

        # 1. Research (Sequential)
        print("\n🔍 Research Agent analyzing...")
        research = run_research_agent(user_input)
        
        # 2. Parallel Execution (Optimist & Devil)
        print("\n⚡ Running Parallel Analysis (Optimist & Devil)...")
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_optimist = executor.submit(run_optimist_agent, user_input, research)
            future_devil = executor.submit(run_devil_agent, user_input, research)
            
            print("👍 Positive Analysis Agent evaluating...")
            print("⚠️  Flaw Finding Agent critiquing...")
            
            positives = future_optimist.result()
            flaws = future_devil.result()
        
        # 3. Synthesis (Sequential)
        print("\n📝 Response Composer Agent synthesizing...")
        final_response = run_composer_agent(user_input, research, positives, flaws)
        
        # 4. Store in Session Context
        self.session_context = {
            "user_input": user_input,
            "research": research,
            "positives": positives,
            "flaws": flaws,
            "final_response": final_response
        }
        
        # 5. Conversational Delivery
        print("💬 Conversational Agent delivering response...")
        return run_conversational_agent(user_input, final_response, self.conversational_history)
