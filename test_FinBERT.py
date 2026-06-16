
import json
import csv
from pathlib import Path
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)

input_dir = Path("/home/kayla/final_project/the_guardian_test/news_article_process")
output_csv = Path("/home/kayla/final_project/the_guardian_test/emotion_tendency.csv")

json_files = sorted(input_dir.glob("*_sentences.json"))

with output_csv.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["year", "source", "line", "tendency", "score", "sentence"])

    for idx, json_file in enumerate(json_files, start=1):
        year = json_file.name[:4]
        source_name = json_file.stem

        try:
            with json_file.open("r", encoding="utf-8") as jf:
                sentences = json.load(jf)

            if not sentences:
                print(f"[{idx}/{len(json_files)}] 跳過空檔案：{json_file.name}")
                continue

            # 批次分析
            results = classifier(sentences, truncation=True)

            # 邊跑邊寫，不存在記憶體裡
            for i, (sentence, result) in enumerate(zip(sentences, results), start=1):
                writer.writerow([
                    year,
                    source_name,
                    f"{i:02d}",
                    result["label"],
                    f"{result['score']:.4f}",
                    sentence
                ])

            print(f"[{idx}/{len(json_files)}] 已完成：{json_file.name}")

        except Exception as e:
            print(f"[{idx}/{len(json_files)}] 讀取失敗：{json_file.name}，錯誤：{e}")

print(f"全部完成，結果已儲存到：{output_csv}")
