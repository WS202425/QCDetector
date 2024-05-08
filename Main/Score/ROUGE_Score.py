from rouge import Rouge

# Example summaries
reference_summary = "The quick brown fox jumps over the lazy dog."
generated_summary = "A quick brown fox jumps over the dog."

# Initialize rouge object
rouge = Rouge()

# Calculating ROUGE scores
scores = rouge.get_scores(generated_summary, reference_summary)
print("ROUGE scores:", scores)
