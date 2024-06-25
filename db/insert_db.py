import json

from db.connection import connect_db
from psycopg2 import errors


def insert_employer(id_employer, name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO employers (id_employer, name)
            VALUES (%s, %s) RETURNING id_employer;
        """, (id_employer, name))
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def insert_vacancy(id_employer, address, employment, experience, name, currency, salary_from, salary_to):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO vacancies (id_employer, address, employment, experience, name, currency, salary_from, salary_to)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (id_employer, address, employment, experience, name, currency, salary_from, salary_to))
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_data():
    with open("./companies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for employer, vacancies in data.items():
            insert_employer(int(list(employer.split("%^"))[1]), list(employer.split("%^"))[0])
            if len(vacancies) > 0:
                for vacancy in vacancies:
                    salary_currency = vacancy["salary"]["currency"] if vacancy.get("salary") else None
                    salary_from = vacancy["salary"]["from"] if vacancy.get("salary") else None
                    salary_to = vacancy["salary"]["to"] if vacancy.get("salary") else None

                    insert_vacancy(int(list(employer.split("%^"))[1]),
                                   vacancy["area"]["name"],
                                   vacancy["employment"]["name"],
                                   vacancy["experience"]["name"],
                                   vacancy["name"],
                                   salary_currency,
                                   salary_from,
                                   salary_to)
