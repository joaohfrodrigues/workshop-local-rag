import streamlit as st
import ollama
from utils import get_embedding_data, load_data_setup_collection

MODEL = "llama3.2"
CONTEXT_SIZE = 8192

st.set_page_config(layout="wide")
st.title("Workshop Local RAG Chatbot Solution")

# Added to make sure the collection is loaded only once
if "collection" not in st.session_state:
    st.session_state.collection = load_data_setup_collection()

# Added an extra key "user_prompt" to store the user prompt while using content to store the prompt with context
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state.chat_history.append({"role": "system", "content": "You are a helpful assistant.", "user_prompt": "You are a helpful assistant."})

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["user_prompt"])

if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # generate a response combining the prompt and data
    data = get_embedding_data(st.session_state.collection, prompt)
    prompt_with_context = f"Using this data: {data}. Respond to this prompt: {prompt}"
    
    st.session_state.chat_history.append({"role": "user", "content": prompt_with_context, "user_prompt": prompt})
    response = ollama.chat(model=MODEL, 
                           options={"context": CONTEXT_SIZE},
                           messages=st.session_state.chat_history, 
                           stream=True)
    def response_generator():
        assistant_response = ''
        for chunk in response:
            assistant_response += chunk['message']['content']
            yield chunk['message']['content']
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response, "user_prompt": assistant_response})

    with st.chat_message("assistant"):
        st.write_stream(response_generator())