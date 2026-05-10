"""
Streamlit Frontend for AutoFixAI - Multi-Agent Bug Resolution System

A minimal, clean UI to visualize the complete workflow:
- Issue Description
- Original Buggy Code
- Fix Plan (from Planner Agent)
- Fixed Code (from Code Writer Agent)
- Execution Statistics
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.state import AgentState
from app.graph.workflow import graph


def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="AutoFixAI - Bug Fixer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )


def render_header():
    """Display main header."""
    st.markdown("# 🤖 AutoFixAI - Multi-Agent Bug Fixer")
    st.markdown("*Fix bugs autonomously using LangGraph + Ollama*")
    st.divider()


def render_issue_input():
    """Render issue input section."""
    st.markdown("## 📋 Describe Your Issue")
    issue = st.text_area(
        "What bug needs fixing?",
        value="The calculate_average() function crashes when given an empty list, and the find_max() function doesn't handle edge cases properly.",
        height=100
    )
    return issue


def render_code_input():
    """Render code input section."""
    st.markdown("## 📂 Original Code")
    default_path = os.path.join(os.path.dirname(__file__), "..", "repo", "sample.py")
    
    if os.path.exists(default_path):
        with open(default_path, "r") as f:
            code = f.read()
        st.code(code, language="python")
        return code
    else:
        st.error("Could not find repo/sample.py")
        return None


def run_workflow(issue):
    """Execute the multi-agent workflow."""
    if not issue.strip():
        st.error("Please provide an issue description")
        return None
    
    with st.spinner("🚀 Running workflow... (1-2 minutes)"):
        try:
            initial_state: AgentState = {
                "issue": issue.strip(),
                "code_context": "",
                "plan": "",
                "patch": "",
            }
            final_state = graph.invoke(initial_state)
            return final_state
        except Exception as e:
            st.error(f"❌ Workflow Error: {str(e)}")
            st.info("Ensure Ollama is running: ollama serve")
            return None


def render_results(state):
    """Display workflow results in tabs."""
    if not state:
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Original", "🧠 Plan", "✅ Fixed", "📊 Stats"])
    
    with tab1:
        st.markdown("## 📖 Original Code")
        st.code(state["code_context"], language="python")
    
    with tab2:
        st.markdown("## 🧠 Fix Strategy")
        st.markdown(state["plan"])
    
    with tab3:
        st.markdown("## ✅ Fixed Code")
        st.code(state["patch"], language="python")
        st.download_button(
            "⬇️ Download Fixed Code",
            data=state["patch"],
            file_name="fixed_code.py",
            mime="text/plain"
        )
    
    with tab4:
        st.markdown("## 📊 Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original", f"{len(state['code_context'])} chars")
        with col2:
            st.metric("Plan", f"{len(state['plan'])} chars")
        with col3:
            st.metric("Fixed", f"{len(state['patch'])} chars")


def main():
    """Main Streamlit app."""
    setup_page()
    render_header()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        issue = render_issue_input()
        code = render_code_input()
    
    with col2:
        st.markdown("## 🚀 Workflow")
        if st.button("Fix My Code", type="primary", use_container_width=True):
            if code:
                state = run_workflow(issue)
                if state:
                    st.session_state.workflow_state = state
                    st.success("✅ Workflow completed!")
    
    st.divider()
    
    if "workflow_state" in st.session_state:
        render_results(st.session_state.workflow_state)
    else:
        st.info("👈 Click 'Fix My Code' to start the workflow")


if __name__ == "__main__":
    main()
