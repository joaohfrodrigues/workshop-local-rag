import streamlit as st
import ollama

MODEL = "llama3.2"
CONTEXT_SIZE = 8192

st.set_page_config(layout="wide")
st.title("Workshop Local RAG Chatbot Challenge")


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state.chat_history.append({"role": "system", "content": "You are a helpful assistant."})

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    response = ollama.chat(model=MODEL, 
                           options={"context": CONTEXT_SIZE},
                           messages=st.session_state.chat_history, 
                           stream=True)
    def response_generator():
        assistant_response = ''
        for chunk in response:
            assistant_response += chunk['message']['content']
            yield chunk['message']['content']
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.write_stream(response_generator())
