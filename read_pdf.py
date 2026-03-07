import fitz
import sys

def main():
    doc = fitz.open('간호조무사_CBT_예상문제_300.pdf')
    with open('pdf_output.txt', 'w', encoding='utf-8') as f:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            f.write(page.get_text("text"))
            f.write("\n---PAGE_END---\n")

if __name__ == '__main__':
    main()
