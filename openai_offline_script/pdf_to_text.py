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


pdf_path = "C:\@code\course_chatbot_app\main_notes.pdf"
content = pdf_to_text(pdf_path, content)
print(len(content))
# save content to jsn file

with open('content.json', 'w') as f:
    json.dump(content, f)
