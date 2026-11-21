def support_bot_pipeline(message: str, portal_domain: str = "BANKING") -> dict:
    # Step 1: Ambiguity detection & anaphora resolution ('it' -> 'bank' due to 'closed')
    candidates = {
        "BANKING": {
            "interpretation": "User saw someone duck near a bank branch, and the branch was closed.",
            "concepts": {"SYN:FINANCIAL_BANK", "SYN:CLOSED_STATUS"},
            "fopc": "∃e1 ∃e2 ∃b [ Saw(e1, speaker, e2) ∧ Duck_Action(e2, her) ∧ Near(e2, b) ∧ FinancialBank(b) ∧ Closed(b) ]"
        },
        "PARK": {
            "interpretation": "User saw her duck near a riverbank, and the park area was closed.",
            "concepts": {"SYN:RIVER_BANK", "SYN:CLOSED_STATUS"},
            "fopc": "∃e1 ∃d ∃b [ Saw(e1, speaker, d) ∧ Bird_Duck(d) ∧ Possess(her, d) ∧ Near(d, b) ∧ RiverBank(b) ∧ Closed(b) ]"
        }
    }
    
    # Step 2: Override domain prior if explicit wildlife distress cue appears (Stage 5 refinement)
    if "injured bird" in message.lower() or "wildlife" in message.lower():
        selected_domain = "PARK"
    else:
        selected_domain = portal_domain if portal_domain in candidates else "CLARIFY"
        
    if selected_domain == "CLARIFY":
        return {"action": "ASK_CLARIFICATION", "question": "Are you referring to a bank branch or a riverbank area?"}
    
    selected = candidates[selected_domain]
    articles = [
        {"id": "Doc_101", "title": "Branch Operating Hours & Closures", "concepts": {"SYN:FINANCIAL_BANK", "SYN:CLOSED_STATUS"}},
        {"id": "Doc_102", "title": "Riverbank Trail & Park Closures", "concepts": {"SYN:RIVER_BANK", "SYN:CLOSED_STATUS"}},
    ]
    
    best_doc = max(articles, key=lambda a: len(a["concepts"] & selected["concepts"]))
    return {"selected_interpretation": selected, "retrieved_article": best_doc}

print("Standard Banking Context:", support_bot_pipeline("I saw her duck near the bank, and it was closed.", "BANKING"))
print("Adversarial Override:", support_bot_pipeline("I saw her duck near the bank, and it was closed—where can I report an injured bird?", "BANKING"))
