"""
Code Reader Agent - First step in the workflow.

Responsibility:
- Read source code from repo/sample.py
- Store code in shared state for planner and writer agents
- Log reading action for transparency

Workflow Position: START → [CODE READER] → Planner → Writer
"""

import os
from app.state import AgentState


def code_reader(state: AgentState) -> AgentState:
    """
    Read source code from the repository.
    
    Args:
        state: Shared workflow state containing user's issue
        
    Returns:
        Updated state with code_context populated
        
    Process:
        1. Locate the sample.py file in repo/
        2. Read entire file contents
        3. Store in state["code_context"]
        4. Log action for visibility
    """
    
    # Construct file path to the sample code
    repo_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "repo",
        "sample.py"
    )
    
    print("\n" + "="*60)
    print("🔍 CODE READER AGENT STARTING")
    print("="*60)
    print(f"📂 Reading from: {repo_path}")
    
    try:
        # Read the source code
        with open(repo_path, "r") as f:
            code_content = f.read()
        
        # Update state with code context
        state["code_context"] = code_content
        
        print(f"✅ Successfully read {len(code_content)} characters of code")
        print(f"📋 Issue to address: {state['issue'][:100]}...")
        print("="*60 + "\n")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find file at {repo_path}")
        state["code_context"] = ""
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        state["code_context"] = ""
    
    return state
