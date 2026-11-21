def compose_semantics(attachment: str) -> dict:
    """
    Demonstrates compositional divergence for:
    'The experienced researcher saw the student with the telescope.'
    """
    subject = {"entity": "r", "predicates": ["Researcher(r)", "Experienced(r)"]}
    object_base = {"entity": "s", "predicates": ["Student(s)"]}
    pp_entity = {"entity": "t", "predicates": ["Telescope(t)"]}

    if attachment == "VP":  # High attachment (Instrument)
        return {
            "attachment": "VP (High)",
            "interpretation": "Researcher used the telescope to see the student.",
            "logic": "∃e [ Saw(e, r, s) ∧ Researcher(r) ∧ Experienced(r) ∧ Student(s) ∧ Telescope(t) ∧ Instrument(e, t) ]"
        }
    elif attachment == "NP":  # Low attachment (Accompaniment/Possession)
        return {
            "attachment": "NP (Low)",
            "interpretation": "Researcher saw the student who had the telescope.",
            "logic": "∃e [ Saw(e, r, s) ∧ Researcher(r) ∧ Experienced(r) ∧ Student(s) ∧ Telescope(t) ∧ Possesses(s, t) ]"
        }
    raise ValueError("Attachment must be 'VP' or 'NP'.")

print(compose_semantics("VP"))
print(compose_semantics("NP"))
