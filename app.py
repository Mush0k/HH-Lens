import json
import os
from flask import Flask, render_template, request, jsonify
from src.database import DatabaseManager
from src.api import HeadHunterApi 
from src.parser import SmartCollector

app = Flask(__name__) 
db = DatabaseManager()

# Функция для загрузки справочников
def load_config(filename):
    path = os.path.join('configs', filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    all_vacancies = db.get_all() 
    
    # загружаем списки
    areas = load_config('areas.json')
    roles = load_config('roles.json')
    
    # сроки для поиска 
    periods = [
        (1, "За 24 часа"),
        (7, "За неделю"),
        (30, "За месяц")
    ]
    
    return render_template('index.html', 
                           vacancies=all_vacancies, 
                           areas=areas, 
                           roles=roles, 
                           periods=periods)

@app.route('/update', methods=['POST'])
async def update_db():
    data = request.get_json() or {}
    city = data.get("city")     
    role_id = data.get("role_id") 
    days = data.get("days", 30)

    api = HeadHunterApi() 
    collector = SmartCollector(db, api)
    
    await collector.collect_by_params(
        city_name=city, 
        sector_id=role_id,
        period_days=days
    )
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Сервер HH-Lens запускается на http://127.0.0.1:5000")
    app.run(debug=True)