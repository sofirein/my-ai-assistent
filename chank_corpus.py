from pathlib import Path
import csv

#Проверка параметров
def split_with_overlap(text, chunk_size, overlap, minimum_length=30):
    if chunk_size <= 0:
        raise ValueError("chunk_size должен быть больше 0")
    if overlap < 0:
        raise ValueError("overlap не может быть отрицательным")
    if overlap >= chunk_size:
        raise ValueError("overlap должен быть меньше chunk_size")

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(text), step):
        # Удаляем пробелы по краям
        chunk = text[start:start + chunk_size].strip()
        
        #Не сохран пуст и слишком коротк
        if len(chunk) >= minimum_length:
            chunks.append(chunk)

    return chunks

#  Создать папку chunks
source_dir = Path("normalized")
chunks_dir = Path("chunks")
chunks_dir.mkdir(exist_ok=True)

#  Найти все TXT-файлы
files = list(source_dir.glob("*.txt"))
all_chunks = []

print(f"Найдено документов: {len(files)}\n")
print("--- Обработка документов ---")

for file_path in files:
    # Прочитать документ
    text = file_path.read_text(encoding="utf-8")
    
    #  Разбить на чанки
    chunks = split_with_overlap(text, chunk_size=300, overlap=50)
    
    #  Сохран
    for chunk_id, chunk in enumerate(chunks):
        chunk_data = {
            "source": file_path.name,
            "chunk_id": chunk_id,
            "length": len(chunk),
            "text": chunk
        }
        all_chunks.append(chunk_data)
        
        #  Сохранить каждый чанк в отдельн файл
        source_stem = file_path.stem
        filename = f"{source_stem}_chunk_{chunk_id}.txt"
        output_path = chunks_dir / filename
        output_path.write_text(chunk, encoding="utf-8")
    
    print(f"{file_path.name}: {len(chunks)} чанков")

#  Вывести число документов и общее число чанков
print(f"\n=== СВОДКА ===")
print(f"Всего документов: {len(files)}")
print(f"Всего чанков: {len(all_chunks)}")

#  Вычислить среднюю длину чанка
total_length = 0
for chunk in all_chunks:
    total_length += chunk["length"]

if len(all_chunks) > 0:
    average = total_length / len(all_chunks)
    print(f"Средняя длина чанка: {round(average, 1)} символов")

#  chunks_summary.csv
with open("chunks_summary.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["source", "chunk_id", "length"])
    
    for chunk in all_chunks:
        writer.writerow([
            chunk["source"],
            chunk["chunk_id"],
            chunk["length"]
        ])

print(f"\nГотово! Чанки в папке 'chunks', сводка в 'chunks_summary.csv'.")