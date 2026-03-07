import re
import json
import os
import random

def parse_pdf_flexible():
    with open('pdf_output.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove page ends
    content = content.replace('---PAGE_END---', '')
    
    # Split content by '문제' keyword to handle multiple blocks
    blocks = content.split('문제')
    
    unique_questions = []
    seen_texts = set()
    
    for block in blocks[1:]: # Skip text before the first '문제'
        try:
            # We want to match: ' 1. [해부생리] 질문내용 \n ① 보기1 \n ② 보기2 \n ③ 보기3 \n ④ 보기4 \n ⑤ 보기5 \n 정답: ③ \n 해설: 주저리'
            
            # Simple line parsing
            lines = block.strip().split('\n')
            
            q_line = ""
            choices = []
            answer = 1
            explanation = ""
            category = "예상기출"
            
            mode = "question"
            ans_map = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
            
            for line in lines:
                l = line.strip()
                if not l: continue
                
                # Check mode transition
                if re.match(r'^[①②③④⑤1-5]\s*\.', l) or re.match(r'^[①②③④⑤]', l):
                    mode = "choice"
                elif l.startswith("정답:"):
                    mode = "answer"
                elif l.startswith("해설:"):
                    mode = "explanation"
                
                if mode == "question":
                    # Extract category if possible
                    cat_match = re.search(r'\[(.*?)\]', l)
                    if cat_match:
                        category = cat_match.group(1)
                        l = l.replace(f'[{category}]', '').strip()
                    
                    # Remove starting number like '1.' or '1 '
                    l = re.sub(r'^\d+[\.\s]*', '', l).strip()
                    q_line += l + " "
                
                elif mode == "choice":
                    # Clean choice text like '① 보기' -> '보기'
                    c_text = re.sub(r'^[①②③④⑤1-5][\.\s]*', '', l).strip()
                    choices.append(c_text)
                    mode = "wait_choice"
                elif mode == "wait_choice":
                    # If it didn't transition out, might be multi-line choice
                    # Let's just append to last choice
                    if choices:
                        choices[-1] += " " + l
                
                elif mode == "answer":
                    ans_char = l.replace("정답:", "").strip()
                    # Just find the first digit or circle number
                    ans_char = re.sub(r'[^\d①②③④⑤]', '', ans_char)
                    if ans_char:
                        answer = ans_map.get(ans_char[0], 1)
                
                elif mode == "explanation":
                    exp_text = l.replace("해설:", "").strip()
                    explanation += exp_text + " "
                    
            if not choices or len(choices) < 5:
                continue
                
            q_text = q_line.strip()
            norm_q = re.sub(r'\s+', ' ', q_text)
            
            if norm_q in seen_texts:
                continue
            seen_texts.add(norm_q)
            
            unique_questions.append({
                "category": category,
                "question": norm_q,
                "choices": choices[:5], # Take exactly 5
                "answer": answer,
                "explanation": explanation.strip(),
                "tip": "기출 변형 핵심 포인트!"
            })
            
        except Exception as e:
            pass

    return unique_questions

def main():
    new_qs = parse_pdf_flexible()
    print(f"Extracted unique questions from PDF: {len(new_qs)}")

    # We only output added questions for now to preview.
    print("Preview of 1 new question:")
    if new_qs:
        print(new_qs[0])
    
    # 2. Load existing DB -> 280
    # Overwrite all DB generation with the newly parsed PDF
    db_path = 'src/data/questions.json'
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            existing_qs = json.load(f)
    else:
         existing_qs = []
         
    # Let's count existing texts (only from the 280 we previously had)
    # The existing\_qs currently have 301. We want to clear out the 21 and insert the new.
    # We will just rewrite the `questions.json` by running `generate_db.py` to reset to 280, then add these.
    
    # Wait, we can just do it all in python here.
    with open('src/data/questions.json', 'w', encoding='utf-8') as f:
        # Actually first reset to 280
        pass

if __name__ == '__main__':
    qs = parse_pdf_flexible()
    print(len(qs))
