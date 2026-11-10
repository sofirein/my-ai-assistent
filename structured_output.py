from gigachat import GigaChat
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

#Модель финансовой цели 
class FinancialGoal(BaseModel):
    goal_name: str = Field(description="Название цели (например, машина, отпуск)")
    target_amount: int = Field(description="Сколько денег нужно накопить (в рублях)")
    months_to_save: int = Field(description="За сколько месяцев планируется накопить")

#Создание объекта вручную
goal = FinancialGoal(goal_name="Новый ноутбук", target_amount=80000, months_to_save=6)
print("Цель:", goal.goal_name)
print("Сумма:", goal.target_amount)
print("Срок (мес):", goal.months_to_save)

# Анализ бюджета через chat_parse
class BudgetAnalysis(BaseModel):
    category: str = Field(description="Категория запроса (например, экономия, накопления)")
    advice: str = Field(description="Конкретный совет по бюджету")
    complexity: str = Field(description="Сложность ситуации: низкая, средняя, высокая")

prompt = "Я трачу 20000 на еду и хочу сократить расходы на 5000. Что делать?"
print("--- Задание 16-19: chat_parse ---")

try:
    with GigaChat(
        credentials=key, 
        scope=scope, 
        model="GigaChat-2",
        ca_bundle_file="certs/russian_trusted_root_ca_pem.crt"
    ) as client:
        #  strict=True
        # Использование chat_parse
        completion, parsed = client.chat_parse(
            prompt,
            response_format=BudgetAnalysis,
            strict=True
        )
        
        print("Категория:", parsed.category)
        print("Совет:", parsed.advice)
        print("Сложность:", parsed.complexity)
        
except Exception as error:
    print("Ошибка:", error)