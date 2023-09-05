import os
import random
import streamlit as st

#decorator
def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):

        # to clear chat history after swtching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

API_KEY_FILE = "openai_api_key.txt"

def read_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_api_key(api_key):
    with open(API_KEY_FILE, "w") as f:
        f.write(api_key)

def delete_api_key():
    if os.path.exists(API_KEY_FILE):
        os.remove(API_KEY_FILE)


def configure_openai_api_key():
    openai_api_key = read_api_key()
    api_key_input = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        value=openai_api_key,
        placeholder="sk-..."
    )

    if openai_api_key:
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key
        if st.sidebar.button("Delete API Key"):
            delete_api_key()
            os.environ.pop("OPENAI_API_KEY", None)
            openai_api_key = ""
            st.experimental_rerun()
    else:
        st.error("Please add your OpenAI API key to continue.")
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
        if st.sidebar.button("Save API Key"):
            os.environ["OPENAI_API_KEY"] = api_key_input
            st.session_state['OPENAI_API_KEY'] = api_key_input
            save_api_key(api_key_input)
            openai_api_key = api_key_input
            st.experimental_rerun()
        st.stop()
        
    return openai_api_key
    
