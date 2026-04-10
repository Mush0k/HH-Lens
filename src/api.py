import httpx
from src.models import Vacancy

class HeadHunterApi:
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json',
        }

    async def get_vacancies(self, area, professional_role, date_from, date_to):
        params = {
            "area": area,
            "professional_role": professional_role,
            "date_from": date_from,
            "date_to": date_to,
            "per_page": 100,
            "order_by": "publication_time"
        }

        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                # для списков (roles) httpx иногда требует особой обработки
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 400:
                    # если все еще 400, то выводим причину 
                    print(f"Детали ошибки 400: {response.text}")
                    return []

                items = response.json().get('items', [])
                
                # превращаем сырой ответ от HH в список объектов Vacancy
                valid_vacancies = []
                for item in items:
                    # проверяем зп
                    salary = item.get('salary')
                    
                    v = Vacancy(
                        id=str(item['id']),
                        name=item['name'],
                        area_name=item['area']['name'],
                        salary_from=salary['from'] if salary else None,
                        salary_to=salary['to'] if salary else None,
                        experience=item.get('experience', {}).get('name'),
                        requirement=item.get('snippet', {}).get('requirement'),
                        responsibility=item.get('snippet', {}).get('responsibility'),
                        alternate_url=item['alternate_url']
                    )
                    valid_vacancies.append(v)
                
                return valid_vacancies

            except Exception as e:
                print(f"Проблема при запросе к HH: {e}")
                return []