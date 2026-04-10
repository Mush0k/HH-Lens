import asyncio
import datetime
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

def load_config(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'configs', filename)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # превращаем список в словарь
        return {item['name']: item['id'] for item in data}

# загружаем словари
CITIES = load_config('areas.json')
TARGET_ROLES = load_config('roles.json')

class SmartCollector:
    def __init__(self, db_manager, api_client):
        self.db = db_manager
        self.api = api_client

    
    async def collect_by_params(self, city_name, sector_id, period_days=30):
    # достаем ID города из словаря
        area_id = CITIES.get(city_name)
    
        role_ids = [sector_id] # API HH ожидает список, даже если роль одна
    
        if not area_id:
            print(f"Ошибка: город '{city_name}' не найден.")
            return

    # Ограничиваем период 30 днями (лимит HH), даже если ввели больше
        safe_days = min(int(period_days), 30)
    
        end_time = datetime.datetime.now()
        start_limit = end_time - datetime.timedelta(days=safe_days)
    
        print(f"Старт: {city_name} (ID: {area_id}) | Роль ID: {sector_id} | Дни: {safe_days}")
        current_end = end_time
        total_saved = 0

        while current_end > start_limit:
            current_start = current_end - datetime.timedelta(hours=12)
            
            vacancies = await self.api.get_vacancies(
                area=area_id,
                professional_role=role_ids,
                date_from=current_start.isoformat(),
                date_to=current_end.isoformat()
            )
            
            if vacancies:
                self.db.save_many(vacancies)
                total_saved += len(vacancies)
                print(f"Найдено {len(vacancies)} (период {current_start.strftime('%H:%M')} - {current_end.strftime('%H:%M')})")
            
            current_end = current_start
            await asyncio.sleep(0.5)
            
        print(f"Сбор завершен! Всего обработано вакансий: {total_saved}")