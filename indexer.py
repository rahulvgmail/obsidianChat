import os
import time
import random
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from embeddings import get_embedding
import logging
from typing import Union
import uuid
import hashlib

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def generate_unique_id():
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    random_num = random.randint(0, 999999)  # Random 6-digit number
    return f"{timestamp}{random_num}"

def deterministic_uuid(content: Union[str, bytes]) -> str:
    """Creates deterministic UUID on hash value of string or byte content.

    Args:
        content: String or byte representation of data.

    Returns:
        UUID of the content.
    """
    if isinstance(content, str):
        content_bytes = content.encode("utf-8")
    elif isinstance(content, bytes):
        content_bytes = content
    else:
        raise ValueError(f"Content type {type(content)} not supported !")

    hash_object = hashlib.sha256(content_bytes)
    hash_hex = hash_object.hexdigest()
    namespace = uuid.UUID("00000000-0000-0000-0000-000000000000")
    content_uuid = str(uuid.uuid5(namespace, hash_hex))

    return content_uuid

def chunk_text(text, max_chunk_size=2000, overlap=100):
    chunks = []
    start = 0
    text_length = len(text)

    while start + overlap < text_length:
        end = start + max_chunk_size
        if end > text_length:
            end = text_length
        else:
            # Find the last period or newline within the chunk to avoid cutting sentences
            last_period = text.rfind('.', start, end)
            last_newline = text.rfind('\n', start, end)
            end = max(last_period, last_newline)
            if end <= start + overlap:  # If no suitable breakpoint found, use the max_chunk_size
                end = start + max_chunk_size

        chunk = text[start:end].strip()
        chunks.append(chunk)
        start = end - overlap  # Move the start point back by the overlap amount
        
        # Safeguard against potential infinite loop
        if start >= end:
            start = end
            logger.warning(f"Potential overlap issue detected at position {start}. Continuing to next chunk.")

    return chunks

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
                logger.debug(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    chunks = chunk_text(content)
                    for i, chunk in enumerate(chunks):
                        embedding = get_embedding(chunk)
                        point_id = deterministic_uuid(chunk)
                        point = PointStruct(
                            id=point_id,
                            payload={
                                "file_path": file_path,
                                "content": chunk,
                                "chunk_index": i,
                                "total_chunks": len(chunks)
                            },
                            vector=embedding
                        )
                        logger.debug(f"Upserting point: {point}")
                        client.upsert(
                            collection_name="obsidian_vault",
                            points=[point],
                        )
                        logger.debug(f"Successfully upserted point with id: {point_id}")
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}")
                    logger.error(f"Error type: {type(e).__name__}")
                    logger.error(f"Error args: {e.args}")
                    continue  # Skip this file and continue with the next one
    return client