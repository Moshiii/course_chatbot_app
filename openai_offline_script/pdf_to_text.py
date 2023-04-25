import PyPDF2
import json
content = {}


def pdf_to_text(pdf_path, content):
    file_name = pdf_path.split('\\')[-1]
    page_text = []
    pdf_file = open(pdf_path, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    for x in range(number_of_pages):
        page = read_pdf.getPage(x)
        page_content = page.extractText()
        page_text.append({"page_number": x,"text": page_content})
        print("page_index :", x, "page_content len:", len(page_content))
    content[file_name] = page_text
    return content

def txt_to_text(txt_path, content):
    file_name = txt_path.split('\\')[-1]
    page_text = []
    txt_file = open(txt_path, 'r',encoding='utf-8', errors='ignore')
    page_content = txt_file.read()
    page_text.append({"page_number": 0,"text": page_content})
    print("page_index :", 0, "page_content len:", len(page_content))
    print(file_name)
    content[file_name] = page_text
    return content

pdf_path = "C:\@code\course_chatbot_app\openai_offline_script\main_notes.pdf"
content1 = pdf_to_text(pdf_path, content)

txt_path = "C:\@code\course_chatbot_app\openai_offline_script\syllabus.txt"
content2 = txt_to_text(txt_path, content)

#conbine content
content = {**content1, **content2}


with open('content.json', 'w') as f:
    json.dump(content, f)
