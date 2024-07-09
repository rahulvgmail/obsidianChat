import os
from collections import defaultdict

def index_vault(vault_path):
    index = defaultdict(list)
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    words = content.lower().split()
                    for word in words:
                        index[word].append(file_path)
    return index
