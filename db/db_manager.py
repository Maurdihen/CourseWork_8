class DBManager:
    def __init__(self, conn):
        self.connection = conn
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        query = """
        SELECT e.name, COUNT(v.id) as vacancies_count
        FROM employers e
        LEFT JOIN vacancies v ON e.id_employer = v.id_employer
        GROUP BY e.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        query = """
        SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency
        FROM vacancies v
        JOIN employers e ON v.id_employer = e.id_employer;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        query = """
        SELECT AVG((v.salary_from + v.salary_to) / 2) as avg_salary
        FROM vacancies v;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        query = """
        SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency
        FROM vacancies v
        JOIN employers e ON v.id_employer = e.id_employer
        WHERE (v.salary_from + v.salary_to) / 2 > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        query = """
        SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency
        FROM vacancies v
        JOIN employers e ON v.id_employer = e.id_employer
        WHERE v.name ILIKE %s;
        """
        self.cursor.execute(query, (f'%{keyword}%',))
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()