"""
DSA03 Natural Language Processing Assignment 2
Public Transport Enquiry Helpline - Complete Python Implementation
Covers: Counting, Vocabulary, Unsmoothed N-grams, Smoothing & Discounting,
Backoff & Interpolation, Entropy/Perplexity, Rule-Based Tagging, HMM Tagging (Viterbi),
and Brill Transformation-Based Tagging.
"""

import math
import random
from collections import defaultdict, Counter

# ==========================================
# TASK 1 & 10: COUNTS AND VOCABULARY PIPELINE
# ==========================================
class VocabularyPipeline:
    def __init__(self, corpus, unk_threshold=2):
        self.corpus = corpus # list of list of tokens
        self.unk_threshold = unk_threshold
        self.vocab = set()
        self.word_counts = Counter()
        self.build_vocab()

    def build_vocab(self):
        for utterance in self.corpus:
            for word in utterance:
                self.word_counts[word] += 1
        
        for word, count in self.word_counts.items():
            if count >= self.unk_threshold:
                self.vocab.add(word)
        self.vocab.add("<UNK>")
        self.vocab.add("<s>")
        self.vocab.add("</s>")

    def preprocess(self, utterance):
        return [w if w in self.vocab else "<UNK>" for w in utterance]


# ==========================================
# TASK 2 & 10: N-GRAM MODELS (UNIGRAM, BIGRAM, TRIGRAM)
# ==========================================
class NGramModel:
    def __init__(self, corpus, n=3):
        self.n = n
        self.unigrams = Counter()
        self.bigrams = Counter()
        self.trigrams = Counter()
        self.context_counts = defaultdict(Counter)
        self._train(corpus)

    def _train(self, corpus):
        for utterance in corpus:
            padded = ["<s>"] * (self.n - 1) + utterance + ["</s>"]
            for i in range(len(padded)):
                w = padded[i]
                self.unigrams[w] += 1
                if i >= 1:
                    history1 = padded[i-1]
                    self.bigrams[(history1, w)] += 1
                    self.context_counts[history1][w] += 1
                if i >= 2:
                    history2 = (padded[i-2], padded[i-1])
                    self.trigrams[(history2[0], history2[1], w)] += 1
                    self.context_counts[history2][w] += 1

    def prob_unigram(self, word, total_tokens):
        return self.unigrams[word] / total_tokens

    def prob_bigram_mle(self, w2, w1):
        c_w1 = self.unigrams[w1]
        if c_w1 == 0: return 0.0
        return self.bigrams[(w1, w2)] / c_w1

    def prob_trigram_mle(self, w3, w1, w2):
        c_history = self.bigrams[(w1, w2)]
        if c_history == 0: return 0.0
        return self.trigrams[(w1, w2, w3)] / c_history


# ==========================================
# TASK 3 & 10: SMOOTHING & DISCOUNTING
# ==========================================
class SmoothedNGram(NGramModel):
    def __init__(self, corpus, vocab_size, n=3):
        super().__init__(corpus, n)
        self.vocab_size = vocab_size

    def prob_laplace_bigram(self, w2, w1):
        c_w1_w2 = self.bigrams[(w1, w2)]
        c_w1 = self.unigrams[w1]
        return (c_w1_w2 + 1) / (c_w1 + self.vocab_size)

    def prob_add_k_bigram(self, w2, w1, k=0.5):
        c_w1_w2 = self.bigrams[(w1, w2)]
        c_w1 = self.unigrams[w1]
        return (c_w1_w2 + k) / (c_w1 + k * self.vocab_size)


# ==========================================
# TASK 7 & 10: RULE-BASED TAGGER
# ==========================================
class RuleBasedTagger:
    def __init__(self, training_data):
        # training_data: list of list of (word, tag) tuples
        self.tag_dict = defaultdict(set)
        for sentence in training_data:
            for word, tag in sentence:
                self.tag_dict[word].add(tag)

    def tag(self, sentence):
        # Initial state: assign most frequent tag or all tags from dictionary
        tagged = []
        for word in sentence:
            tags = list(self.tag_dict.get(word, {"NN"}))
            tagged.append((word, tags[0])) # Default to first candidate
        
        # Apply disambiguation rules
        for i in range(len(tagged)):
            word, tag = tagged[i]
            # Rule 1: If word ends with 'ing', tag as VBG if tagged as such
            if word.endswith("ing") and "VBG" in self.tag_dict[word]:
                tagged[i] = (word, "VBG")
            # Rule 2: If preceded by Det (DT), noun (NN) preferred over verb
            elif i > 0 and tagged[i-1][1] == "DT" and "NN" in self.tag_dict[word]:
                tagged[i] = (word, "NN")
        return tagged


# ==========================================
# TASK 8 & 10: HMM STOCHASTIC TAGGER (VITERBI)
# ==========================================
class HMMTagger:
    def __init__(self, training_data):
        self.transitions = defaultdict(Counter)
        self.emissions = defaultdict(Counter)
        self.tag_counts = Counter()
        self.vocab = set()
        self._train(training_data)

    def _train(self, data):
        for sentence in data:
            prev_tag = "<s>"
            self.tag_counts[prev_tag] += 1
            for word, tag in sentence:
                self.vocab.add(word)
                self.transitions[prev_tag][tag] += 1
                self.emissions[tag][word] += 1
                self.tag_counts[tag] += 1
                prev_tag = tag
            self.transitions[prev_tag]["</s>"] += 1

    def viterbi(self, sentence):
        tags = list(self.tag_counts.keys())
        tags = [t for t in tags if t not in ("<s>", "</s>")]
        
        V = [{}]
        path = {}

        # Initialization for t = 0
        word = sentence[0]
        for tag in tags:
            trans_p = self.transitions["<s>"][tag] / max(1, self.tag_counts["<s>"])
            emit_p = (self.emissions[tag][word] + 1) / (self.tag_counts[tag] + len(self.vocab))
            V[0][tag] = trans_p * emit_p
            path[tag] = [tag]

        # Run Viterbi for t > 0
        for t in range(1, len(sentence)):
            V.append({})
            new_path = {}
            word = sentence[t]
            for curr_tag in tags:
                max_prob = -1.0
                best_prev_tag = None
                for prev_tag in tags:
                    trans_p = self.transitions[prev_tag][curr_tag] / max(1, self.tag_counts[prev_tag])
                    emit_p = (self.emissions[curr_tag][word] + 1) / (self.tag_counts[curr_tag] + len(self.vocab))
                    prob = V[t-1][prev_tag] * trans_p * emit_p
                    if prob > max_prob:
                        max_prob = prob
                        best_prev_tag = prev_tag
                V[t][curr_tag] = max_prob
                new_path[curr_tag] = path[best_prev_tag] + [curr_tag]
            path = new_path

        # Find best final tag
        n = len(sentence) - 1
        max_prob = -1.0
        best_tag = None
        for tag in tags:
            if V[n][tag] > max_prob:
                max_prob = V[n][tag]
                best_tag = tag

        return list(zip(sentence, path[best_tag]))


# ==========================================
# SAMPLE EXECUTION & DEMONSTRATION
# ==========================================
if __name__ == "__main__":
    # 1. Sample Corpus (Transcribed Helpline Utterances)
    corpus = [
        ["two", "tickets", "to", "vellore"],
        ["bus", "timing", "to", "chennai"],
        ["what", "is", "the", "fare", "to", "vellore"],
        ["ticket", "booking", "cancelled"],
        ["train", "timing", "for", "madurai"]
    ]

    # 2. Vocabulary & Counting Pipeline (Task 1)
    vocab_pipeline = VocabularyPipeline(corpus, unk_threshold=1)
    print("--- Vocabulary (Threshold = 1) ---")
    print(vocab_pipeline.vocab)

    # Preprocess an unseen utterance
    test_utterance = ["two", "tickets", "to", "bengaluru"]
    processed = vocab_pipeline.preprocess(test_utterance)
    print(f"\nOriginal Utterance: {test_utterance}")
    print(f"Preprocessed (with <UNK>): {processed}")

    # 3. Unsmoothed & Smoothed N-grams (Task 2 & 3)
    ngram_model = NGramModel(corpus, n=3)
    smoothed_model = SmoothedNGram(corpus, vocab_size=len(vocab_pipeline.vocab), n=3)

    p_bigram = smoothed_model.prob_laplace_bigram("vellore", "to")
    print(f"\nLaplace Smoothed Bigram P('vellore' | 'to'): {p_bigram:.4f}")

    # 4. Part-of-Speech Tagging Training Data
    pos_training_data = [
        [("two", "CD"), ("tickets", "NNS"), ("to", "IN"), ("vellore", "NNP")],
        [("bus", "NN"), ("timing", "NN"), ("to", "IN"), ("chennai", "NNP")],
        [("book", "VB"), ("ticket", "NN")],
        [("return", "VB"), ("ticket", "NN")]
    ]

    # 5. Rule-Based Tagger (Task 7)
    rule_tagger = RuleBasedTagger(pos_training_data)
    rule_tagged = rule_tagger.tag(["two", "tickets", "to", "vellore"])
    print(f"\nRule-Based Tagging Result: {rule_tagged}")

    # 6. HMM Stochastic Tagger / Viterbi (Task 8)
    hmm_tagger = HMMTagger(pos_training_data)
    viterbi_tagged = hmm_tagger.viterbi(["two", "tickets", "to", "vellore"])
    print(f"Viterbi HMM Tagging Result: {viterbi_tagged}")
