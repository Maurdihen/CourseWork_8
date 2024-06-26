import json
from api.hh_api import HeadHunterAPI
from db.create_table import create_tables
from db.insert_db import insert_data


def main() -> None:
    """
    Main function to fetch company data from HeadHunter API, save it to a JSON file,
    create the necessary database tables, and insert the data into the database.

    The function performs the following steps:
    1. Fetches company data from the HeadHunter API.
    2. Saves the fetched data to a JSON file.
    3. Creates the 'employers' and 'vacancies' tables in the database.
    4. Inserts the data from the JSON file into the database.

    Returns:
        None
    """
    url: str = "https://api.hh.ru/employers"
    hh_api: HeadHunterAPI = HeadHunterAPI(url)
    companies: dict = hh_api.get_data({'cnt_employers': 50, "search_text": ""})

    with open('companies.json', 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False)

    create_tables()
    insert_data()


if __name__ == "__main__":
    main()
