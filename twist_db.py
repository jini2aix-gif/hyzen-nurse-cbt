
import json
import re
import random
import copy

def load_db():
    with open('src/data/questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_variations(core_db):
    new_db = []
    
    current_id = 1
    
    for item in core_db:
        # Save Original
        orig = copy.deepcopy(item)
        orig['id'] = current_id
        orig['question'] = f"[{current_id}번] {re.sub(r'^\[\d+번\]\s*', '', orig['question'])}"
        new_db.append(orig)
        current_id += 1
        
        base_q = re.sub(r'^\[\d+번\]\s*', '', item['question']).strip()
        ans_idx = item['answer'] - 1
        distractors = [c for i, c in enumerate(item['choices']) if i != ans_idx]
        correct_choice = item['choices'][ans_idx]
        
        # 1. Negative Variation (옳지 않은 것은?)
        neg = copy.deepcopy(item)
        neg['id'] = current_id
        
        # Extract main topic. E.g "체온 측정 시 가장 높게 측정되며..." -> "체온 측정"
        words = base_q.split()
        topic = " ".join(words[:2]) if len(words) >= 2 else base_q
        
        neg_q = f"[{current_id}번] 다음 중 '{topic}' 관련 사항으로 옳지 않은 것을 고르시오."
        neg['question'] = neg_q
        
        # In a negative question, 4 choices must be true/plausible, 1 is blatantly false (the old distractor)
        # However, to do this without AI is hard, so we make the answer the opposite of correct.
        
        # Correct choice becomes true statement:
        true_statements = [
             "해당 처치 시 반드시 환자의 상태를 주의 깊게 살핀다.",
             "교과서 및 임상 실무 지침에 따라 가장 권장되는 조치를 취한다.",
             f"정답 지침에 따르면 {re.sub(r'^\d+\.\s*', '', correct_choice)} 사항이 가장 중요하다.",
             item['explanation']
        ]
        
        # The fake/false statement will be based on a distinct distractor
        false_statement = f"반드시 {re.sub(r'^\d+\.\s*', '', distractors[0])} 조치를 우선적으로 무조건 시행한다."
        
        choices = true_statements[:4]
        choices.append(false_statement)
        random.shuffle(choices)
        
        neg['choices'] = [f"{i+1}. {c}" for i, c in enumerate(choices)]
        neg['answer'] = choices.index(false_statement) + 1
        neg['category'] = "부정/오답 변형"
        new_db.append(neg)
        current_id += 1
        
        # 2. Case Scenario Variation
        case = copy.deepcopy(item)
        case['id'] = current_id
        
        case_q = f"[{current_id}번] 60세 환자가 김판서 간호조무사에게 질문을 던졌다. 현장 실무에서 `{base_q}` 라는 상황에 직면했을 때, 간호조무사가 시행해야 할 올바른 조치 혹은 답변으로 가장 적절한 것은?"
        case['question'] = case_q
        
        # Keep same choices but shuffled
        d_choices = [re.sub(r'^\d+\.\s*', '', c) for c in item['choices']]
        correct_str = d_choices[ans_idx]
        random.shuffle(d_choices)
        
        case['choices'] = [f"{i+1}. {c}" for i, c in enumerate(d_choices)]
        case['answer'] = d_choices.index(correct_str) + 1
        case['category'] = "현장 실무 변형"
        new_db.append(case)
        current_id += 1
        
    return new_db

if __name__ == '__main__':
    db = load_db()
    new_db = generate_variations(db)
    with open('src/data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(new_db, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {len(new_db)} deep-varied questions (3x rule-based twisted).")
