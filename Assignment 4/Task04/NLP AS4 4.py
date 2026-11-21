import re

SENSE_INVENTORY = {
    "NOUN": {
        "S1_Financial_Institution": {"deposit", "deposited", "cash", "account", "loan", "money", "branch"},
        "S2_River_Margin": {"river", "water", "sat", "muddy", "fisherman", "shore", "stream"}
    },
    "VERB": {
        "S3_Lateral_Tilt_Maneuver": {"pilot", "aircraft", "plane", "left", "right", "turn", "wing"}
    }
}

def disambiguate_bank(sentence: str, pos: str) -> dict:
    tokens = set(re.findall(r"[a-z]+", sentence.lower()))
    candidates = SENSE_INVENTORY.get(pos, {})
    
    scores = {}
    evidence = {}
    for sense_id, cues in candidates.items():
        overlap = tokens.intersection(cues)
        scores[sense_id] = len(overlap)
        evidence[sense_id] = sorted(list(overlap))
    
    # Fallback to S1 for NOUN if tied at 0
    best_sense = max(scores, key=lambda k: scores[k])
    return {
        "sentence": sentence,
        "pos": pos,
        "predicted_sense": best_sense,
        "evidence": evidence[best_sense]
    }

test_cases = [
    ("Nila deposited cash at the bank.", "NOUN"),
    ("They sat on the bank of the river.", "NOUN"),
    ("The pilot banked the aircraft to the left.", "VERB"),
    ("The fisherman walked along the muddy bank before sunrise.", "NOUN"),
]

for sent, tag in test_cases:
    print(disambiguate_bank(sent, tag))
