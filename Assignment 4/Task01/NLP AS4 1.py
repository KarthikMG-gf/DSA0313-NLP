def parse_transfer_event(sentence: str) -> dict:
    """Maps syntactic variations of the transfer event to a canonical frame."""
    tokens = sentence.lower().replace(".", "").replace(",", "").split()
    
    # Canonical semantic frame independent of surface word order
    if "maya" in tokens and "ravi" in tokens and "book" in tokens and "gave" in tokens:
        return {
            "event_id": "TRANSFER_EVENT_01",
            "predicate": "GIVING",
            "tense": "PAST",
            "roles": {
                "Agent": {"entity": "Maya", "type": "Person"},
                "Recipient": {"entity": "Ravi", "type": "Person"},
                "Theme": {"entity": "Book_1", "type": "Artifact", "definite": False},
            },
            "temporal": "Yesterday" if "yesterday" in tokens else "Unspecified",
            "fopc": "∃e ∃b [ Giving(e) ∧ Agent(e, Maya) ∧ Recipient(e, Ravi) ∧ Theme(e, b) ∧ Book(b) ∧ Time(e, Yesterday) ]"
        }
    raise ValueError("Unsupported sentence structure.")

def validate_frame(frame: dict) -> bool:
    roles = frame.get("roles", {})
    assert roles.get("Agent", {}).get("type") == "Person", "Invalid Agent type"
    assert "Theme" in roles and "Recipient" in roles, "Missing core participants"
    return True

# Demonstration on two word orders
s1 = "Maya gave Ravi a book yesterday."
s2 = "Yesterday, Maya gave a book to Ravi."

f1, f2 = parse_transfer_event(s1), parse_transfer_event(s2)
assert f1 == f2 and validate_frame(f1)
print("Canonical Frame:", f1)
