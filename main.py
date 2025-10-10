"""
Minimal Multi-Agent System with Pydantic AI
The orchestrator is itself an LLM agent that decides which agents to call
"""
import asyncio
from orchestrator import orchestrate, OrchestratorContext
from moderator import moderate
from memory_updater import update_memory


async def main():
    """Simple async chat interface with stateful context"""
    print("=" * 70)
    print("DYNATRACE MULTI-AGENT SYSTEM")
    print("=" * 70)
    print("🧠 Intelligent Orchestrator with Specialist Agents")
    print("Agents: Problem Finder | Vulnerability | Root Cause | Mitigation")
    print("=" * 70)
    print("The orchestrator will decide which agents to call based on your query")
    print("Type 'exit' to quit")
    print("=" * 70)
    
    # Maintain context across conversation
    context = OrchestratorContext()
    

    while True:
        user_input = input("\n💬 You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("\n👋 Goodbye!")
            break
            
        if not user_input:
            continue
        
        print("\n🤖 Orchestrator is analyzing your request...\n")
        
        # Moderator (pass-through)
        moderated = moderate(user_input)
        
        # Orchestrator agent decides what to do (async)
        response = await orchestrate(moderated, context)

        context+=respone
        
        # Memory updater (pass-through)
        update_memory(user_input, response)
        
        print(response)


if __name__ == "__main__":
    asyncio.run(main())