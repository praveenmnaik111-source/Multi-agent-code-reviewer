"""
LangGraph Workflow Orchestration - Core of the multi-agent system.

Defines the computational graph that:
- Connects the three agents in sequence
- Manages state flow between agents
- Ensures proper execution order
- Compiles into a runnable workflow

Workflow Graph:
    ┌─────────┐
    │ READER  │
    └────┬────┘
         │ (code_context)
         ▼
    ┌─────────┐
    │ PLANNER │
    └────┬────┘
         │ (plan)
         ▼
    ┌─────────┐
    │ WRITER  │
    └────┬────┘
         │ (patch)
         ▼
      (final)
"""

from langgraph.graph import StateGraph
from app.state import AgentState
from app.agents.code_reader import code_reader
from app.agents.planner import planner
from app.agents.code_writer import code_writer


def create_workflow():
    """
    Create and compile the multi-agent workflow graph.
    
    Returns:
        Compiled workflow ready for invocation
        
    Graph Structure:
        1. code_reader node: Reads source code
        2. planner node: Analyzes and plans fix
        3. code_writer node: Generates fixed code
        
    Edges:
        reader → planner → writer → end
    """
    
    # Initialize the state graph with AgentState schema
    workflow = StateGraph(AgentState)
    
    # Add three nodes for each agent
    print("📐 Building workflow graph...")
    
    # Node 1: Code Reader
    workflow.add_node("reader", code_reader)
    print("  ✓ Added 'reader' node")
    
    # Node 2: Planner
    workflow.add_node("planner", planner)
    print("  ✓ Added 'planner' node")
    
    # Node 3: Code Writer
    workflow.add_node("writer", code_writer)
    print("  ✓ Added 'writer' node")
    
    # Define edges (connections between nodes)
    print("🔗 Connecting nodes...")
    
    # Start from reader
    workflow.set_entry_point("reader")
    print("  ✓ Set entry point to 'reader'")
    
    # Reader → Planner
    workflow.add_edge("reader", "planner")
    print("  ✓ Connected reader → planner")
    
    # Planner → Writer
    workflow.add_edge("planner", "writer")
    print("  ✓ Connected planner → writer")
    
    # Writer → End
    workflow.set_finish_point("writer")
    print("  ✓ Set finish point at 'writer'")
    
    # Compile the graph into a runnable workflow
    print("\n🔨 Compiling workflow...")
    compiled_workflow = workflow.compile()
    print("✅ Workflow compiled successfully!\n")
    
    return compiled_workflow


# Create and store compiled workflow at module load
graph = create_workflow()
