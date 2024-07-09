import openai
from embeddings import get_embedding
from graphs import D3Graph, MatplotGraph

class Chatbot:
    def __init__(self, qdrant_client, openai_api_key):
        self.client = qdrant_client
        openai.api_key = openai_api_key

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

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        return response.choices[0].text.strip()
