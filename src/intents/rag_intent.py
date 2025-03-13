from src.domain.models.action_base import ActionBase
from src.domain.models.chat_message import ChatMessage
from src.domain.repositories.chroma_repository import ChromaRepository
from src.domain.services.llms.langchain_openai import create_explicit_rag_chain, create_very_simple_rag


class RAGIntent(ActionBase):
    action_name = "rag_intent"

    def __init__(self, emit, message: ChatMessage, session: dict):
        self.base = super().__init__(emit)
        self.message = message
        self.session = session

    def execute(self):
        try:
            vector = ChromaRepository()
            chromadb = vector.get_chromadb()

            process_question = create_very_simple_rag(chromadb)
            result = process_question(self.message.message)

            # Format sources
            sources = []
            for doc in result.get("source_documents", []):
                # Get a snippet of the content
                content_preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                # Safely get source information if it exists
                source_name = "Unknown source"
                if hasattr(doc, 'metadata') and isinstance(doc.metadata, dict):
                    source_name = doc.metadata.get('source', 'Unknown source')

                sources.append({
                    "name": source_name,
                    "preview": content_preview
                })

            answer = f"Answer: {result.get('answer', '')}\n\nSources: {sources}"

        except Exception as e:
            # Provide a more detailed error message with traceback
            import traceback
            trace_str = traceback.format_exc()
            print(f"Error in RAGIntent: {trace_str}")
            answer = f"I encountered an error while searching the knowledge base: {str(e)}"

        new_message = self.create_new_message(answer, "message_classifier")
        self.emit_message(new_message)