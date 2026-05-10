"""
Main entry point for AutoFixAI - Multi-Agent Bug Resolution System.

This script:
1. Initializes the workflow graph
2. Sets up the initial problem (issue)
3. Invokes the multi-agent workflow
4. Displays the final generated fix

Execution Flow:
    Initialize State → Invoke Graph → Execute Agents → Display Results

The system automatically orchestrates:
    issue → code_reader → planner → code_writer → patch
"""

from app.state import AgentState
from app.graph.workflow import graph


def run_auto_fix():
    """
    Run the complete AutoFixAI multi-agent workflow.
    
    Process:
        1. Define the bug/issue to fix
        2. Create initial state
        3. Invoke the workflow graph
        4. Display results from each agent
    """
    
    print("\n" + "="*70)
    print(" "*15 + "🤖 AUTOFIXAI - MULTI-AGENT BUG RESOLUTION 🤖")
    print("="*70)
    print("\nStarting autonomous bug fixing workflow...")
    print("Powered by: LangGraph + Ollama (qwen2.5-coder:7b)\n")
    
    # Define the issue/bug to fix
    # This could come from user input, issue tracker, or bug report
    issue = """
The calculate_average() function crashes when given an empty list,
and the find_max() function doesn't handle edge cases properly.
Please fix these functions and add proper error handling and type hints.
"""
    
    print("="*70)
    print("📋 ISSUE DESCRIPTION:")
    print("="*70)
    print(issue)
    print("="*70 + "\n")
    
    # Initialize the state with the issue
    # Other fields will be populated by agents during execution
    initial_state: AgentState = {
        "issue": issue.strip(),
        "code_context": "",      # Will be filled by code_reader
        "plan": "",             # Will be filled by planner
        "patch": "",            # Will be filled by code_writer
    }
    
    print("🚀 INVOKING WORKFLOW...\n")
    
    try:
        # Execute the workflow with the initial state
        # The graph automatically orchestrates all agents in sequence
        final_state = graph.invoke(initial_state)
        
        # Display results
        print("\n" + "="*70)
        print(" "*20 + "✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
        # Show the final generated fix
        print("🎯 FINAL GENERATED FIX:")
        print("-"*70)
        print(final_state.get("patch", "No patch generated"))
        print("-"*70 + "\n")
        
        # Show summary statistics
        print("📊 EXECUTION SUMMARY:")
        print("-"*70)
        print(f"Original code length:     {len(final_state.get('code_context', ''))} chars")
        print(f"Fix plan length:          {len(final_state.get('plan', ''))} chars")
        print(f"Generated patch length:   {len(final_state.get('patch', ''))} chars")
        print("-"*70 + "\n")
        
        print("="*70)
        print("🎉 AutoFixAI workflow completed! Check the generated patch above.")
        print("="*70 + "\n")
        
        return final_state
        
    except Exception as e:
        print(f"\n❌ WORKFLOW ERROR:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Ensure Ollama is running: ollama serve")
        print("  2. Ensure model is pulled: ollama pull qwen2.5-coder:7b")
        print("  3. Check .env configuration")
        print("  4. Verify network connectivity to localhost:11434\n")
        raise


if __name__ == "__main__":
    """
    Entry point for the AutoFixAI system.
    
    Prerequisites:
        1. Ollama running locally (ollama serve)
        2. Model downloaded (ollama pull qwen2.5-coder:7b)
        3. Dependencies installed (pip install -r requirements.txt)
        4. .env file configured
    """
    run_auto_fix()
