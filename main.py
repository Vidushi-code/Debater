from src.orchestrator import MultiAgentSystem

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
        try:
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
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Session ended.")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
