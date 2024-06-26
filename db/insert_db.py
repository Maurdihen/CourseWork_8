import json
from typing import Optional
from psycopg2 import errors
from psycopg2.extensions import connection, cursor
from db.connection import connect_db


def insert_employer(id_employer: int, name: str) -> None:
    """
    Inserts a new employer into the employers table.

    Args:
        id_employer (int): The employer's ID.
        name (str): The employer's name.

    Returns:
        None
    """
    conn: connection = connect_db()
    cur: cursor = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO employers (id_employer, name)
            VALUES (%s, %s) RETURNING id_employer;
        """, (id_employer, name))
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_vacancy(id_employer: int, address: Optional[str], employment: Optional[str],
                   experience: Optional[str], name: str, currency: Optional[str],
                   salary_from: Optional[int], salary_to: Optional[int]) -> None:
    """
    Inserts a new vacancy into the vacancies table.

    Args:
        id_employer (int): The employer's ID.
        address (Optional[str]): The address of the vacancy.
        employment (Optional[str]): The employment type.
        experience (Optional[str]): The required experience level.
        name (str): The vacancy name.
        currency (Optional[str]): The salary currency.
        salary_from (Optional[int]): The starting salary.
        salary_to (Optional[int]): The ending salary.

    Returns:
        None
    """
    conn: connection = connect_db()
    cur: cursor = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO vacancies (id_employer, address, employment, experience, name, currency, salary_from, salary_to)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (id_employer, address, employment, experience, name, currency, salary_from, salary_to))
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_data() -> None:
    """
    Reads company and vacancy data from a JSON file and inserts it into the database.

    The JSON file should contain a dictionary where keys are employer identifiers and values are lists of vacancies.
    Each employer identifier is a string formatted as "name%^id".

    Returns:
        None
    """
    with open("./companies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for employer, vacancies in data.items():
            insert_employer(int(list(employer.split("%^"))[1]), list(employer.split("%^"))[0])
            if len(vacancies) > 0:
                for vacancy in vacancies:
                    salary_currency = vacancy["salary"]["currency"] if vacancy.get("salary") else None
                    salary_from = vacancy["salary"]["from"] if vacancy.get("salary") else None
                    salary_to = vacancy["salary"]["to"] if vacancy.get("salary") else None

                    insert_vacancy(
                        int(list(employer.split("%^"))[1]),
                        vacancy["area"]["name"],
                        vacancy["employment"]["name"],
                        vacancy["experience"]["name"],
                        vacancy["name"],
                        salary_currency,
                        salary_from,
                        salary_to
                    )
