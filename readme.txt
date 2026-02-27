    ### Step 1: Install Python

    You'll need **Python 3.10 or higher** to run LangChain v1 applications.

    #### Check if Python is installed

    ```bash
    python --version
    # or
    python3 --version
    ```

    If you see Python 3.10 or higher, you're good! Skip to [Step 2](#step-2-clone-the-repository). If not:

    #### Install Python

    1. Visit [python.org](https://www.python.org/downloads/)
    2. Download Python 3.10+ for your operating system
    3. Follow the installation instructions (make sure to check "Add Python to PATH" on Windows)
    4. Verify installation:

    ```bash
    python --version  # Should show 3.10 or higher
    pip --version     # Should show pip version
    ```

    ---

    ### Step 2: Clone the Repository

    ```bash
    # Clone the course repository
    git clone https://github.com/massimotisi/applied-llms-labs-2025-2026

    # Navigate to the project
    cd applied-llms-labs-2025-2026

    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Mac/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt
    ```

    This will install all required packages including:

    - `langchain-openai` - OpenAI-compatible model integration
    - `langchain-core` - Core LangChain functionality
    - `langchain` - Main LangChain package with additional utilities
    - `langchain-azure-ai` - Azure specific langchain integrations
    - `python-dotenv` - Environment variable management for API keys

    ---

