import re

class Chatbot:
    def __init__(self, index):
        self.index = index

    def get_response(self, user_input):
        keywords = re.findall(r'\w+', user_input.lower())
        relevant_files = set()
        for keyword in keywords:
            relevant_files.update(self.index.get(keyword, []))

        if not relevant_files:
            return "I couldn't find any relevant information in your vault."

        response = f"I found relevant information in the following files:\n"
        for file in relevant_files:
            response += f"- {file}\n"
        return response
