import streamlit as st
import sqlite3
import hashlib

# Вспомогательная функция для хеширования паролей
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Создание базы данных
def create_database():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

create_database()

# Функция для добавления пользователя в базу данных
def add_user(username, hashed_password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Функция для проверки аутентификации пользователя
def check_credentials(username, hashed_password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    result = c.fetchone()
    conn.close()
    return result is not None

# Функция для отображения формы входа
def login():
    st.sidebar.subheader('Вход')
    username = st.sidebar.text_input('Имя пользователя')
    password = st.sidebar.text_input('Пароль', type='password')
    if st.sidebar.button('Войти'):
        hashed_password = hash_password(password)
        if check_credentials(username, hashed_password):
            st.session_state['username'] = username
            st.sidebar.success('Успешный вход!')
        else:
            st.sidebar.error('Неверное имя пользователя или пароль.')

# Функция для отображения формы регистрации
def registration():
    st.sidebar.subheader('Регистрация')
    new_username = st.sidebar.text_input('Новое имя пользователя')
    new_password = st.sidebar.text_input('Новый пароль', type='password')
    if st.sidebar.button('Зарегистрироваться'):
        if new_username and new_password:
            hashed_password = hash_password(new_password)
            try:
                add_user(new_username, hashed_password)
                st.sidebar.success('Регистрация прошла успешно!')
            except sqlite3.IntegrityError:
                st.sidebar.error('Такое имя пользователя уже существует.')
        else:
            st.sidebar.error('Имя пользователя и пароль не могут быть пустыми.')

# Функция для отображения основной платформы
def main_platform():
    st.title('Добро пожаловать в приложение!')
    # Здесь будет функционал основной платформы (чат, загрузка файлов, поиск литературы)
    # Помести сюда логику для инструментов, как ты описал в функционале после регистрации

# Проверка аутентификации пользователя
if 'username' not in st.session_state:
    registration()
    login()
else:
    main_platform()
