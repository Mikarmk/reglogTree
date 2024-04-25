import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Подключение к Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('your_google_sheet_name').sheet1

# Страница регистрации
def registration():
    st.title('Регистрация')
    username = st.text_input('Введите имя пользователя')
    password = st.text_input('Введите пароль', type='password')

    if st.button('Зарегистрироваться'):
        if username in sheet.col_values(1):
            st.error('Пользователь с таким именем уже зарегистрирован')
        else:
            sheet.append_row([username, password])
            st.success('Регистрация прошла успешно')

# Страница авторизации
def login():
    st.title('Авторизация')
    username = st.text_input('Введите имя пользователя')
    password = st.text_input('Введите пароль', type='password')

    if st.button('Войти'):
        user_data = sheet.get_all_records()
        for user in user_data:
            if user['Username'] == username and user['Password'] == password:
                st.success('Успешный вход')
                break
        else:
            st.error('Неверное имя пользователя или пароль')

# Основная часть приложения
def main():
    st.sidebar.title('Навигация')
    page = st.sidebar.radio('Выберите страницу', ['Регистрация', 'Авторизация'])

    if page == 'Регистрация':
        registration()
    elif page == 'Авторизация':
        login()

if __name__ == '__main__':
    main()
