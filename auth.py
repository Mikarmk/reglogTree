import streamlit as st
import hashlib
import sqlite3

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

# Формы регистрации и входа
def auth_forms():
    create_database()  # убедитесь, что база данных создается
    with st.sidebar:
        if 'username' not in st.session_state:
            # Формы регистрации и входа
            st.subheader('Регистрация')
            new_username = st.text_input('Новое имя пользователя')
            new_password = st.text_input('Новый пароль', type='password')
            if st.button('Зарегистрироваться'):
                if new_username and new_password:
                    hashed_password = hash_password(new_password)
                    try:
                        add_user(new_username, hashed_password)
                        st.success('Регистрация прошла успешно!')
                    except sqlite3.IntegrityError:
                        st.error('Такое имя пользователя уже существует.')
                else:
                    st.error('Имя пользователя и пароль не могут быть пустыми.')

            st.subheader('Вход')
            username = st.text_input('Имя пользователя', key='login_user')
            password = st.text_input('Пароль', type='password', key='login_pass')
            if st.button('Войти'):
                hashed_password = hash_password(password)
                if check_credentials(username, hashed_password):
                    st.session_state['username'] = username
                    st.success('Успешный вход!')
                else:
                    st.error('Неверное имя пользователя или пароль.')
            return False  # пользователь не прошел аутентификацию
        else:
            # пользователь вошел в систему
            st.write(f'Добро пожаловать, {st.session_state.username}!')
            if st.button('Выйти'):
                del st.session_state['username']
            return True  # пользователь прошел аутентификацию
