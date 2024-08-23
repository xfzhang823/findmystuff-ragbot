# FindMyStuff RAG Bot

This project is a Retrieval-Augmented Generation (RAG) bot that allows users to search and retrieve information from documents stored on their PC via a chatbot interface. The bot uses the LlamaIndex framework, OpenAI's GPT-4 model, and Streamlit for the front-end.

## Features

- **Document Retrieval**: Load documents from a specified directory and create a vectorstore index for efficient search.
- **Conversational Interface**: Chat with the bot to retrieve information from your documents in a natural, context-aware manner.
- **Safeword Feature**: Easily exit the chat session using a safeword.

## Requirements

- Python 3.7 or higher
- Virtual environment (recommended)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/findmystuff-ragbot.git
    cd findmystuff-ragbot
    ```

2. **Create and activate a virtual environment:**
    - On Windows:
        ```bash
        python -m venv env
        .\env\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        python3 -m venv env
        source env/bin/activate
        ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a `.env` file in the root directory of the project.
    - Add your OpenAI API key:
        ```
        OPENAI_API_KEY=your_openai_api_key_here
        ```

## Usage

1. **Prepare your document data:**
   - Place your text documents in the `data/your document file data folder` directory (replace my sample data with your data folder)

2. **Run the bot:**
    ```bash
    streamlit run find_my_stuff_3rd_grader_ragbot.py
    ```

3. **Interact with the bot:**
   - Ask questions about the content in your documents.
   - Use the safeword `quit` to exit the chat session.

## Directory Structure

