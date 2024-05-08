from transformers import AutoTokenizer, AutoModel
import torch

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
model = AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

# Example sentences
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast brown fox leaps over a lazy dog."

# Tokenize and encode sentences to get their embeddings
encoded_input_1 = tokenizer(sentence1, return_tensors='pt', padding=True, truncation=True, max_length=128)
encoded_input_2 = tokenizer(sentence2, return_tensors='pt', padding=True, truncation=True, max_length=128)

with torch.no_grad():
    model_output_1 = model(**encoded_input_1)
    model_output_2 = model(**encoded_input_2)

# Mean pooling to get sentence embeddings
embeddings_1 = model_output_1.last_hidden_state.mean(dim=1)
embeddings_2 = model_output_2.last_hidden_state.mean(dim=1)

# Calculate cosine similarity
cosine_similarity = torch.nn.CosineSimilarity(dim=1)
similarity_score = cosine_similarity(embeddings_1, embeddings_2)
print(f"Semantic similarity score: {similarity_score.item()}")
