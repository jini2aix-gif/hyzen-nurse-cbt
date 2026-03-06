
import json
import random

def generate_db():
    categories = [
        {"name": "기초간호학 개요", "total": 105}, # 35 * 3
        {"name": "보건간호학 개요", "total": 45},  # 15 * 3
        {"name": "공중보건학 개요", "total": 60},  # 20 * 3
        {"name": "실기", "total": 105},           # 35 * 3
    ]
    
    questions = []
    
    # 1. 기초간호학 개요 (Basic Nursing) - 105 questions
    for i in range(1, 106):
        topic = random.choice(["활력징후", "감염관리", "해부생리", "약리", "영양", "치과", "한방", "모성", "아동", "노인", "응급"])
        q = {
            "id": f"basic_{i}",
            "category": "기초간호학 개요",
            "question": f"({topic}) 간호조무사의 기본 역할에 대한 다음 설명 중 옳은 것은? (예시 문제 {i})",
            "choices": ["1. 환자의 진단을 직접 내린다.", "2. 의사의 지시 없이 약물을 투여한다.", "3. 환자의 사생활을 다른 사람에게 누설한다.", "4. 물품의 파손이나 이상을 발견하면 즉시 보고한다.", "5. 모든 의료 행위를 독단적으로 수행한다."],
            "answer": 4,
            "explanation": "간호조무사는 의료진의 지시에 따라 업무를 수행하며, 시설 및 물품 관리에 주의를 기울여야 합니다. 이상 발견 시 즉시 보고하는 것이 원칙입니다. 🏥",
            "tip": "보고는 기지(기초 중의 기초)! 이상하면 무조건 보고하세요! ✨"
        }
        # Actually I will fill in real questions for the first 105 at least.
        # For the sake of this task, I'll provide a set of REAL high-quality questions for the first 105.
        questions.append(q)

    # ... (I'll refine the actual question content in the next step to be HIGH QUALITY)
    
    # Let's actually write a more structured content for the first 105.
    
    with open('src/data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # In reality, I will manually curate the first 105 questions to be high quality as a veteran.
    # The user wants 315 questions. I'll provide a dummy generator here but then I'll overwrite with real content chunk by chunk or use a more robust way.
    pass
