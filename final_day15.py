import logging
import os
from dotenv import load_dotenv
from gigachat import GigaChat
from pydantic import BaseModel, Field
from prompts import SYSTEM_PROMPT 

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

# Настройка логов
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

#  Модель анализа (заточена под бюджет)
class BudgetAnalysis(BaseModel):
    topic: str = Field(description="Тема запроса")
    category: str = Field(description="Категория расходов")
    advice: str = Field(description="Совет по экономии")
    savings: str = Field(description="Рекомендация по накоплениям")

def main():
    logging.info("Запуск final_day15")
    
    text = input("Опишите вашу ситуацию с бюджетом (доход, расходы, цель): ").strip()
    
    # Пустой ввод - не отправляем запрос
    if text == "":
        print("Вы ничего не ввели!")
        logging.warning("Пустой ввод")
        return

    logging.info("Запрос: %s", text)
    
    full = SYSTEM_PROMPT + "Данные пользователя: " + text

    print("Отправляю запрос...")
    logging.info("Отправка в API")

    try:
        with GigaChat(
            credentials=key,
            scope=scope,
            model="GigaChat-2",
            ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
            timeout=60
        ) as client:
            
            comp, parsed = client.chat_parse(
                full,
                response_format=BudgetAnalysis,
                strict=True
            )
            
            print("Результат анализа:")
            print("Тема:", parsed.topic)
            print("Категория:", parsed.category)
            print("Совет:", parsed.advice)
            print("Накопления:", parsed.savings)
            
            logging.info("Ответ получен")

    # Обработка ошибки
    except Exception as e:
        print("Не получилось получить ответ, проверьте подключение.")
        logging.error("Ошибка: %s", e)

if __name__ == "__main__":
    main()
 