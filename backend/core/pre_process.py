# pre-proccess the raw data from the crawler
import json
import re

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "raw.json"

def get_data():
    with open(JSON_PATH, "r") as f:
        data = json.load(f)
    return data

def pre_process_pages(data):
    '''
    DATA TO EXTRACT FOR PAGES:
    url
    title
    main_heading
    headings
    category
    department
    content
    attachments
    '''
    pages = data.get("pages", [])
    if not pages:
        return []
    processed_data = []
    for page in pages:
        processed_page = {
            "url": page.get("url", ""),
            "title": page.get("title", ""),
            "main_heading": page.get("main_heading", ""),
            "headings": page.get("headings", []),
            "category": page.get("category", ""),
            "department": page.get("department", ""),
            "content": page.get("content", ""),
            "attachments": page.get("attachments", []),
        }
        processed_data.append(processed_page)

    return processed_data

def pre_process_docs(data):
    ''''
    DATA TO EXTRACT FOR DOCS:
    url
    type
    title
    link_texts
    category
    found_on
    content
    '''
    docs = data.get("documents", [])
    if not docs:
        return []
    processed_data = []
    for doc in docs:
        processed_doc = {
            "url": doc.get("url", ""),
            "type": doc.get("type", ""),
            "title": doc.get("title", ""),
            "link_texts": doc.get("link_texts", []),
            "category": doc.get("category", ""),
            "found_on": doc.get("found_on", []),
            "content": doc.get("content", ""),
        }
        processed_data.append(processed_doc)
    return processed_data

def clean_text(text: str) -> str:
    # 1. Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 2. Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # 3. Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 4. Remove meaningless repeated characters
    # e.g. "---------" -> "-"
    #      "_________" -> "_"
    #      ".........." -> "."
    text = re.sub(r"([^\w\s])\1{3,}", r"\1", text)

    return text.strip()
  
def clean_data_content(data):
    for page in data.get("pages", []):
        page["content"] = clean_text(page.get("content", ""))
    for doc in data.get("documents", []):
        
        for content in doc.get("content", []):
            content["text"] = clean_text(content.get("text", ""))
    return data  

def write_processed_data(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    data = get_data()
    processed_pages = pre_process_pages(data)
    processed_docs = pre_process_docs(data)
    processed_data = {
        "source": "https://www.gecg28.ac.in/",
        "pages": processed_pages,
        "documents": processed_docs
    }
    processed_data = clean_data_content(processed_data)
    output_path = BASE_DIR / "data" / "processed.json"
    write_processed_data(processed_data, output_path)

if __name__ == "__main__":
    main()
    