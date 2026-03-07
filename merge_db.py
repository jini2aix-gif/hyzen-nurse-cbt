import re
import json
import random

def get_unique_from_pdf():
    with open('pdf_output.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple lines processing for robust extraction
    content = content.replace('---PAGE_END---', '')
    
    # We will use regex but be very flexible
    pattern = re.compile(
        r'문제\s+\d+\.\s*(?:\[([^\]]+)\])?\s*(.*?)\n'
        r'①\s*(.*?)\n②\s*(.*?)\n③\s*(.*?)\n④\s*(.*?)\n⑤\s*(.*?)\n'
        r'정답:\s*([①②③④⑤])\s*\n'
        r'해설:\s*(.*?)(?=\n문제\s+\d+\.|\Z)', 
        re.DOTALL
    )
    
    matches = pattern.findall(content)
    
    ans_map = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
    
    unique_qs = []
    seen = set()
    
    for match in matches:
        category = match[0].strip() if match[0] else '기출예상'
        q_text = match[1].strip().replace('\n', ' ')
        norm_q = re.sub(r'\s+', ' ', q_text)
        
        if norm_q in seen:
            continue
        seen.add(norm_q)
        
        choices = [match[2].strip(), match[3].strip(), match[4].strip(), match[5].strip(), match[6].strip()]
        answer = ans_map.get(match[7].strip(), 1)
        explanation = match[8].strip().replace('\n', ' ')
        
        unique_qs.append({
            "category": category,
            "question": norm_q,
            "choices": choices,
            "answer": answer,
            "explanation": explanation,
            "tip": "제공해주신 특급 기출 DB!"
        })
        
    return unique_qs

def merge_db():
    pdf_core = get_unique_from_pdf()
    
    # Load existing 280
    with open('src/data/questions.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)
        
    start_id = max(q['id'] for q in existing) + 1
    
    contexts = [
        "PDF 제공 기출:",
        "[의료 간호 현장]",
        "[핵심 실무 변경]",
        "[종합 응용 문항]"
    ]
    
    extra_added = 0
    # Duplicate prevention against existing texts
    existing_texts = set(re.sub(r'\[\d+번\]\s*', '', q.get('question', '')).strip() for q in existing)
    
    for core in pdf_core:
        norm_q = core['question']
        
        for i in range(4):
            ctx_q = f"{contexts[i]} {norm_q}"
            if ctx_q in existing_texts:
                continue
            existing_texts.add(ctx_q)
            
            # choices
            d_choices = list(core['choices'])
            correct_text = d_choices[core['answer'] - 1]
            random.shuffle(d_choices)
            new_ans_idx = d_choices.index(correct_text) + 1
            
            existing.append({
                "id": start_id,
                "category": core['category'],
                "question": f"[{start_id}번] {ctx_q}",
                "choices": [f"{idx+1}. {c}" for idx, c in enumerate(d_choices)],
                "answer": new_ans_idx,
                "explanation": core['explanation'],
                "tip": core['tip']
            })
            start_id += 1
            extra_added += 1
            
    print(f"Added {extra_added} variations from {len(pdf_core)} unique PDF core questions.")
    print(f"Total Database Size Now: {len(existing)}")
    
    with open('src/data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    merge_db()
