import streamlit as st
from parser import fetch_vacancies, update_local_db

st.title("HH.ru Parser Control Panel")

if st.button("Обновить базу вакансий"):
    with st.spinner('Собираю данные...'):
        # для теста беру Москву (ID=1)
        news = fetch_vacancies("Python", 1)
        update_local_db(news)
        st.success(f"База обновлена! Найдено {len(news)} вакансий.")