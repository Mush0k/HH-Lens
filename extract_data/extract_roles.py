import requests
import json

def get_clean_areas():
    print("Загрузка данных из HH API...")
    url = "https://api.hh.ru/professional_roles"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return

    flat_list = []
    # рекурсивная функция для прохода по всем уровням
    # есть список категорий, в каждой список roles
    for category in data.get('categories', []):
        category_name = category['name']
        for role in category.get('roles', []):
            flat_list.append({
                "id": role['id'],
                "name": role['name'],
                "category": category_name  
            })

    # Сохраняем
    with open('roles.json', 'w', encoding='utf-8') as f:
        json.dump(flat_list, f, ensure_ascii=False, indent=4)
    
    print(f"Готово! Сохранено {len(flat_list)} ролей")

if __name__ == "__main__":
    get_clean_areas()