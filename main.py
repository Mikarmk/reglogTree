import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Подключение к Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('your-google-sheet').sheet1

# Регистрация пользователя
def register_user(username, password):
    existing_users = sheet.col_values(1)
    if username in existing_users:
        return "Пользователь с таким именем уже существует"
    else:
        sheet.append_row([username, password])
        return "Регистрация прошла успешно"

# Авторизация пользователя
def login_user(username, password):
    user_data = sheet.find(username)
    if user_data:
        stored_password = sheet.cell(user_data.row, 2).value
        if password == stored_password:
            return "Авторизация успешна"
        else:
            return "Неверный пароль"
    else:
        return "Пользователь не найден"

# Сохранение сообщений пользователя
def save_message(username, message):
    messages_sheet = client.open('your-google-sheet').get_worksheet(1)
    messages = messages_sheet.col_values(1)
    if len(messages) >= 10:
        messages_sheet.delete_row(1)
    messages_sheet.append_row([message])

# Интерфейс Streamlit
st.title('Регистрация и авторизация')

action = st.selectbox('Выберите действие', ['Регистрация', 'Авторизация'])

if action == 'Регистрация':
    username = st.text_input('Имя пользователя')
    password = st.text_input('Пароль', type='password')
    if st.button('Зарегистрироваться'):
        result = register_user(username, password)
        st.write(result)

if action == 'Авторизация':
    username = st.text_input('Имя пользователя')
    password = st.text_input('Пароль', type='password')
    if st.button('Войти'):
        result = login_user(username, password)
        st.write(result)
