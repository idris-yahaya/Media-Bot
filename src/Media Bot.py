import requests
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

def main():
    configure()
    os.getenv('api_key')

NOTION_TOKEN = ""
DATABASE_ID = "YOUR_DATABASE_ID"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2023-11-07",
}

main()
print("IT WORKED")
print(os.getenv('NOTION_KEY'))
print(os.getenv('NOTION_PAGE_ID'))
