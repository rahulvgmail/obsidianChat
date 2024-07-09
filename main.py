import os
from dotenv import load_dotenv
from indexer import index_vault
from chatbot import Chatbot
import logging

# Add this near the top of your main.py file, after the imports
logging.getLogger("httpcore").setLevel(logging.WARNING)

def main():
    # Load environment variables from .env file
    load_dotenv()

    print("Starting the Obsidian vault chatbot...")
    vault_path = input("Enter the path to your Obsidian vault: ")
    if not os.path.exists(vault_path):
        print("The specified path does not exist.")
        return

    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        print("Anthropic API key is not set in the .env file.")
        return

    print("Indexing vault... This may take a while.")
    qdrant_client = index_vault(vault_path)
    chatbot = Chatbot(qdrant_client, anthropic_api_key)

    print("Chatbot is ready. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = chatbot.get_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()