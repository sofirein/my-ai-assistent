import logging

#  Настройка логирования
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

#Три уровня
logging.info("Помощник по бюджету запущен")
logging.warning("Пользователь не указал категорию расходов")
logging.error("Не удалось подключиться к базе данных трат")

print("Смотри файл app.log, там всё записалось")