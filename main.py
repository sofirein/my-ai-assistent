import os 
from dotenv import load_dotenv
from gigachat import GigaChat 
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

print("=== Чат-помощник по бюджету ===")
print("Доступные команды: 'выход', 'очистить', 'история'")
print("Для начала просто напишите ваш доход и цель.\n")

# Задание 18, 19: Метка нового запуска в журнале
with open("chat_history.txt", "a", encoding="utf-8") as f:
    f.write("\n=== Новый запуск ===\n")

# Задание 10: Создаем messages ДО цикла (только system)
messages = [
    ChatMessage(role="system", content=SYSTEM_PROMPT)
]

max_pairs = 3 # Задание 16: Лимит пар
successful_exchanges = 0 # Доп. задание: счетчик обменов

with GigaChat(
    credentials=key,
    scope=scope,
    model="GigaChat-2",
    ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
    timeout=60,
) as client:
    
    # Задание 7: Бесконечный цикл ввода
    while True:
        user_input = input("\nВы: ").strip()
        
        # Задание 8: Проверка команды выхода
        if user_input.lower() == "выход":
            print("Завершение работы. До свидания!")
            break
            
        # Задание 8: Проверка пустого ввода
        if not user_input:
            print("Ошибка: пустой ввод. Пожалуйста, напишите текст.")
            continue
            
        # Задание 14: Команда очистки
        if user_input.lower() == "очистить":
            messages = [messages[0]] # Оставляем только system
            print("История текущего диалога очищена. Продолжайте общение.")
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write("\n[История текущего диалога очищена]\n")
            continue
            
        # Задание 15: Команда просмотра истории
        if user_input.lower() == "история":
            print(f"Текущая длина истории: {len(messages)}")
            print("Роли сообщений:")
            for m in messages:
                print(f"- {m.role}")
            continue

        # Если это обычный текст, добавляем его в историю
        messages.append(ChatMessage(role="user", content=user_input))

        # Сборка запроса с историей
        request = ChatCompletionRequest(
            messages=messages, # Передаем ВСЮ историю
            model_options=ChatModelOptions(
                temperature=0.2,
                max_tokens=400
            )
        )

        print("Помощник печатает...")
        
        try:
            # Отправка запроса
            response = client.chat.create(request)
            answer = response.messages[0].content[0].text
            
            print(f"Помощник: {answer}")
            
            # Задание 18: Добавляем ответ в историю
            messages.append(ChatMessage(role="assistant", content=answer))
            successful_exchanges += 1
            
            # Запись в текстовый журнал
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write(f"Вы: {user_input}\n")
                f.write(f"Помощник: {answer}\n\n")

            # Задание 17: Ограничение размера истории (max_pairs = 3)
            # 1 system + 2 * max_pairs (user + assistant)
            if len(messages) > 1 + 2 * max_pairs:
                # Оставляем system (messages[0]) и последние 2*max_pairs сообщений
                messages = [messages[0]] + messages[-2 * max_pairs:]
                print(f"[Система: память сокращена до последних {max_pairs} обменов]")

        except Exception as e:
            print(f"Ошибка при запросе к API: {e}")
            # Если ошибка, удаляем последний вопрос пользователя, чтобы не ломать историю
            messages.pop()