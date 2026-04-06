import asyncio
import datetime
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

# Вспомогательная функция для загрузки твоих json-конфигов
def load_config(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'configs', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Загружаем словари
CITIES = load_config('areas.json')
TARGET_ROLES = load_config('roles.json')

class SmartCollector:
    def __init__(self, db_manager, api_client):
        self.db = db_manager
        self.api = api_client

    async def collect_by_params(self, city_name, sector_name, period_days=30):
        area_id = CITIES.get(city_name)
        role_ids = TARGET_ROLES.get(sector_name)
        
        if not area_id or not role_ids:
            print(f"❌ Ошибка: город '{city_name}' или сфера '{sector_name}' не найдены в конфигах.")
            return

        end_time = datetime.datetime.now()
        start_limit = end_time - datetime.timedelta(days=period_days)
        
        print(f"🚀 Старт выгрузки: {city_name} | {sector_name} | глубина: {period_days} дн.")

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
                print(f"✅ Найдено {len(vacancies)} (период {current_start.strftime('%H:%M')} - {current_end.strftime('%H:%M')})")
            
            current_end = current_start
            await asyncio.sleep(0.5)
            
        print(f"🎉 Сбор завершен! Всего обработано вакансий: {total_saved}")