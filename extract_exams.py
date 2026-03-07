import fitz
import sys
import glob
import re
import json
import os

def parse_questions(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    
    qs = {}
    blocks = re.split(r'\n(\d+)\.\s+', "\n" + text)
    
    for i in range(1, len(blocks), 2):
        q_num = int(blocks[i])
        chunk = blocks[i+1]
        
        c1_idx = chunk.find('①')
        c2_idx = chunk.find('②')
        c3_idx = chunk.find('③')
        c4_idx = chunk.find('④')
        c5_idx = chunk.find('⑤')
        
        if c1_idx == -1 or c2_idx == -1 or c3_idx == -1 or c4_idx == -1 or c5_idx == -1:
            continue
            
        q_text = chunk[:c1_idx].strip()
        c1 = chunk[c1_idx+1:c2_idx].strip()
        c2 = chunk[c2_idx+1:c3_idx].strip()
        c3 = chunk[c3_idx+1:c4_idx].strip()
        c4 = chunk[c4_idx+1:c5_idx].strip()
        c5 = chunk[c5_idx+1:].strip()
        
        c5 = re.sub(r'\n?(\d+)\s+-\s+(\d+).*', '', c5, flags=re.DOTALL).strip()
        c5 = re.sub(r'간호조무사.*', '', c5, flags=re.DOTALL).strip()
        c5_lines = c5.split('\n')
        c5_final = ""
        for line in c5_lines:
            if "교시" in line or "짝수형" in line or "홀수형" in line:
                break
            c5_final += line + " "
        c5 = c5_final.strip()

        q_text = re.sub(r'\s+', ' ', q_text)
        c1 = re.sub(r'\s+', ' ', c1)
        c2 = re.sub(r'\s+', ' ', c2)
        c3 = re.sub(r'\s+', ' ', c3)
        c4 = re.sub(r'\s+', ' ', c4)
        c5 = re.sub(r'\s+', ' ', c5)
        
        qs[q_num] = {
            "question": q_text,
            "choices": [c1, c2, c3, c4, c5]
        }
    return qs

def parse_answers(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
        
    ans_map = {}
    lines = text.split('\n')
    
    # strictly a-z or 0-9 ascii digits
    # "1" -> match, "①" -> no match
    nums = [int(l.strip()) for l in lines if re.match(r'^\d+$', l.strip())]
    
    for idx_1 in range(len(nums)):
        if nums[idx_1] == 1:
            try:
                # the table goes: q_num, ans, q_num, ans. 
                # e.g., 1, 3, 2, 2, 3, 5, 4, 3, 5, 3
                # Or it goes column by column: 1..25, 26..50... and answers? No, test_pdf output showed interleaved:
                # 1교시 \n 기초간호학개요 \n 1 \n 3 \n 1교시 \n 기초간호학개요 \n 2 \n 2 \n
                # Let's search for sequence of 1,2,3 up to at least 10 in alternating spots
                valid = True
                for step in range(10):
                    pos = idx_1 + step*2
                    if pos >= len(nums) or nums[pos] != step+1:
                        valid = False
                        break
                
                if valid:
                    # we found it
                    for q in range(1, 101):
                        pos = idx_1 + (q-1)*2
                        if pos+1 < len(nums):
                            ans_map[nums[pos]] = nums[pos+1]
                    break
            except IndexError:
                pass
                
    if not ans_map:
        # Fallback if answer key is simply listed as 1~100 sequentially and then 100 answers? No.
        # Let's see if there's a different sequence: answers might be inline
        pass
                
    return ans_map

pairs = [
    ("2021년도_상반기_간호조무사_국가시험_짝수형.pdf", "2021년도_상반기_간호조무사_국가시험_가답안_짝수형.pdf"),
    ("2021년도_하반기_간호조무사_국가시험_문제지.pdf", "2021년도_하반기_간호조무사_국가시험_가답안.pdf"),
    ("2022년도 상반기 간호조무사 국가시험 문제지(짝수형).pdf", "2022년도 상반기 간호조무사 국가시험 가답안(짝수형).pdf"),
    ("2022년도 상반기 간호조무사 국가시험 문제지(홀수형).pdf", "2022년도 상반기 간호조무사 국가시험 가답안(홀수형).pdf"),
    ("2022년도_하반기_간호조무사_국가시험_짝수형_문제지.pdf", "2022년도_하반기_간호조무사_국가시험_가답안_짝수형.pdf"),
    ("2023년도_하반기_간호조무사_국가시험_짝수형.pdf", "2023년도_하반기_간호조무사_국가시험_가답안_짝수형.pdf"),
    ("2023년도_하반기_간호조무사_국가시험_홀수형.pdf", "2023년도_하반기_간호조무사_국가시험_가답안_홀수형.pdf")
]

base_dir = r"c:\간호조무사\간호조무사_기출문제"

all_new_qs = []

for q_pdf, a_pdf in pairs:
    q_path = f"{base_dir}\\{q_pdf}"
    a_path = f"{base_dir}\\{a_pdf}"
    
    qs = parse_questions(q_path)
    ans = parse_answers(a_path)
    
    print(f"File {q_pdf}: Parsed {len(qs)} questions, matched {len(ans)} answers")
    
    # 2021년도 상반기, 하반기 등 추출 (regex로 연도와 반기)
    match_year = re.search(r'(202\d년도.*?상반기|202\d년도.*?하반기)', q_pdf)
    category_name = match_year.group(1) if match_year else "기출문제"
    
    for q_num, data in qs.items():
        if q_num in ans:
            all_new_qs.append({
                "category": category_name,
                "question": f"[{category_name}] {data['question']}",
                "choices": [f"{i+1}. {c}" for i, c in enumerate(data['choices'])],
                "answer": ans[q_num],
                "explanation": "기출문제 정답입니다. 자세한 해설은 기본서를 참고하세요.",
                "tip": "국가시험 실전 기출"
            })

print(f"Total new valid questions: {len(all_new_qs)}")

# DB 갱신
db_path = r"c:\간호조무사\src\data\questions.json"
with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Keep the original 111 questions
original_data = data[:111]

# Deduplicate
seen = set()
unique_new_qs = []
for q in all_new_qs:
    q_text = q['question']
    if q_text not in seen:
        seen.add(q_text)
        unique_new_qs.append(q)

final_db = original_data + unique_new_qs

for i, q in enumerate(final_db):
    q['id'] = i + 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"DB updated successfully! Total questions now: {len(final_db)}")
