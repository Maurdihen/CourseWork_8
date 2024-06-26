from db.connection import connect_db
from psycopg2.extensions import connection, cursor


def create_tables() -> None:
    """
    Creates the 'employers' and 'vacancies' tables in the database if they do not already exist.

    The 'employers' table includes:
        - id (SERIAL PRIMARY KEY)
        - id_employer (INT UNIQUE NOT NULL)
        - name (VARCHAR(255) NOT NULL)

    The 'vacancies' table includes:
        - id (SERIAL PRIMARY KEY)
        - id_employer (INT NOT NULL, FOREIGN KEY references employers(id_employer) ON DELETE CASCADE)
        - address (VARCHAR(255))
        - employment (VARCHAR(255))
        - experience (VARCHAR(255))
        - name (VARCHAR(255))
        - currency (VARCHAR(255))
        - salary_from (INT)
        - salary_to (INT)

    Returns:
        None
    """
    conn: connection = connect_db()
    cur: cursor = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id SERIAL PRIMARY KEY,
            id_employer INT UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            id_employer INT NOT NULL,
            address VARCHAR(255),
            employment VARCHAR(255),
            experience VARCHAR(255),
            name VARCHAR(255),
            currency VARCHAR(255),
            salary_from INT,
            salary_to INT,
            FOREIGN KEY (id_employer) REFERENCES employers(id_employer) ON DELETE CASCADE
        );
    """)

    conn.commit()

    cur.close()
    conn.close()
