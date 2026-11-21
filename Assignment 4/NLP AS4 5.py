import numpy as np

def cosine_sim(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def concept_jaccard(c1: set, c2: set) -> float:
    return len(c1 & c2) / len(c1 | c2) if (c1 | c2) else 0.0

query = {
    "text": "methods for finding the meaning of ambiguous words",
    "dense": np.array([0.85, 0.78, 0.10]),
    "concepts": {"SYN:WSD", "SYN:POLYSEMY", "SYN:ALGORITHM"}
}

documents = [
    {"id": "D1", "title": "Supervised Lesk Approaches to Polysemy Resolution", "dense": np.array([0.84, 0.80, 0.12]), "concepts": {"SYN:WSD", "SYN:POLYSEMY", "SYN:ALGORITHM"}, "title_match": True},
    {"id": "D2", "title": "Word Sense Disambiguation Algorithms", "dense": np.array([0.88, 0.82, 0.08]), "concepts": {"SYN:WSD", "SYN:ALGORITHM"}, "title_match": True},
    {"id": "D3", "title": "Lexical Ambiguity Resolution Survey", "dense": np.array([0.81, 0.75, 0.15]), "concepts": {"SYN:POLYSEMY", "SYN:WSD"}, "title_match": True},
    {"id": "D4", "title": "Contextual Embeddings for Semantics", "dense": np.array([0.79, 0.74, 0.18]), "concepts": {"SYN:WSD"}, "title_match": False},
    {"id": "D6", "title": "Syntactic Parsing of Structural Ambiguity", "dense": np.array([0.65, 0.30, 0.75]), "concepts": {"SYN:SYNTAX"}, "title_match": False},
]

ranked = []
for doc in documents:
    score = (
        0.45 * cosine_sim(query["dense"], doc["dense"])
        + 0.35 * concept_jaccard(query["concepts"], doc["concepts"])
        + 0.20 * (1.0 if doc["title_match"] else 0.3)
    )
    ranked.append((doc["id"], round(score, 3), doc["title"]))

ranked.sort(key=lambda x: x[1], reverse=True)
for r in ranked:
    print(r)

# Precision & Recall calculation
relevant_set = {"D1", "D2", "D3", "D4", "D5"}
retrieved_set = {"D1", "D2", "D4", "D6"}
precision = len(relevant_set & retrieved_set) / len(retrieved_set)
recall = len(relevant_set & retrieved_set) / len(relevant_set)
print(f"Precision: {precision:.2f}, Recall: {recall:.2f}")
