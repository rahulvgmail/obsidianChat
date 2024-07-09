import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from embeddings import get_embedding

def index_vault(vault_path):
    client = QdrantClient(":memory:")
    client.create_collection(
        collection_name="obsidian_vault",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    embedding = get_embedding(content)
                    client.upsert(
                        collection_name="obsidian_vault",
                        points=[
                            {
                                "id": str(hash(file_path)),
                                "payload": {"file_path": file_path, "content": content},
                                "vector": embedding,
                            }
                        ],
                    )
    return client
