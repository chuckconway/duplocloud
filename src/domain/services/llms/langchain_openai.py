from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

rag_prompt_template = """
You are an AI assistant providing helpful information.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know. 
Don't try to make up an answer.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

def create_rag_chain(vector_store):
    # Create a retriever from the vector store
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # Retrieve top 4 most similar chunks
    )

    # Create the language model
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0
    )

    # Create the prompt
    prompt = PromptTemplate(
        template=rag_prompt_template,
        input_variables=["context", "question"]
    )

    # Create a QA chain
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt,
            "document_variable_name": "summaries"  # This must match the input variable in the prompt
        }

    )

    return qa_chain


def create_simple_rag_chain(vector_store):
    # Create a retriever from the vector store
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Create the language model
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0
    )

    # Use the from_chain_type factory with minimal customization
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Use the stuff chain type
        retriever=retriever,
        return_source_documents=True,
        # Don't provide a custom prompt - use the default
    )

    return qa_chain

def create_metadata_safe_rag_chain(vector_store):
    # Create a retriever from the vector store
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Create the language model
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0
    )

    # Create a custom document prompt that doesn't require 'source' metadata
    custom_document_prompt = PromptTemplate(
        template="{page_content}",
        input_variables=["page_content"]
    )

    # Create a QA prompt template
    qa_prompt = PromptTemplate(
        template="""Use the following extracted parts of documents to answer the question. If you don't know the answer, just say that you don't know. Don't try to make up an answer.

QUESTION: {question}

DOCUMENTS:
{context}

ANSWER:""",
        input_variables=["question", "context"]
    )

    # Create the QA chain with custom prompts
    qa_chain = load_qa_with_sources_chain(
        llm=llm,
        chain_type="stuff",
        prompt=qa_prompt,
        document_prompt=custom_document_prompt
    )

    # Connect the retriever to the QA chain
    return RetrievalQAWithSourcesChain(
        combine_documents_chain=qa_chain,
        retriever=retriever,
        return_source_documents=True
    )

    # Alternative approach: Adding default metadata to documents
def add_default_metadata_to_docs(retriever):
    """
    Wraps a retriever to add default metadata to documents that are missing it.
    """
    original_get_relevant_documents = retriever.get_relevant_documents

    def get_relevant_documents_with_metadata(*args, **kwargs):
        docs = original_get_relevant_documents(*args, **kwargs)
        for doc in docs:
            if 'source' not in doc.metadata:
                doc.metadata['source'] = 'Unknown source'
        return docs

    retriever.get_relevant_documents = get_relevant_documents_with_metadata
    return retriever


def create_explicit_rag_chain(vector_store):
    """
    Create a RAG chain by explicitly building each component with matching variable names.
    This avoids variable name conflicts in LangChain's internals.
    """
    # Create the language model
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0
    )

    # Create the retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Create a document prompt that only requires page_content
    document_prompt = PromptTemplate(
        template="{page_content}",
        input_variables=["page_content"]
    )

    # Create the main QA prompt with context as the variable name
    qa_prompt = PromptTemplate(
        template="""Use the following excerpts from documents to answer the question. 
If you don't know the answer, just say you don't know.

QUESTION: {question}

EXCERPTS:
{context}

ANSWER:""",
        input_variables=["question", "context"]
    )

    # Create the LLM chain to generate the answer
    llm_chain = LLMChain(
        llm=llm,
        prompt=qa_prompt
    )

    # Create the StuffDocumentsChain to combine documents
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_prompt=document_prompt,
        document_variable_name="context"  # This matches the variable in qa_prompt
    )

    # Create the Retrieval chain to handle the whole process
    qa_chain = RetrievalQAWithSourcesChain(
        combine_documents_chain=stuff_chain,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain


# Super simple approach that works with any version of LangChain
def create_very_simple_rag(vector_store):
    """
    A very simple approach to RAG that avoids complex chains.
    This is the most reliable approach that should work with any version of LangChain.
    """
    # Create the language model
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0
    )

    # Create the retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Define a function to process a question
    def process_question(question):
        # Get relevant documents
        docs = retriever.get_relevant_documents(question)

        # Extract content from documents
        contexts = [doc.page_content for doc in docs]
        combined_context = "\n\n".join(contexts)

        # Create a prompt manually
        prompt = f"""Use the following excerpts from documents to answer the question. 
If you don't know the answer, just say you don't know.

QUESTION: {question}

EXCERPTS:
{combined_context}

ANSWER:"""

        # Get response from LLM
        response = llm.invoke(prompt)

        # Return the result with source documents
        return {
            "answer": response.content,
            "source_documents": docs
        }

    # Return the processing function
    return process_question