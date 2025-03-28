import csv
import chromadb
import ollama
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from typing import Dict, List, Optional
from os import listdir
from os.path import isfile, join

class CSVLoader(BaseLoader):
    def __init__(
        self,
        file_paths: List[str],
        source_column: Optional[str] = None,
        csv_args: Optional[Dict] = None,
        encoding: Optional[str] = None,
    ):
        self.file_paths = file_paths
        self.source_column = source_column
        self.encoding = encoding
        self.csv_args = csv_args or {}

    def load(self) -> List[Document]:
        docs = []
        for file_path in self.file_paths:
            with open(file_path, newline="", encoding=self.encoding) as csvfile:
                csv_reader = csv.DictReader(csvfile, **self.csv_args)  # type: ignore
                for i, row in enumerate(csv_reader):
                    content = "\n".join(f"{k.strip()}: {v.strip()}" for k, v in row.items())
                    try:
                        source = (
                            row[self.source_column]
                            if self.source_column is not None
                            else file_path
                        )
                    except KeyError:
                        raise ValueError(
                            f"Source column '{self.source_column}' not found in CSV file."
                        )
                    metadata = {"source": source, "row": i}
                    doc = Document(page_content=content, metadata=metadata)
                    docs.append(doc)
        return docs

def load_data_setup_collection():
    files_list = [f'docs/{f}' for f in listdir("docs") if isfile(join("docs", f))]
    loader = CSVLoader(file_paths=files_list)
    docs = loader.load()
    collection = chromadb.Client().create_collection(name="docs_chatbot")

    # store each document in a vector embedding database
    for i, d in enumerate(docs):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d.__str__())
        embedding = response["embedding"]
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d.__str__()]
        )
    return collection

def get_embedding_data(collection, prompt: str, n_results=20):
  """Get embedding data from the prompt

  Args:
      promtp (str): The prompt to get the embedding data from

  Returns:
      List[List[Document]] : The embedding data
  """
  response = ollama.embeddings(
    prompt=prompt,
    model="mxbai-embed-large"
  )
  results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=n_results
  )
  return results['documents']