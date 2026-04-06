from flask import Flask, render_template, request, jsonify
from src.database import DatabaseManager
# Временно импортируем заглушку для API, пока не напишем реальную
# from src.api import HeadHunterApi 
from src.parser import SmartCollector

app = Flask(__name__, template_folder='../templates') # Убедись, что папка templates есть!
db = DatabaseManager()

@app.route('/')
def index():
    # Берем все вакансии из базы для главной страницы
    raw_vacancies = db.get_all() 
    # В реальности тут лучше отдавать JSON для фронта или передавать в шаблон
    return render_template('index.html', count=len(raw_vacancies))

@app.route('/update', methods=['POST'])
async def update_db():
    # Получаем данные от пользователя (например, из формы или кнопок на фронте)
    data = request.json
    city = data.get("city", "Санкт-Петербург")
    sector = data.get("sector", "Аналитика")
    days = data.get("days", 7) # По умолчанию неделя
    
    # api = HeadHunterApi() # Эту штуку нам еще предстоит написать
    # collector = SmartCollector(db, api)
    
    # Запускаем сбор (await collector.collect_by_params(city, sector, period_days=days))
    
    return jsonify({"status": "success", "message": f"Сбор данных для {city} запущен!"})

if __name__ == '__main__':
    app.run(debug=True)