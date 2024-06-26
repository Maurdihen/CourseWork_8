from typing import Dict, Any, List, Optional
import requests


class HeadHunterAPI:
    def __init__(self, url: str) -> None:
        """
        Initializes the HeadHunterAPI with the given URL.

        Args:
            url (str): The base URL for the HeadHunter API (e.g., https://api.hh.ru/employers).
        """
        self.url = url
        self.id_employers: List[str] = []

    def _get_employers_id(self, cnt_employers: int, search_text: str = "") -> None:
        """
        Retrieves the IDs of the employers based on the given count and search text.

        Args:
            cnt_employers (int): The number of employers to retrieve.
            search_text (str): The search text to filter employers (default is an empty string).
        """
        response = requests.get(self.url, params={'per_page': cnt_employers, 'text': search_text})
        response.raise_for_status()  # Ensure we raise an exception for bad responses
        for employer in response.json().get("items", []):
            self.id_employers.append(employer["id"])

    def _get_info_employers(self, employer_id: str) -> Dict[str, Any]:
        """
        Retrieves detailed information about a specific employer by their ID.

        Args:
            employer_id (str): The ID of the employer.

        Returns:
            Dict[str, Any]: The detailed information of the employer.
        """
        response = requests.get(f"{self.url}/{employer_id}")
        response.raise_for_status()
        return response.json()

    def _get_company_vacancies(self, vacancy_url: str) -> Dict[str, Any]:
        """
        Retrieves the vacancies of a specific company.

        Args:
            vacancy_url (str): The URL to fetch the vacancies for the company.

        Returns:
            Dict[str, Any]: The vacancies of the company.
        """
        response = requests.get(vacancy_url)
        response.raise_for_status()
        return response.json()

    def get_data(self, params: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieves the data for the employers based on the provided parameters.

        Args:
            params (Dict[str, Any]): The parameters for the data retrieval, including:
                - cnt_employers (int): The number of employers to retrieve.
                - search_text (str): The search text to filter employers.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary where the keys are employer identifiers
                                              and the values are lists of vacancies.
        """
        data: Dict[str, List[Dict[str, Any]]] = {}
        cnt_employers: int = params.get("cnt_employers", 10)
        search_text: str = params.get("search_text", "")

        self._get_employers_id(cnt_employers, search_text)

        for id_employer in self.id_employers:
            company = self._get_info_employers(id_employer)
            vacancies = self._get_company_vacancies(company["vacancies_url"]).get("items", [])
            data[company["name"] + "%^" + f"{company['id']}"] = vacancies

        return data

# temp = HeadHunterAPI("https://api.hh.ru/employers")
# print(temp.get_data({"cnt_employers": 10, "search_text": ""}))
