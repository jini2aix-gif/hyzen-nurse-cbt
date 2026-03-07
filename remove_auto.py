import json
import re

db_path = r"c:\간호조무사\src\data\questions.json"

with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

# AI가 생성한 문제(변형, 사례형, 최신 빈출 코어 등)를 모두 제거하고
# 순수하게 PDF 기출문제 폴더에서 추출한 문제(category가 "기출문제"로 시작)만 남깁니다.
pure_db = [q for q in db if q.get("category", "").startswith("기출문제")]

# Remove any prefix like "[1번]" that AI might have added to the question text
for q in pure_db:
    q["question"] = re.sub(r'^\[\d+번\]\s*', '', q["question"])

# Re-index the IDs perfectly
for i, q in enumerate(pure_db):
    q["id"] = i + 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(pure_db, f, ensure_ascii=False, indent=2)

print(f"Total pure questions remaining: {len(pure_db)}")
