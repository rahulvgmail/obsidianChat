import sonnet as snt
import tensorflow as tf
import tensorflow_text as text

class EmbeddingModel(snt.Module):
    def __init__(self, vocab_size, embedding_size):
        super().__init__()
        self.embedding = snt.Embed(vocab_size, embedding_size)
        self.tokenizer = text.WhitespaceTokenizer()
    
    def __call__(self, text):
        # Tokenize the text
        tokens = self.tokenizer.tokenize(text)
        
        # Convert tokens to integer indices (you'll need to implement this based on your vocabulary)
        indices = self.tokens_to_indices(tokens)
        
        # Get embeddings
        return self.embedding(indices)
    
    def tokens_to_indices(self, tokens):
        # This is a placeholder function. You need to implement this based on your vocabulary.
        # For now, let's just hash the tokens to get some integer values
        return tf.strings.to_hash_bucket_fast(tokens, num_buckets=self.embedding.vocab_size)

# Initialize the model (you'd need to train this with appropriate data)
vocab_size = 10000  # Example value, adjust as needed
embedding_size = 384  # To match the current setup
model = EmbeddingModel(vocab_size, embedding_size)

def get_embedding(text):
    # Ensure text is a tensor
    text_tensor = tf.constant([text])
    return model(text_tensor).numpy().tolist()[0]