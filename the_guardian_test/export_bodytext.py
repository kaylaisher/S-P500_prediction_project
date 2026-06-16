import json
import os
import html
import sys

"""
python3 export_bodytext.py guardian_metadata_output/2024-01.json
"""

def export_bodytext(json_path, out_dir="count_emotion_index"):
    # 1. 從檔名取出月份前綴,例如 2024-01.json -> 2024-01
    prefix = os.path.splitext(os.path.basename(json_path))[0]

    # 2. 建立輸出資料夾(已存在也不會報錯)
    os.makedirs(out_dir, exist_ok=True)

    # 3. 讀 JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 4. iterate,start=1 讓編號從 1 開始
    for i, item in enumerate(data, start=1):
        body = item.get("bodyText", "")
        body = html.unescape(body)          # 把 &amp; 之類還原成 &
        filename = f"{prefix}-{i}.txt"        # 2024-01-1.txt ...
        out_path = os.path.join(out_dir, filename)
        with open(out_path, "w", encoding="utf-8") as out:
            out.write(body)
        print(f"已寫入 {out_path}  ({len(body)} 字元)")

if __name__ == "__main__":
    # 用法: python export_bodytext.py 2024-01.json
    path = sys.argv[1] if len(sys.argv) > 1 else "guardian_metadata_output/2024-01.json"
    export_bodytext(path)