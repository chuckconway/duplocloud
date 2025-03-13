import os
from uuid import uuid4

import chromadb
from chromadb.utils import embedding_functions
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

collection_name = "duplocloud_documentation"

class ChromaRepository:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    def get_chromadb(self) -> Chroma:
        persistent_client = chromadb.PersistentClient()

        # Create the OpenAI embedding function
        openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="text-embedding-3-large",
            dimensions=3072  # Explicitly set dimensions for text-embedding-3-large
        )

        # Check if collection exists, create only if it doesn't
        try:
            collection = persistent_client.get_collection(collection_name)
            print(f"Using existing collection: {collection_name}")
        except:
            # Collection doesn't exist, create it
            print(f"Creating new collection: {collection_name}")
            collection = persistent_client.create_collection(
                name=collection_name,
                embedding_function=openai_ef,
                metadata={"hnsw:space": "cosine"}  # Specify distance metric
            )

        # Create the Langchain Chroma wrapper with this collection
        vector_store_from_client = Chroma(
            client=persistent_client,
            collection_name=collection_name,
            embedding_function=self.embeddings,  # Using the class embeddings
            # persist_directory="./chroma_langchain_db"
        )

        return vector_store_from_client

    def upsert(self,  directory_path: str):

        markdown_files = self.find_markdown_files(directory_path)
        docs = []

        for markdown_file in markdown_files:
            source_name = os.path.basename(markdown_file)
            markdown_text = self.read_markdown_file(markdown_file)

            docs.append(Document(page_content=markdown_text, metadata={"source_path": markdown_file, "source": source_name}, id=source_name))

        uuids = [str(uuid4()) for _ in range(len(docs))]

        chroma_client = self.get_chromadb()
        chroma_client.add_documents(docs, ids=uuids)

    def find_markdown_files(self, directory) -> list[str]:
        """
        Recursively loads Markdown files from the specified directory.

        Args:
            directory (str): The directory to start searching from.

        Returns:
            list: A list of paths to Markdown files.
        """
        markdown_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".md") and not file.lower().endswith("readme.md"):
                    markdown_files.append(os.path.join(root, file))

        return markdown_files

    def read_markdown_file(self, file_path) -> str | None:
        """
        Opens and reads the text from a Markdown file.

        Args:
            file_path (str): The path to the Markdown file.

        Returns:
            str: The text contents of the Markdown file.
        """
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                return text
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def search(self, query: str):
        vector_store = self.get_chromadb()
        results = vector_store.similarity_search_with_score(
            query,
            k=2, # top 2 results
        )

        return results

