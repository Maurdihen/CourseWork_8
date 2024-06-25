from db.connection import connect_db


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                id_employer INT UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL
            );
        """)

    cursor.execute("""
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

    cursor.close()
    conn.close()
