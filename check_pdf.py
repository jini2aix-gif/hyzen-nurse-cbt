import re

def count_unique():
    with open('pdf_output.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(
        r'문제\s+\d+\.\s*(?:\[([^\]]+)\])?\s*(.*?)\n'
        r'①\s*(.*?)\n②\s*(.*?)\n③\s*(.*?)\n④\s*(.*?)\n⑤\s*(.*?)\n'
        r'정답:\s*([①②③④⑤])\s*\n'
        r'해설:\s*(.*?)(?=\n문제\s+\d+\.|\Z)', 
        re.DOTALL
    )
    
    matches = pattern.findall(content)
    
    all_qs = []
    unique_qs = set()
    
    for match in matches:
        q_text = match[1].strip()
        all_qs.append(q_text)
        unique_qs.add(q_text)
        
    print(f"Total questions matching pattern: {len(all_qs)}")
    print(f"Total Unique question texts: {len(unique_qs)}")
    
if __name__ == '__main__':
    count_unique()
