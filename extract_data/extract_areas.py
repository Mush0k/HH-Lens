import requests
import json

def get_clean_areas():
    print("Загрузка данных из HH API...")
    url = "https://api.hh.ru/areas"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return

    flat_list = []

    # рекурсивная функция для прохода по всем уровням
    def parse_item(items):
        for item in items:
            # забираем только нужное
            flat_list.append({
                "id": item['id'],
                "name": item['name']
            })
            
            # если есть вложенные области, идем внутрь них
            if item.get('areas'):
                parse_item(item['areas'])

    print("Распаковываю дерево регионов...")
    parse_item(data)

    # сохраняем результат в файл, чтобы не дергать API лишний раз
    with open('areas.json', 'w', encoding='utf-8') as f:
        json.dump(flat_list, f, ensure_ascii=False, indent=4)
    
    print(f"Готово! Сохранено {len(flat_list)} локаций в файл areas.json")

if __name__ == "__main__":
    get_clean_areas()