from gigachat import GigaChat
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

#Ошибка int() и сохранение объекта ошибки
print("--- Задание 1-2: try/except с int() ---")
try:
    income = int(input("Введите ваш доход (только цифры): "))
    print("Вы ввели доход:", income, "руб.")
except Exception as error:
    print("Это не число! Введите сумму цифрами.", error)

#API внутри try, короткое сообщение пользователю
print("--- Задание 3-4: API внутри try/except ---")
try:
    with GigaChat(credentials=key, scope=scope, model="GigaChat-2", verify_ssl_certs=False) as client:
        response = client.chat.create("Как сэкономить 1000 рублей?")
        print(response.messages[0].content[0].text)
except Exception as err:
    print("Не удалось получить совет по экономии.")
    print("Техническая информация:", err)