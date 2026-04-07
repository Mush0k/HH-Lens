from flask import Flask, render_template, request, jsonify
from src.database import DatabaseManager
from src.api import HeadHunterApi 
from src.parser import SmartCollector

# 1. Инициализируем Flask. Папка templates должна быть в корне проекта.
app = Flask(__name__) 
db = DatabaseManager()

@app.route('/')
def index():
    #Главная страница: достаем вакансии из БД и отдаем в HTML
    # Вызываем метод, который ты уже проверяла в run_test.py
    all_vacancies = db.get_all() 
    
    # Отправляем данные в шаблон index.html
    return render_template('index.html', vacancies=all_vacancies)

@app.route('/update', methods=['POST'])
async def update_db():
    #Маршрут для запуска парсера прямо из браузера (в будущем)
    data = request.get_json() or {}
    city = data.get("city", "Санкт-Петербург")
    sector = data.get("sector", "Аналитика")
    days = data.get("days", 3)
    
    # Теперь мы можем использовать реальный API, который написали!
    api = HeadHunterApi() 
    collector = SmartCollector(db, api)
    
    # Запускаем сбор данных
    await collector.collect_by_params(city_name=city, sector_name=sector, period_days=days)
    
    return jsonify({"status": "success", "message": f"Обновлено для города {city}"})

if __name__ == '__main__':
    # Запуск сервера
    app.run(debug=True)