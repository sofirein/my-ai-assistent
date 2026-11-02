import os 
from dotenv import load_dotenv
from gigachat import GigaChat 
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions

# 1. Чтение настроек: загружаем ключ доступа из скрытого файла (.env)
load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

print("=== Помощник по бюджету ===")

# 2. Ввод пользователя (Задание 7): три отдельных вопроса
income = input("1. Какой у вас доход? ").strip()
constraint = input("2. Есть ли ограничения (ипотека, кредиты)? ").strip()
goal = input("3. Какая ваша цель (на что копите)? ").strip()

# 3. Выбор формата (Задание 11)
format_choice = input("Формат (1 - краткий, 2 - пошаговый): ").strip()

# 4. Проверки на пустоту (Задание 9)
if not income or not goal:
    print("Ошибка: Доход и цель обязательны для заполнения. Запрос не отправлен.")
    exit()

if not constraint:
    constraint = "не указаны"

if format_choice == "1":
    format_text = "Дай краткий ответ, только основные цифры и выводы."
elif format_choice == "2":
    format_text = "Дай подробный пошаговый ответ с объяснениями."
else:
    print("Ошибка: Неверный выбор формата. Введите 1 или 2. Запрос не отправлен.")
    exit()

# 5. Сборка пользовательского промпта (Задание 8)
user_prompt = f"""
Мои данные:
- Доход: {income} рублей.
- Ограничения: {constraint}.
- Цель: {goal}.

Формат ответа: {format_text}
"""

print("--- Сформированный запрос ---")
print(user_prompt)
print("-----------------------------")

# 6. Сборка запроса с настройками (Задания 3, 13)
request = ChatCompletionRequest(
    messages=[
        ChatMessage(
            role="system",
            content=SYSTEM_PROMPT,
        ),
        ChatMessage(
            role="user",
            content=user_prompt,  # Передаем собранный текст
        )
    ],
    # Настройки генерации (Задание 13)
    model_options=ChatModelOptions(
        temperature=0.2,
        max_tokens=400,
        repetition_penalty=1.05
    )
)

print("Отправляем запрос....")

with GigaChat(
    credentials=key,
    scope=scope,
    model="GigaChat-2",
    ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
    timeout=60,
) as client:
    # 7. Отправка запроса
    response = client.chat.create(request)
    # 8. Извлечение текста ответа
    answer = response.messages[0].content[0].text
    print("\n=== Ответ нейросети ===")
    print(answer)

# 9. Сохранение в файлы (Задание 19)
with open("last_prompt.txt", "w", encoding="utf-8") as f:
    f.write(user_prompt)

with open("last_answer.txt", "w", encoding="utf-8") as f:
    f.write(answer)

print("\n[Файлы last_prompt.txt и last_answer.txt обновлены]")