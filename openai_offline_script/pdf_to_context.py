import PyPDF2
import json
import os
content = {}


def pdf_to_text(pdf_path, content):
    file_name = pdf_path.split('\\')[-1]
    page_text = []
    pdf_file = open(pdf_path, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    print(number_of_pages)
    for x in range(number_of_pages):
        page = read_pdf.getPage(x)
        page_content = page.extractText()
        page_content = page_content.replace('\n', ' ')
        page_content = page_content.replace('  ', ' ')
        page_content = page_content.replace('  ', ' ')
        page_content = page_content.replace('  ', ' ')
        page_content = page_content.replace('  ', ' ')
        page_content = page_content.replace('  ', ' ')
        page_content = page_content.strip()
        if len(page_content) == 0:
            continue
        page_text.append({"page_number": x, "text": page_content})
        print("page_index :", x, "page_content len:", len(page_content))
    content[file_name] = page_text
    return content


def txt_to_text(txt_path, content):
    file_name = txt_path.split('\\')[-1]
    page_text = []
    txt_file = open(txt_path, 'r', encoding='utf-8', errors='ignore')
    page_content = txt_file.read()
    page_content = page_content.replace('\n', ' ')
    page_content = page_content.strip()
    page_text.append({"page_number": 0, "text": page_content})
    print("page_index :", 0, "page_content len:", len(page_content))
    print(file_name)
    content[file_name] = page_text
    return content


def read_all_txt_files_in_folder(folder_path):
    content_all = {}
    file_list = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            file_list.append(folder_path + file)
    for f in file_list:
        content = {}
        content = txt_to_text(f, content)
        content_all.update(content)
    return content_all


def read_all_pdf_files_in_folder(folder_path):
    content_all = {}
    file_list = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_list.append(folder_path + file)
    for f in file_list:
        content = {}
        content = pdf_to_text(f, content)
        content_all.update(content)
    return content_all


folder_path = "C:\@code\course_chatbot_app\content\\"
# content_all = read_all_txt_files_in_folder(folder_path)
content_all = read_all_pdf_files_in_folder(folder_path)

with open('content.json', 'w') as f:
    json.dump(content_all, f)
