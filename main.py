import streamlit as st
from auth import show_registration_form, check_credentials, hash_password

# Функция аутентификации (можно разместить в auth.py)
def show_auth_form():
    with st.sidebar:
        st.subheader("Вход")
        auth_username = st.text_input("Имя пользователя", key="auth_user")
        auth_password = st.text_input("Пароль", type="password", key="auth_pass")
        auth_button = st.button("Войти")

        if auth_button:
            hashed_auth_password = hash_password(auth_password)
            if check_credentials(auth_username, hashed_auth_password):
                st.session_state["username"] = auth_username
                st.success(f"Добро пожаловать, {auth_username}!")
            else:
                st.error("Неверное имя пользователя или пароль.")

def show_main_page():
    st.title("Главная страница")
    # Тут будет основной функционал приложения

if "username" not in st.session_state:
    show_auth_form()  # Показываем форму аутентификации если пользователь не залогинен
    show_registration_form()  # Показываем форму регистрации
else:
    show_main_page()  # Показываем главную страницу
