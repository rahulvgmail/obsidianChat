from langchain.chat_models import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from embeddings import get_embedding
from graphs import D3Graph, MatplotGraph

class Chatbot:
    def __init__(self, qdrant_client, anthropic_api_key):
        self.client = qdrant_client
        self.chat_model = ChatAnthropic(anthropic_api_key=anthropic_api_key)

    def get_response(self, user_input):
        query_vector = get_embedding(user_input)
        search_result = self.client.search(
            collection_name="obsidian_vault",
            query_vector=query_vector,
            limit=3
        )

        if not search_result:
            return "I couldn't find any relevant information in your vault."

        context = "\n".join([hit.payload['content'] for hit in search_result])
        
        messages = [
            SystemMessage(content="You are an AI assistant that helps users find information in their Obsidian vault. Use the following context to answer the user's question:"),
            HumanMessage(content=f"Context:\n{context}\n\nUser question: {user_input}")
        ]

        response = self.chat_model(messages)

        return response.content
