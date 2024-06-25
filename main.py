import json

from api.hh_api import HeadHunterAPI
from db.create_table import create_tables
from db.insert_db import insert_data

if __name__ == "__main__":
    url = "https://api.hh.ru/employers"
    hh_api = HeadHunterAPI(url)
    companies = hh_api.get_data({'cnt_employers': 100, "search_text": ""})

    with open('companies.json', 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False)

    create_tables()
    insert_data()