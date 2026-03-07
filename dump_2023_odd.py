import fitz
import sys

pdf_path = r"c:\간호조무사\간호조무사_기출문제\2023년도_하반기_간호조무사_국가시험_홀수형.pdf"
doc = fitz.open(pdf_path)
print(doc[0].get_text("text")[:2000])
