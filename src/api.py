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
            "professional_role": professional_role, # Передаем список ролей
            "date_from": date_from,
            "date_to": date_to,
            "per_page": 100,
            "order_by": "publication_time"
        }

        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                # Важно: для списков (roles) httpx иногда требует особой обработки
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 400:
                    # Если всё еще 400, давай выведем причину (HH пишет её в JSON)
                    print(f"❌ Детали ошибки 400: {response.text}")
                    return []

                items = response.json().get('items', [])
                
                # Превращаем сырой ответ от HH в список наших объектов Vacancy
                valid_vacancies = []
                for item in items:
                    # Проверяем зарплату (она может быть None)
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
                print(f"⚠️ Проблема при запросе к HH: {e}")
                return []