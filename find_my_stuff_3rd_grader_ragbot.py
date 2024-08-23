"""
This module is a RAG (retrieval augmented generation) that allows users 
to search and retrieve information from documents stored on their PC via a chatbot.
It uses Llama_index as framework, OpenAI API as LLM, and Streamline for front-end.

The chatbot uses OpenAI's GPT-4 model to provide accurate and context-aware 
responses based on the content of the documents.

The main functionalities include:
- Loading OpenAI API settings and initializing the language model (LLM) 
and embedding model.
- Checking if a pre-existing vectorstore index is available; 
if not, creating a new index from the documents.
- Setting up a chat engine using LlamaIndex that supports conversational interactions 
with context memory.
- Configuring a Streamlit interface for user interaction, 
including a chat input and message display area.
- Implementing a "safeword" feature to allow users to exit the chat session.

Modules and Functions:
- is_directory_empty: Checks if a given directory is empty.
- load_or_create_index: Loads an existing vectorstore index 
or creates a new one from documents.
- chat_with_bot: Handles the interaction with the chat engine 
to get responses based on user input.
"""

# Dependencies
import os
import sys
import logging
from dotenv import load_dotenv
import openai
import streamlit as st
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from utils.get_file_names import get_file_names
from utils.language_detector import LanguageDetector

# Ensure UTF-8 encoding throughout, logging
os.environ["PYTHONIOENCODING"] = "utf-8"
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Load OpenAI API key and LLM settings
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI("gpt-4", temperature=0.1)
embed_model = OpenAIEmbedding(
    embed_model="text-embedding-ada-002"
)  # Removed max_length
Settings.llm = llm
Settings.embed_model = embed_model


def is_directory_empty(dir_path):
    """
    Check if the given directory is empty.

    Args:
        dir_path (str): Path to the directory.

    Returns:
        bool: True if the directory is empty, False otherwise.
    """
    return len(os.listdir(dir_path)) == 0


def load_or_create_index():
    """
    Load the vectorstore index from disk if it exists, otherwise create a new one from documents.

    Returns:
        VectorStoreIndex: The loaded or newly created vectorstore index.
    """
    if is_directory_empty(PERSIST_DIR):
        txt_files = get_file_names(DOC_DIR, full_path=True, file_types=".txt")
        en_txt_files = [
            file
            for file in txt_files
            if LanguageDetector.detect_primary_language_from_file(file) == "en"
        ]
        documents = SimpleDirectoryReader(
            DOC_DIR, encoding="utf-8", filename_as_id=True
        ).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist(PERSIST_DIR)
        return index
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        return load_index_from_storage(storage_context)


def chat_with_bot(user_input):
    """
    Get a response from the chat engine based on user input.

    Args:
        user_input (str): The user's input.

    Returns:
        str: The chat engine's response.
    """
    response = chat_engine.chat(user_input)
    return response.response


# Directories for persisted vectorstore and documents
PERSIST_DIR = os.path.join(os.getcwd(), "vectorstore")
DOC_DIR = os.path.join(os.getcwd(), "data/yearbook text data")


# Load or create the vectorstore index
index = load_or_create_index()

# Initialize chat engine
memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    llm=llm,
    context_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk about "
        "the economic indicators in these documents."
        "Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
    ),  # customize the role depending on the type of documents you are trying to search
    verbose=False,
)

# Set up Streamlit app
st.set_page_config(
    page_title="FindMyStuff, a RAG bot powered by LlamaIndex",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title(
    "FindMyStuff, a RAG bot to search content on your PC - powered by LlamaIndex 💬🦙"
)
st.info('To exit the chat session, the safe word is "quit".')

SAFE_WORD = "quit"

# Initialize chat messages history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about content on documents in your PC!",
        }
    ]

if "quit" not in st.session_state:
    st.session_state.quit = False

# Chat functionality
if st.session_state.quit:
    st.write("Chat session ended. Refresh the page to start a new session.")
else:
    if prompt := st.chat_input("Your question"):
        if prompt.lower() == SAFE_WORD:
            st.session_state.quit = True
            st.write("Chat session ended. Refresh the page to start a new session.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = chat_with_bot(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
