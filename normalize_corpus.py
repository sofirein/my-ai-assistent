from pathlib import Path

# 4, 26, 27: Универсальная функция очистки одной строки
def clean_line(line):
    # 26: Заменяем неразрывный пробел
    line = line.replace("\u00a0", " ")
    # 2: Заменяем табуляцию на пробел
    line = line.replace("\t", " ")
    # 3: Убираем лишние пробелы внутри строки (оставляем только по одному)
    line = " ".join(line.split())
    return line

# 15: Универсальная функция нормализации всего текста
def normalize_text(text):
    lines = text.splitlines()
    clean_lines = []
    
    for line in lines:
        line = clean_line(line)
        
        # 6: Пропускаем пустые строки
        if line == "":
            continue
            
        #  9: Удаляем точные дубли строк (сохраняя порядок)
        if line not in clean_lines:
            clean_lines.append(line)
            
    return "\n".join(clean_lines)

# 21: Создаем папку для нормализованных документов
source_dir = Path("cleaned")       # Берем очищенные файлы из Дня 16
normalized_dir = Path("normalized")
normalized_dir.mkdir(exist_ok=True)

# 22: Находим все TXT-файлы в папке cleaned
files = list(source_dir.glob("*.txt"))
print(f"Найдено файлов для нормализации: {len(files)}\n")

total_before = 0
total_after = 0

print("--- Обработка документов ---")

for file_path in files:
    text = file_path.read_text(encoding="utf-8")
    
    # Нормализуем текст
    normalized = normalize_text(text)
    
    # Задание 18, 19, 24: Считаем размеры до и после
    before = len(text)
    after = len(normalized)
    
    total_before += before
    total_after += after
    
    # Задание 23: Сохраняем под тем же именем в папку normalized
    output_path = normalized_dir / file_path.name
    output_path.write_text(normalized, encoding="utf-8")
    
    print(f"{file_path.name}: {before} -> {after} символов (удалено {before - after})")

# 20, 31: Общая сводка и процент сокращения
print("=== ОБЩАЯ СВОДКА ===")
print(f"Общий объем до: {total_before} символов")
print(f"Общий объем после: {total_after} символов")

if total_before > 0:
    percent = (total_before - total_after) / total_before * 100
    print(f"Процент сокращения: {round(percent, 1)}%")

# 13: Проверка, что после очистки не появилось пустых документов
print("Проверка на пустые документы:")
for file_path in normalized_dir.glob("*.txt"):
    content = file_path.read_text(encoding="utf-8")
    if len(content.strip()) == 0:
        print(f"ВНИМАНИЕ: файл {file_path.name} пуст!")
    else:
        print(f"{file_path.name}: OK")

print("Готово! Все файлы сохранены в папку 'normalized'.")