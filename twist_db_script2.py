import json
import re
import random
import copy

def load_db():
    # Load original 111 questions
    with open('src/data/questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Filter back to only original core (if it was already manipulated, we find the first 111)
    core_db = [q for q in data if q['category'] == '최신 빈출 코어']
    if len(core_db) < 111:
        core_db = data[:111]
    return core_db[:111] # rigidly ensure 111

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
        distractors = [re.sub(r'^\d+\.\s*', '', c) for i, c in enumerate(item['choices']) if i != ans_idx]
        correct_choice = re.sub(r'^\d+\.\s*', '', item['choices'][ans_idx])
        
        # 1. Negative Variation (옳지 않은 것은?)
        neg = copy.deepcopy(item)
        neg['id'] = current_id
        
        words = base_q.replace("?", "").split()
        topic = " ".join(words[:4]) if len(words) >= 4 else base_q
        
        neg_q = f"[{current_id}번] 다음 중 '{topic}...' 에 대한 설명으로 옳지 않은 것을 고르시오."
        neg['question'] = neg_q
        
        true_statements = [
             f"{correct_choice}이(가) 이 상황에서 가장 권장되는 조치이다.",
             "해당 간호 시 환자의 프라이버시를 보호하고 편안한 환경을 제공해야 한다.",
             item['explanation'].replace('요.', '다.').replace('니다.', '다.'),
             "활력징후 측정 및 처치 결과는 즉시 간호기록부에 정확히 서명과 함께 기록한다.",
             "시술 전후로 반드시 흐르는 물에 비누로 손을 씻어 교차 감염을 예방한다."
        ]
        
        # Fake statement based on distractor
        selected_distractor = random.choice(distractors)
        false_statement = f"반드시 {selected_distractor} 처치를 가장 먼저 무조건 단독으로 시행해야 한다."
        
        choices = true_statements[:4]
        choices.append(false_statement)
        random.shuffle(choices)
        
        neg['choices'] = [f"{i+1}. {c}" for i, c in enumerate(choices)]
        neg['answer'] = choices.index(false_statement) + 1
        neg['category'] = "역추론 변형"
        neg['explanation'] = f"오답: {false_statement} / 해설: {item['explanation']}"
        new_db.append(neg)
        current_id += 1
        
        # 2. Case Scenario Variation
        case = copy.deepcopy(item)
        case['id'] = current_id
        
        case_q = f"[{current_id}번] 신입 간호조무사가 실무 현장에서 '{base_q}' 라는 질문을 선임에게 던졌다. 이에 대한 올바른 대답으로 짝지어진 것은?"
        case['question'] = case_q
        
        d_choices = [re.sub(r'^\d+\.\s*', '', c) for c in item['choices']]
        correct_str = d_choices[ans_idx]
        random.shuffle(d_choices)
        
        case['choices'] = [f"{i+1}. {c}" for i, c in enumerate(d_choices)]
        case['answer'] = d_choices.index(correct_str) + 1
        case['category'] = "사례/현장형 문항"
        new_db.append(case)
        current_id += 1
        
    return new_db

if __name__ == '__main__':
    db = load_db()
    new_db = generate_variations(db)
    with open('src/data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(new_db, f, ensure_ascii=False, indent=2)
    print(f"Refined and successfully generated {len(new_db)} deep-varied questions (3x natural twisted).")
