import asyncio
from src.database import DatabaseManager
from src.api import HeadHunterApi
from src.parser import SmartCollector

async def main():
    # 1. Инициализируем всё по цепочке
    db = DatabaseManager()
    api = HeadHunterApi()
    collector = SmartCollector(db, api)

    print("--- ТЕСТОВЫЙ ЗАПУСК ---")
    
    # 2. Пробуем собрать вакансии (например, Ижевск, Аналитика, за 1 день)
    # Эти названия должны быть в твоих JSON-файлах!
    await collector.collect_by_params(
        city_name="Санкт-Петербург", 
        sector_name="Аналитика", 
        period_days=3
    )
    
    print("--- ТЕСТ ЗАВЕРШЕН ---")
    
    # 3. Проверим, появилось ли что-то в базе
    data = db.get_all()
    print(f"В базе сейчас записей: {len(data)}")
    if data:
        print(f"Последняя добавленная: {data[-1][1]}") # Печатаем название вакансии

if __name__ == "__main__":
    asyncio.run(main())