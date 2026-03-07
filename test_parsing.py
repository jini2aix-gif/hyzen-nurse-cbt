import extract_exams

base_dir = r"c:\간호조무사\간호조무사_기출문제"
for q_pdf, a_pdf in extract_exams.pairs:
    q_path = f"{base_dir}\\{q_pdf}"
    a_path = f"{base_dir}\\{a_pdf}"
    
    qs = extract_exams.parse_questions(q_path)
    ans = extract_exams.parse_answers(a_path)
    print(f"File {q_pdf}: Parsed {len(qs)} questions, matched {len(ans)} answers")

