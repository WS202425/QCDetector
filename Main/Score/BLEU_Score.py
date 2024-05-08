from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import word_tokenize
import nltk
import json

nltk.download('punkt')
# Example sentences
with open("checking_topics_responses_ZH_38_100.json", "r", encoding="utf-8") as f:
    data = json.load(f)
# Tokenizing the sentences
    for item in data:
        reference_tokens = word_tokenize(reference.lower())
        candidate_tokens = word_tokenize(candidate.lower())

# Calculating BLEU score
score = sentence_bleu([reference_tokens], candidate_tokens)
print(f"BLEU score: {score}")
