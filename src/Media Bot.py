from dotenv import load_dotenv
import requests
import json
import os

#Constants
TOKEN_INDEX = 0
DB_ID_INDEX = 1
HEADERS_INDEX = 2

# Load environment variables and configure Notion API settings.
def configure():
    load_dotenv()
    token = os.getenv('NOTION_KEY')
    db_id = os.getenv('NOTION_DATABASE_ID')

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2023-11-18",
    }

    return [token, db_id, headers]


# Retrieve pages from the Notion database.
def get_pages(configs: list, num_pages=None, export=False):
    url = f"https://api.notion.com/v1/databases/{configs[DB_ID_INDEX]}/query"
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    results = requests.post(url, headers=configs[HEADERS_INDEX], json=payload)
    
    data = results.json()
    pages = data["results"]

    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        results = requests.post(url, headers=configs[HEADERS_INDEX], json=payload)
        data = results.json()
        pages.extend(data["results"])
    
    if export:
        with open('db.json', 'w', encoding='utf8') as f:
            json.dump(pages, f, ensure_ascii=False, indent=4)

    print(f"Request Status Code: {results.status_code}")
    return pages


# Create a page in the Notion database.
def create_page(configs: list, data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": configs[DB_ID_INDEX]}, "properties": data}

    results = requests.post(create_url, headers=configs[HEADERS_INDEX], json=payload)
    print(results.status_code)
    return results


# Update a page in the Notion database.
def update_page(configs: list, page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": data}

    results = requests.patch(url, headers=configs[HEADERS_INDEX], json=payload)
    print(f"Request Status Code: {results.status_code}")
    return results


# Delete a page from the Notion database.
def delete_page(configs: list, page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}

    results = requests.patch(url, headers=configs[HEADERS_INDEX], json=payload)
    print(f"Request Status Code: {results.status_code}")
    return results


if __name__ == "__main__":
    configs = configure()

    # Meta Data
    """
        - Title~
        - Type~
        - Satus
        - Rating
        - Chapters/Episode~
        - Current
        - Cover Image~
        - Link~
    """