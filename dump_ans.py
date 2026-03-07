import fitz

pdf_path = r"c:\간호조무사\간호조무사_기출문제\2021년도_하반기_간호조무사_국가시험_가답안.pdf"
doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text("text")

with open(r"c:\간호조무사\ans_test_2021_2.txt", "w", encoding="utf-8") as f:
    f.write(text)

pdf_path2 = r"c:\간호조무사\간호조무사_기출문제\2023년도_하반기_간호조무사_국가시험_가답안_짝수형.pdf"
doc2 = fitz.open(pdf_path2)
text2 = ""
for page in doc2:
    text2 += page.get_text("text")

with open(r"c:\간호조무사\ans_test_2023_2.txt", "w", encoding="utf-8") as f:
    f.write(text2)
