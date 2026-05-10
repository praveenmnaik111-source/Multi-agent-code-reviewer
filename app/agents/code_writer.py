"""
Code Writer Agent - Third step in the workflow.

Responsibility:
- Receive fix plan and original code context
- Generate corrected/fixed code using LLM
- Store corrected code in shared state
- Ensure code is syntactically valid

Workflow Position: Reader → Planner → [CODE WRITER] → END
"""

from app.state import AgentState
from app.llm import llm


def code_writer(state: AgentState) -> AgentState:
    """
    Generate corrected code based on the fix plan.
    
    Args:
        state: Shared workflow state with plan and code_context
        
    Returns:
        Updated state with patch populated
        
    Process:
        1. Combine plan + original code into generation prompt
        2. Use LLM to generate fixed code
        3. Extract and validate generated code
        4. Store in state["patch"]
        5. Log generated fix for visibility
    """
    
    print("\n" + "="*60)
    print("✍️  CODE WRITER AGENT STARTING")
    print("="*60)
    
    # Construct the code generation prompt for LLM
    generation_prompt = f"""You are an expert Python developer. Based on the fix plan provided, 
generate corrected Python code that addresses all issues.

ORIGINAL CODE:
```python
{state['code_context']}
```

FIX STRATEGY/PLAN:
{state['plan']}

Please generate the COMPLETE fixed code in a python code block. Include:
1. All necessary imports
2. Proper error handling
3. Type hints where appropriate
4. Docstrings for functions
5. Comments explaining fixes

Return ONLY the corrected Python code in a code block."""
    
    print("🔧 Generating fixed code from plan...")
    print(f"📋 Plan summary: {state['plan'][:100]}...")
    
    try:
        # Use LLM to generate corrected code
        response = llm.invoke(generation_prompt)
        generated_content = response.content if hasattr(response, 'content') else str(response)
        
        # Extract code from markdown code blocks if present
        if "```python" in generated_content:
            # Extract content between ```python and ```
            start_idx = generated_content.find("```python") + len("```python")
            end_idx = generated_content.find("```", start_idx)
            if end_idx != -1:
                patch = generated_content[start_idx:end_idx].strip()
            else:
                patch = generated_content[start_idx:].strip()
        elif "```" in generated_content:
            # Fallback for generic code blocks
            start_idx = generated_content.find("```") + len("```")
            end_idx = generated_content.find("```", start_idx)
            if end_idx != -1:
                patch = generated_content[start_idx:end_idx].strip()
            else:
                patch = generated_content[start_idx:].strip()
        else:
            # No code blocks found, use entire response
            patch = generated_content
        
        # Update state with generated patch
        state["patch"] = patch
        
        print("✅ Fixed code generated successfully")
        print(f"📊 Generated code length: {len(patch)} characters")
        print("="*60)
        print("GENERATED FIXED CODE:")
        print("-"*60)
        print(patch[:800] + "\n..." if len(patch) > 800 else patch)
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error generating code: {str(e)}")
        state["patch"] = f"Error: Could not generate fixed code - {str(e)}"
    
    return state
