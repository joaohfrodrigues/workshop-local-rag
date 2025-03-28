# Local RAG Workshop: Theory and Application with Ollama and LangChain

In this session, you will build a simple retrieval-augmented generation (RAG) pipeline and feed your large language model (LLM) with additional information in your prompts, that it can use to answer your questions.

## Before the Session

To ensure you're ready to participate, guarantee that you fulfill all pre-requisites of the session.

### Important: Download your contextual data

For this workshop, each participant will work with contextual data about themselves. To do it, download a copy of your LinkedIn data by going to Me >  Settings and Privacy > Data Privacy > Get a copy of your data.

The data won't be available right away so make sure you do this ahead of time.

If you don't have a LinkedIn account, reach out to the Workshop instructor for more information.

### Install Required Libraries

Run the following commands to clone the repo and install dependencies:

```bash
# Clone the repository
git clone <repo-url>
cd <repo-name>

# Create a virtual environment (optional)
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Install Ollama

Please install Ollama in your OS by following [this link](https://ollama.com).

We will be using llama, a state of the art LLM developed by Meta. LLMs require, as the name implies, large amounts of data to train and run. Since we are going to run these models locally, we will use one of the versions with least amount of parameters (3 billion).

We will also be using an embedding model for our contextual data.

To install them, use the commands below.

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

Take some time to try the models with some prompts, by using `ollama run llama3.2`.

### Optional: Familiarize Yourself with Tools

- [Ollama](https://ollama.com) documentation  
- [LangChain](https://python.langchain.com/en/latest/) documentation

## During the Session

Follow the guidelines in local_rag.ipynb.

## After the Session

- Explore extending the RAG pipeline with custom data.
- Experiment with different prompting techniques.
- Try to pump the performance by using cloud models.

## References

This course was heavily based in the following courses below.

- [DeepLearning.AI Course on LLMs](https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/)  
- [Towards Data Science Tutorial](https://towardsdatascience.com/local-rag-from-scratch-3afc6d3dea08)  
- [Ollama - Embedding Models](https://ollama.com/blog/embedding-models)
- [How to build chatbot with a local LLM and streamlit](https://medium.com/@auslei/how-to-build-chatbot-with-a-local-llm-in-5-minutes-a1b6898bc04b)