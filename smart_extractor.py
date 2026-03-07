import fitz
import glob
import re
import json

base_dir = r"c:\간호조무사\간호조무사_기출문제"
pdfs = glob.glob(f"{base_dir}\\*.pdf")

def identify_pdf(path):
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc[:3]: # top 3 pages is enough to identify
            text += page.get_text("text") + "\n"
            
        if "OOPS!" in text or "요청한 파일을 찾을 수 없습니다" in text:
            return "error", "", ""
            
        # extract year and term
        year_match = re.search(r'(20\d\d)년도\s*(상반기|하반기)', text)
        if not year_match:
            year_match = re.search(r'(20\d\d)년도\s*(상반기|하반기)', path)
        
        if not year_match:
            return "unknown", "", ""
            
        year_term = f"{year_match.group(1)} {year_match.group(2)}"
        
        # extract type
        type_match = re.search(r'(홀수형|짝수형)', text)
        if not type_match:
            type_match = re.search(r'(홀수형|짝수형)', path)
        exam_type = type_match.group(1) if type_match else "알수없음"
        
        # question or answer
        if "정답" in text and ("문제번호" in text or "가답안" in text or "교시" in text):
            # Check if this could be just the exam paper mentioning "1교시"? Exam papers usually have lots of "①", "②"
            choices_count = text.count("②")
            if choices_count < 10:
                doc_type = "answer"
            else:
                doc_type = "question"
        elif "국가시험 문제지" in text or text.count("②") > 10:
            doc_type = "question"
        else:
            doc_type = "unknown"
            
        # override from filename if ambiguous
        if doc_type == "unknown":
            if "가답안" in path:
                doc_type = "answer"
            elif "문제지" in path:
                doc_type = "question"
                
        return doc_type, year_term, exam_type
    except Exception as e:
        return "error", "", ""

pdf_info = {}
for p in pdfs:
    dtype, yt, et = identify_pdf(p)
    if dtype == "error":
        continue
    key = f"{yt}_{et}"
    if key not in pdf_info:
        pdf_info[key] = {"question": None, "answer": None}
    pdf_info[key][dtype] = p

print("Identified Pairs:")
for key, data in pdf_info.items():
    print(f"[{key}] Q: {data['question']} | A: {data['answer']}")

# Let's extract them
all_new_qs = []

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
            if "교시" in line or "짝수형" in line or "홀수형" in line or "국가시험" in line:
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
    
    nums = [int(l.strip()) for l in lines if re.match(r'^\d+$', l.strip())]
    
    for idx_1 in range(len(nums)):
        if nums[idx_1] == 1:
            try:
                valid = True
                for step in range(10):
                    pos = idx_1 + step*2
                    if pos >= len(nums) or nums[pos] != step+1:
                        valid = False
                        break
                
                if valid:
                    for q in range(1, 101):
                        pos = idx_1 + (q-1)*2
                        if pos+1 < len(nums):
                            ans_map[nums[pos]] = nums[pos+1]
                    break
            except IndexError:
                pass
                
    # fallback for other answer layouts, e.g., horizontal
    if not ans_map:
        # let's write a loose matcher: we want values from 1 to 5 corresponding to q_num 1 to 100
        # just find sequences of answer numbers
        possible_answers = [x for x in nums if 1 <= x <= 5]
        if len(possible_answers) == 100:
            for q in range(1, 101):
                ans_map[q] = possible_answers[q-1]
                
    return ans_map

for key, data in pdf_info.items():
    if data["question"] and data["answer"]:
        qs = parse_questions(data["question"])
        ans = parse_answers(data["answer"])
        print(f"Extracting {key}: matched {len(qs)} qs, {len(ans)} ans")
        
        for q_num, q_data in qs.items():
            if q_num in ans:
                all_new_qs.append({
                    "category": f"기출문제 ({key.replace('_', ' ')})",
                    "question": f"[{key.replace('_', ' ')}] {q_data['question']}",
                    "choices": [f"{i+1}. {c}" for i, c in enumerate(q_data['choices'])],
                    "answer": ans[q_num],
                    "explanation": "기출문제 정답입니다. 본 웹페이지는 문제 해설 기능을 현재 추가 개발 중입니다.",
                    "tip": "국가시험 실전 기출"
                })

db_path = r"c:\간호조무사\src\data\questions.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

# The user requested: "기존에 있던 문제들에서 너가 생성 된 문제는 다 삭제하고 남기고, 추가로 폴더안(간호조무사_기출문제) 의 문제들을 추가해서 DB 구성해줘."
# We know the first 111 questions are the original ones (core_db). So keep those.
original_data = db[:111]

# Deduplicate new questions
seen = set()
unique_new_qs = []
for q in all_new_qs:
    q_text = q['question']
    if q_text not in seen:
        seen.add(q_text)
        unique_new_qs.append(q)

final_db = original_data + unique_new_qs

# Re-assign ID
for i, q in enumerate(final_db):
    q['id'] = i + 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"Total old original questions kept: {len(original_data)}")
print(f"Total new unique PDF questions added: {len(unique_new_qs)}")
print(f"Total questions generated and saved to DB: {len(final_db)}")
