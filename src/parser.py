import requests
import json
import os
from models import Vacancy

def fetch_vacancies(query: str, area_id: int, pages=3):
    """Листает страницы и собирает вакансии"""
    all_results = []
    url = "https://api.hh.ru/vacancies"
    
    for page in range(pages):
        params = {
            "text": query,
            "area": area_id,
            "page": page,
            "per_page": 100, # максимум для одной страницы
            "search_field": "name" 
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            items = response.json().get('items', [])
            if not items:
                break
            for item in items:
                all_results.append(Vacancy(
                    id=item['id'],
                    name=item['name'],
                    area_name=item['area']['name'],
                    salary_from=item['salary']['from'] if item.get('salary') else None,
                    salary_to=item['salary']['to'] if item.get('salary') else None,
                    alternate_url=item['alternate_url']
                ))
        else:
            break
            
    return all_results

def update_local_db(new_vacancies):
    """Добавляет только новые вакансии в файл, избегая дублей"""
    file_path = 'data/raw_data.json'
    
    # 1. загружаем старые данные
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                old_data = json.load(f)
            except:
                old_data = []
    else:
        old_data = []

    # 2. объединяем по ID (чтобы не было повторов)
    existing_ids = {v['id'] for v in old_data}
    added_count = 0
    
    for v in new_vacancies:
        if v.id not in existing_ids:
            old_data.append(v.model_dump())
            existing_ids.add(v.id)
            added_count += 1
            
    # 3. сохраняем
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(old_data, f, ensure_ascii=False, indent=4)
    
    print(f"✨ Готово! Добавлено новых вакансий: {added_count}. Всего в базе: {len(old_data)}")