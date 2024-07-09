import sonnet
from embeddings import get_embedding

class Chatbot:
    def __init__(self, qdrant_client):
        self.client = qdrant_client
        self.chat_model = sonnet.ChatModel()

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
        
        prompt = f"""
        You are an AI assistant that helps users find information in their Obsidian vault.
        Use the following context to answer the user's question:

        {context}

        User question: {user_input}
        """

        response = self.chat_model.generate(prompt)
        return response
