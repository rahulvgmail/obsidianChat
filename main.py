import os
from indexer import index_vault
from chatbot import Chatbot

def main():
    print("Starting the Obsidian vault chatbot...")
    vault_path = input("Enter the path to your Obsidian vault: ")
    if not os.path.exists(vault_path):
        print("The specified path does not exist.")
        return

    print("Indexing vault... This may take a while.")
    qdrant_client = index_vault(vault_path)
    chatbot = Chatbot(qdrant_client)

    print("Chatbot is ready. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = chatbot.get_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
