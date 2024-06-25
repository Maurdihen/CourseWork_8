from typing import Dict, Any

import requests

class HeadHunterAPI:
    def __init__(self, url: str) -> None:
        self.url = url  # https://api.hh.ru/employers
        self.id_employers = []

    def _get_employers_id(self, cnt_employers: int, search_text: str = ""):
        response = requests.get(self.url, params={'per_page': cnt_employers, "text": search_text})
        for employer in response.json()["items"]:
            self.id_employers.append(employer["id"])

    def _get_info_employers(self, employer_id):
        response = requests.get(f"{self.url}/{employer_id}")
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def _get_company_vacancies(self, vacancy_url):
        response = requests.get(vacancy_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_data(self, params: Dict[str, Any] = None):
        data = {}
        self._get_employers_id(params["cnt_employers"], params["search_text"])
        for id_employer in self.id_employers:
            company = self._get_info_employers(id_employer)
            vacancies = self._get_company_vacancies(company["vacancies_url"])["items"]
            data[company["name"] + "%^" + f"{company['id']}"] = vacancies
        return data

#
# temp = HeadHunterAPI("https://api.hh.ru/employers")
#
# print(temp.get_data({"cnt_employers": 10, "search_text": ""}))