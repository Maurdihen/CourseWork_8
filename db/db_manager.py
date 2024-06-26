from psycopg2.extensions import connection, cursor
from typing import List, Tuple, Any


class DBManager:
    def __init__(self, conn: connection) -> None:
        """
        Initializes the DBManager with a database connection.

        Args:
            conn (connection): A connection object to the PostgreSQL database.
        """
        self.connection: connection = conn
        self.connection.autocommit = True
        self.cursor: cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Retrieves the number of vacancies for each company.

        Returns:
            List[Tuple[str, int]]: A list of tuples where each tuple contains the company name and the count of vacancies.
        """
        query = """
        SELECT e.name, COUNT(v.id) as vacancies_count
        FROM employers e
        LEFT JOIN vacancies v ON e.id_employer = v.id_employer
        GROUP BY e.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], Optional[str]]]:
        """
        Retrieves all vacancies with their details.

        Returns:
            List[Tuple[str, str, Optional[int], Optional[int], Optional[str]]]: A list of tuples where each tuple contains
            the company name, vacancy name, salary range, and currency.
        """
        query = """
        SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency
        FROM vacancies v
        JOIN employers e ON v.id_employer = e.id_employer;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Calculates the average salary across all vacancies.

        Returns:
            Optional[float]: The average salary, or None if there are no salaries to average.
        """
        query = """
        SELECT AVG((v.salary_from + v.salary_to) / 2) as avg_salary
        FROM vacancies v;
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[int], Optional[int], Optional[str]]]:
        """
        Retrieves vacancies with a salary higher than the average salary.

        Returns:
            List[Tuple[str, str, Optional[int], Optional[int], Optional[str]]]: A list of tuples where each tuple contains
            the company name, vacancy name, salary range, and currency for vacancies with a higher than average salary.
        """
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        query = """
        SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency
        FROM vacancies v
        JOIN employers e ON v.id_employer = e.id_employer
        WHERE (v.salary_from + v.salary_to) / 2 > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[
        Tuple[str, str, Optional[int], Optional[int], Optional[str]]]:
        """
        Retrieves vacancies that contain the specified keyword in their name.

        Args:
            keyword (str): The keyword to search for in vacancy names.

        Returns:
            List[Tuple[str, str, Optional[int], Optional[int], Optional[str]]]: A list of tuples where each tuple contains
            the company name, vacancy name, salary range, and currency for vacancies that match the keyword.
        """
        query = """
        SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency
        FROM vacancies v
        JOIN employers e ON v.id_employer = e.id_employer
        WHERE v.name ILIKE %s;
        """
        self.cursor.execute(query, (f'%{keyword}%',))
        return self.cursor.fetchall()

    def __del__(self) -> None:
        """
        Closes the cursor and the connection when the DBManager is deleted.
        """
        self.cursor.close()
        self.connection.close()
