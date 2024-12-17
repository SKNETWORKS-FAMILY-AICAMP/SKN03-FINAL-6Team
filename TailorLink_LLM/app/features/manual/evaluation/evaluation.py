import re
from collections import Counter
from itertools import islice
from bert_score import score
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import os

# METEOR
def normalize_text_for_evaluation(text):
    """
    Normalize the text by lowercasing and removing punctuation.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

def count_word_matches(reference, hypothesis):
    """
    Compute word matches between the reference and hypothesis.
    """
    ref_words = reference.split()
    hyp_words = hypothesis.split()

    ref_counts = Counter(ref_words)
    hyp_counts = Counter(hyp_words)

    # Find intersection of words
    matches = sum((ref_counts & hyp_counts).values())
    return matches

def calculate_meteor_score(reference, hypothesis):
    """
    Compute the METEOR score for a single pair of reference and hypothesis.
    """
    # Normalize texts
    reference = normalize_text_for_evaluation(reference)
    hypothesis = normalize_text_for_evaluation(hypothesis)

    # Calculate precision and recall
    matches = count_word_matches(reference, hypothesis)
    precision = matches / len(hypothesis.split()) if hypothesis.split() else 0
    recall = matches / len(reference.split()) if reference.split() else 0

    # Calculate F-measure
    if precision + recall > 0:
        f1_score = (10 * precision * recall) / (9 * precision + recall)
    else:
        f1_score = 0

    # Apply penalty for word order mismatch
    hyp_words = hypothesis.split()
    ref_words = reference.split()
    chunks = 0
    i = 0
    while i < len(hyp_words):
        if hyp_words[i] in ref_words:
            start_index = ref_words.index(hyp_words[i])
            while i < len(hyp_words) and start_index < len(ref_words) and hyp_words[i] == ref_words[start_index]:
                i += 1
                start_index += 1
            chunks += 1
        else:
            i += 1

    penalty = 0.5 * (chunks / matches) if matches > 0 else 1
    meteor_score = f1_score * (1 - penalty)

    # Return the detailed metrics
    return {
        "recall": recall,
        "precision": precision,
        "f1_score": f1_score
    }

# ROUGE-N
def generate_ngrams(text, n):
    """
    Generate n-grams from text.
    """
    tokens = text.split()
    return list(zip(*[tokens[i:] for i in range(n)]))

def calculate_rouge_n(reference, hypothesis, n=1):
    """
    Compute ROUGE-N score.
    """
    # Generate n-grams for reference and hypothesis
    ref_ngrams = Counter(generate_ngrams(reference, n))
    hyp_ngrams = Counter(generate_ngrams(hypothesis, n))

    # Count overlapping n-grams
    overlap = sum((ref_ngrams & hyp_ngrams).values())
    total_ref_ngrams = sum(ref_ngrams.values())
    total_hyp_ngrams = sum(hyp_ngrams.values())

    # Calculate Recall, Precision, and F1-score
    recall = overlap / total_ref_ngrams if total_ref_ngrams > 0 else 0
    precision = overlap / total_hyp_ngrams if total_hyp_ngrams > 0 else 0
    f1_score = (2 * recall * precision / (recall + precision)) if (recall + precision) > 0 else 0

    return {"recall": recall, "precision": precision, "f1_score": f1_score}

# ROUGE-L
def calculate_lcs_length(x, y):
    """
    Compute the length of the Longest Common Subsequence (LCS).
    """
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

def calculate_rouge_l(reference, hypothesis):
    """
    Compute ROUGE-L score.
    """
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()

    # Length of LCS
    lcs = calculate_lcs_length(ref_tokens, hyp_tokens)

    # Calculate Recall, Precision, and F1-score
    recall = lcs / len(ref_tokens) if len(ref_tokens) > 0 else 0
    precision = lcs / len(hyp_tokens) if len(hyp_tokens) > 0 else 0
    f1_score = (2 * recall * precision / (recall + precision)) if (recall + precision) > 0 else 0

    return {"recall": recall, "precision": precision, "f1_score": f1_score}

# BERTScore
def calculate_bertscore(reference, hypothesis, device=None):
    """
    Calculate BERTScore.
    """
    P, R, F1 = score(hypothesis, reference, lang="ko", verbose=True, device=device)
    return {"recall": R.mean().item(), "precision": P.mean().item(), "f1_score": F1.mean().item()}

# GPTScore
def get_gpt_perplexity(text):
    """
    Calculate GPT-based perplexity for a given text.
    """
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
    loss = outputs.loss
    perplexity = torch.exp(loss)
    return perplexity.item()

# Sentence Similarity
def calculate_sentence_cosine_similarity(reference, hypothesis, device=None):
    """
    Calculate cosine similarity between sentence embeddings.
    """
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device=device)

    # Generate embeddings
    ref_embedding = model.encode([reference])
    hyp_embedding = model.encode([hypothesis])

    # Compute cosine similarity
    similarity = cosine_similarity(ref_embedding, hyp_embedding)
    return {"Cosine Similarity": similarity[0][0]}

# G-EVAL
def calculate_g_eval(reference, hypothesis):
    """
    G-EVAL: GPT-based text evaluation.
    """
    client = OpenAI()
    prompt = f"""
    You are an expert evaluator for language models. Please evaluate the following two texts:

    Reference Text: "{reference}"
    Hypothesis Text: "{hypothesis}"

    Provide a similarity score between 0 and 100, where:
    - 0 means the texts are completely different.
    - 100 means the texts are identical in meaning and language quality.

    Please briefly explain in Korean the reasoning behind your score.
    """
    # Chat API call
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract response
    gpt_response = completion.choices[0].message.content
    return gpt_response

# RAG Evaluation
def evaluate_text_similarity(reference, hypothesis, use_g_eval=False, use_gpu=False):
    """
    Unified function to evaluate text similarity using various metrics.
    """
    results = {}

    # Device configuration
    device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"

    # METEOR
    results['METEOR'] = calculate_meteor_score(reference, hypothesis)

    # ROUGE-N (Unigram)
    results['ROUGE-1'] = calculate_rouge_n(reference, hypothesis, n=1)

    # ROUGE-L
    results['ROUGE-L'] = calculate_rouge_l(reference, hypothesis)

    # BERTScore
    results['BERTScore'] = calculate_bertscore([reference], [hypothesis], device)

    results['Precision'] = {
        "METEOR": results['METEOR']["precision"],
        "ROUGE-1": results['ROUGE-1']["precision"],
        "ROUGE-L": results['ROUGE-L']["precision"],
        "BERTScore": results['BERTScore']["precision"],
    }
    results['Recall'] = {
        "METEOR": results['METEOR']["recall"],
        "ROUGE-1": results['ROUGE-1']["recall"],
        "ROUGE-L": results['ROUGE-L']["recall"],
        "BERTScore": results['BERTScore']["recall"],
    }
    results['F1 Score'] = {
        "METEOR": results['METEOR']["f1_score"],
        "ROUGE-1": results['ROUGE-1']["f1_score"],
        "ROUGE-L": results['ROUGE-L']["f1_score"],
        "BERTScore": results['BERTScore']["f1_score"],
    }

    # Cosine Similarity
    results['Cosine Similarity'] = calculate_sentence_cosine_similarity(reference, hypothesis, device)

    # G-EVAL (optional)
    if use_g_eval:
        results['G-EVAL'] = calculate_g_eval(reference, hypothesis)
    else:
        results['G-EVAL'] = "Skipped"

    return results
