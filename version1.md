# Version 1: Code Reviewer Automation Tool

## Overview
This is the initial version (v1) of an automated code review tool built with Python. The system uses a multi-agent architecture to analyze and potentially fix code issues in a sample repository.

## Architecture
The application is structured into several key components:

### Core Components
- **app/**: Main application logic
  - **agents/**: Specialized AI agents for different tasks
    - `code_reader.py`: Reads source code from the repository
    - `code_writer.py`: Handles code modifications (assumed based on structure)
    - `planner.py`: Plans the review process (assumed based on structure)
  - **graph/**: Workflow orchestration
    - `workflow.py`: Defines the agent interaction flow
  - `llm.py`: Likely integrates with a large language model for AI capabilities
  - `state.py`: Manages shared state across agents

- **frontend/**: User interface
  - `streamlit_app.py`: Web app built with Streamlit for user interaction
  - `requirements.txt`: Frontend dependencies

- **repo/**: Sample code repository for review
  - `sample.py`: Example code to be analyzed

### Workflow
The system follows a sequential workflow:
1. **Code Reader Agent**: Reads code from `repo/sample.py` and stores it in shared state
2. **Planner Agent**: Analyzes the code and plans fixes (based on user issues)
3. **Writer Agent**: Applies code changes
4. **Graph Workflow**: Orchestrates the agent interactions

### Technologies Used
- **Python**: Core language
- **Streamlit**: For the web frontend
- **Agent-based Architecture**: Multi-agent system for modular code review
- **State Management**: Shared state for agent communication

### Key Features (v1)
- Automated code reading from a sample repository
- Agent-based workflow for code analysis
- Web interface for user interaction
- Extensible architecture for adding more agents

### Limitations
- Currently works with a single sample file (`repo/sample.py`)
- Basic error handling in agents
- No advanced AI model integration visible in current code
- Manual setup required for dependencies

### Future Enhancements
- Support for multiple files/repositories
- Integration with Git for version control
- Advanced LLM capabilities for better code analysis
- Testing framework integration
- CI/CD pipeline support

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the main app: `python run.py`
3. Access the frontend: Run `streamlit run frontend/streamlit_app.py`

## Dependencies
See `requirements.txt` for Python packages used.