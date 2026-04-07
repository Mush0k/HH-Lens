import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        # База будет лежать в папке data/
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'vacancies.db')
        self.conn = sqlite3.connect('data/vacancies.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицу, если ее еще нет. id - это PRIMARY KEY (защита от дублей!)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id TEXT PRIMARY KEY,
                name TEXT,
                area_name TEXT,
                salary_from INTEGER,
                salary_to INTEGER,
                experience TEXT,
                requirement TEXT,
                responsibility TEXT,
                alternate_url TEXT
            )
        ''')
        self.conn.commit()

    def save_many(self, vacancies: list):
        # INSERT OR IGNORE - если ID уже есть, он просто пропустит эту вакансию
        query = '''
            INSERT OR IGNORE INTO vacancies 
            (id, name, area_name, salary_from, salary_to, experience, requirement, responsibility, alternate_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        # Превращаем объекты Pydantic в кортежи для базы
        data = [
            (v.id, v.name, v.area_name, v.salary_from, v.salary_to, 
             v.experience, v.requirement, v.responsibility, v.alternate_url) 
            for v in vacancies
        ]
        
        self.cursor.executemany(query, data)
        self.conn.commit()

    def get_all(self):
        # Эта функция пригодится для Фласка, чтобы отдавать данные на фронт
        self.cursor.execute('SELECT * FROM vacancies')
        return self.cursor.fetchall()