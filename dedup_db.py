import json
import re

def clean_question_text(q_text):
    # Remove numbering like [1번], [15번]
    q = re.sub(r'^\[\d+번\]\s*', '', q_text)
    
    # Remove context prefixes
    contexts = [
        "일반 병동 입원 환자 간호 시,",
        "[응급실 실무] 긴급 상황에서,",
        "[외래 진찰] 초진 환자 교육 과정 중,",
        "국시 기출 변형 사례:",
        "PDF 제공 기출:",
        "[의료 간호 현장]",
        "[핵심 실무 변경]",
        "[종합 응용 문항]",
        "[유튜브 빈출특강]",
        "[학원 원장님 강조]",
        "[요약 정리 필기]",
        "[시험 직전 벼락치기]"
    ]
    
    for ctx in contexts:
        if q.startswith(ctx):
            q = q[len(ctx):].strip()
            
    # Also remove any remaining extra spaces
    q = re.sub(r'\s+', ' ', q).strip()
    return q

def dedup_db():
    with open('src/data/questions.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)
        
    unique_core_qs = {}
    
    for item in existing:
        base_q = clean_question_text(item['question'])
        
        # We will keep the first instance of each base question
        if base_q not in unique_core_qs:
            unique_core_qs[base_q] = item
            
    deduped_list = list(unique_core_qs.values())
    
    # Re-number the IDs and format questions neatly
    for idx, item in enumerate(deduped_list):
        item['id'] = idx + 1
        base_q = clean_question_text(item['question'])
        item['question'] = f"[{idx + 1}번] {base_q}"
        
    print(f"Original inflated DB size: {len(existing)}")
    print(f"Truly Unique questions size after deduplication: {len(deduped_list)}")
    
    with open('src/data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(deduped_list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    dedup_db()
