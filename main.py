import os
from dotenv import load_dotenv
from indexer import index_vault
from chatbot import Chatbot

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
    print("For multiline input, start your message and press Enter.")
    print("Continue typing on new lines. Type '##END' on a new line to finish your input.")
    while True:
        print("You: ", end="")
        user_input_lines = []
        while True:
            line = input()
            if line.strip() == "##END":
                break
            user_input_lines.append(line)
        
        user_input = "\n".join(user_input_lines)
        
        if user_input.lower().strip() == 'quit':
            break
        if user_input.strip():
            response = chatbot.get_response(user_input)
            print("Chatbot:", response)

if __name__ == "__main__":
    main()
