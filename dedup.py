import json
import re

db_path = r"c:\간호조무사\src\data\questions.json"

with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

# The first 111 questions are core.
core_qs = db[:111]
new_qs = db[111:]

def clean_question_text(text):
    # Remove prefix like "[2021 상반기 짝수형]" 
    text = re.sub(r'^\[.*?\]\s*', '', text)
    # Re-normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_choices_set(choices):
    # remove "1. ", "2. " prefixes and spaces
    cleaned = []
    for c in choices:
        c_clean = re.sub(r'^\d+\.\s*', '', c)
        c_clean = re.sub(r'\s+', '', c_clean)
        cleaned.append(c_clean)
    return frozenset(cleaned)

unique_new_qs = []
seen_questions = {} # map of (cleaned_q, choices_set) -> question object

for q in new_qs:
    q_clean = clean_question_text(q['question'])
    c_set = get_choices_set(q['choices'])
    key = (q_clean, c_set)
    
    if key not in seen_questions:
        # Also clean the question text to remove the prefix permanently if preferred,
        # but the user might want to keep the origin info in the question.
        # Let's keep the prefix in the question, or move it to tip.
        seen_questions[key] = q
        unique_new_qs.append(q)

final_db = core_qs + unique_new_qs

# re-id
for i, q in enumerate(final_db):
    q["id"] = i + 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"Core questions: {len(core_qs)}")
print(f"New original pdf questions: {len(new_qs)}")
print(f"New UNIQUE pdf questions: {len(unique_new_qs)}")
print(f"Total questions: {len(final_db)}")
