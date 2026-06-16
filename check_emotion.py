import json
from pathlib import Path

# 設定專案根目錄
project_root = Path(__file__).resolve().parent
print("project_root:", project_root)

# 讀取文字檔
txt_path = project_root / "the_guardian_test" / "count_emotion_index" / "2024-01-1.txt"

# 讀取 emotion.json
json_path = project_root / "emotion_dataset" / "emotion.json"

print("txt 路徑：", txt_path)
print("json 路徑：", json_path)

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

with open(json_path, "r", encoding="utf-8") as f:
    emotion_data = json.load(f)

print("文字檔前 200 字：")
print(text[:200])

positive_words = emotion_data.get("positive", [])
negative_words = emotion_data.get("negative", [])

print("positive_words 數量：", len(positive_words))
print("negative_words 數量：", len(negative_words))

matched_positive = []
matched_negative = []

if "Wall" in text:
    print("文本中包含 'Wall' 字樣。")

# 檢查 positive
for word in positive_words:
    if word in text:
        matched_positive.append(word)

# 檢查 negative
for word in negative_words:
    if word in text:
        matched_negative.append(word)

print("命中的 positive：", matched_positive)
print("命中的 negative：", matched_negative)
