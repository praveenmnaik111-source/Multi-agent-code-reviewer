"""
Planner Agent - Second step in the workflow.

Responsibility:
- Receive issue description and source code context
- Analyze the problem using LLM
- Generate a fix strategy/plan
- Store plan in shared state for writer agent

Workflow Position: Reader → [PLANNER] → Writer
"""

from app.state import AgentState
from app.llm import llm


def planner(state: AgentState) -> AgentState:
    """
    Analyze the issue and generate a fix plan.
    
    Args:
        state: Shared workflow state with issue and code_context
        
    Returns:
        Updated state with plan populated
        
    Process:
        1. Combine issue + code into analysis prompt
        2. Use LLM to generate fix strategy
        3. Store plan in state["plan"]
        4. Log plan for visibility
    """
    
    print("\n" + "="*60)
    print("🧠 PLANNER AGENT STARTING")
    print("="*60)
    
    # Construct the analysis prompt for LLM
    analysis_prompt = f"""You are an expert code reviewer. Analyze the following code and issue.

ISSUE/BUG REPORT:
{state['issue']}

CURRENT CODE:
```python
{state['code_context']}
```

Please analyze this code and provide a detailed fix strategy:
1. Identify the root cause
2. Explain the fix approach
3. List specific changes needed
4. Consider edge cases

Provide a clear, step-by-step plan."""
    
    print("📝 Analyzing issue and code...")
    print(f"📌 Issue: {state['issue'][:80]}...")
    
    try:
        # Use LLM to generate fix plan
        response = llm.invoke(analysis_prompt)
        plan = response.content if hasattr(response, 'content') else str(response)
        
        # Update state with the generated plan
        state["plan"] = plan
        
        print("✅ Plan generated successfully")
        print(f"📊 Plan length: {len(plan)} characters")
        print("="*60)
        print("GENERATED PLAN:")
        print("-"*60)
        print(plan[:500] + "..." if len(plan) > 500 else plan)
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error generating plan: {str(e)}")
        state["plan"] = f"Error: Could not generate plan - {str(e)}"
    
    return state
