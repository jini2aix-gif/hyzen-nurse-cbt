import fitz
import sys
import glob
import re

pdf = r"c:\간호조무사\간호조무사_기출문제\2021년도_하반기_간호조무사_국가시험_문제지.pdf"
doc = fitz.open(pdf)
text = ""
for page in doc:
    text += page.get_text("text")

# Print a chunk showing some questions
match = re.search(r'1\.\s*.*?\n①.*?\n⑤.*?\n', text, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Pattern not found. Printing first 1000 characters:")
    print(text[:1000])
