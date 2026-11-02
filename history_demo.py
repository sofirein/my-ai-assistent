from gigachat.models import ChatMessage
from prompts import SYSTEM_PROMPT

# Задание 4: Создаем список и добавляем сообщения вручную
messages = [
    ChatMessage(role="system", content=SYSTEM_PROMPT),
    ChatMessage(role="user", content="Мой доход 50000, хочу накопить на машину."),
    ChatMessage(role="assistant", content="Тестовый ответ без API: для накопления на машину рекомендую откладывать 10%.")
]

# Задание 5: Выводим длину и роли
print(f"Длина истории: {len(messages)}")
print("Роли сообщений:")
for message in messages:
    print(f"- {message.role}")

# Задание 6: Предсказание (в отчете вы напишете, что ожидали 5 элементов для 2 обменов)
# Добавляем еще один обмен для проверки
messages.append(ChatMessage(role="user", content="А если я сокращу расходы на еду?"))
messages.append(ChatMessage(role="assistant", content="Это поможет быстрее достичь цели."))
print(f"\nПосле второго обмена длина: {len(messages)}")
for message in messages:
    print(f"- {message.role}")

# Задание 9: Проверка цикла и добавления без API
print("\n--- Проверка цикла (Задание 9) ---")
test_messages = [ChatMessage(role="system", content=SYSTEM_PROMPT)]

while True:
    user_input = input("Введите текст (или 'выход'): ").strip()
    
    # Задание 8: Проверки
    if user_input.lower() == "выход":
        print("Завершение работы.")
        break
    if not user_input:
        print("Пустой ввод, попробуйте снова.")
        continue

    # Задание 9: Добавляем в список
    test_messages.append(ChatMessage(role="user", content=user_input))
    # Имитация ответа
    test_messages.append(ChatMessage(role="assistant", content="Тестовый ответ без API"))
    
    print(f"Длина списка: {len(test_messages)}")
    print("Текущие роли:", [m.role for m in test_messages])

# Задание 16: Тест ограничения истории (max_pairs = 3)
print("\n--- Проверка лимита истории (Задание 16) ---")
max_pairs = 3
# Создаем 4 полные пары (плюс 1 system = 9 элементов)
limit_test = [ChatMessage(role="system", content="system")]
for i in range(1, 5):
    limit_test.append(ChatMessage(role="user", content=f"Вопрос {i}"))
    limit_test.append(ChatMessage(role="assistant", content=f"Ответ {i}"))

print(f"До сокращения: {len(limit_test)} элементов")
# Алгоритм: system + последние 2*max_pairs элементов
if len(limit_test) > 1 + 2 * max_pairs:
    limit_test = [limit_test[0]] + limit_test[-2 * max_pairs:]

print(f"После сокращения: {len(limit_test)} элементов")
print("Роли после сокращения:", [m.role for m in limit_test])
print("Тексты после сокращения:", [m.content for m in limit_test])