from flask import Flask, render_template, request, jsonify
import json
import os
# импорт функций
from parser import fetch_vacancies

app = Flask(__name__)

# путь к базе данных JSON
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data.json')

@app.route('/')
def index():
    # загружаем вакансии из JSON, чтобы показать их на главной
    vacancies = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            vacancies = json.load(f)
    
    return render_template('index.html', vacancies=vacancies)

@app.route('/update', methods=['POST'])
def update_db():
    # вызываем парсер
    new_data = fetch_vacancies("Python", "47") 
    
    # возвращаем JSON, чтобы JS на фронте понял, что все ок
    return jsonify({"status": "success", "count": len(new_data)})

if __name__ == '__main__':
    app.run(debug=True)