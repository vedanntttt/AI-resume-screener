import zipfile
import xml.etree.ElementTree as ET
import sys

def extract_text(docx_path):
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    text = []
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        for p in tree.findall('.//w:p', ns):
            p_text = ''.join(node.text for node in p.findall('.//w:t', ns) if node.text)
            if p_text:
                text.append(p_text)
    return '\n'.join(text)

if __name__ == '__main__':
    with open('parsed_doc.txt', 'w', encoding='utf-8') as f:
        f.write(extract_text(sys.argv[1]))
