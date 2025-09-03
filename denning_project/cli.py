"""
The Command-Line Interface (CLI) for Project Denning.
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from agent_core.agent import Agent

def main():
    print("--Welcome to Project Denning: Evolving AI purely on law --")
    
    try:
        agent = Agent(config_path='config.yaml')
        print("Agent initialized successfully. Type 'exit' or 'quit' to end.")
    except Exception as e:
        print(f"\nFATAL ERROR: Could not initialize the Denning agent: {e}")
        print("Please ensure 'config.yaml' and your '.env' file are set up correctly.")
        return

    while True:
        user_input = input("\n[Denning] Ask your question > ")

        if user_input.lower() in ['exit', 'quit']:
            print("Exiting Project Denning. Goodbye.")
            break

        if user_input.lower() in ['status', 'state', 'what are you working on?']:
            print(f"Agent Status: {agent.get_status()}")
            continue
            
        print("Thinking...")
        answer = agent.handle_query(user_input)
        
        print("\n==================== Denning's Answer ====================")
        print(answer)
        print("==========================================================")

if __name__ == '__main__':
    main()
