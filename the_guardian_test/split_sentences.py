'''
python3 split_sentences.py 2024-01-1.txt
'''

from pathlib import Path
import json
import nltk
from nltk.tokenize import sent_tokenize

# 第一次使用才需要下載
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

def split_one_file(input_path: Path):
    # 讀取文字
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 斷句
    sentences = sent_tokenize(text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 輸出檔名：xxx.txt -> xxx_sentences.json
    output_path = input_path.with_name(input_path.stem + "_sentences.json")

    # 存成 JSON 陣列
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)

    print(f"[OK] {input_path.name} -> {output_path.name} ({len(sentences)} 句)")

def main():
    project_root = Path(__file__).resolve().parent
    target_dir = project_root / "the_guardian_test" / "count_emotion_index"

    if not target_dir.exists():
        print(f"找不到資料夾：{target_dir}")
        return

    txt_files = sorted(target_dir.glob("*.txt"))

    if not txt_files:
        print("資料夾內沒有找到任何 .txt 檔")
        return

    for txt_file in txt_files:
        split_one_file(txt_file)

    print(f"\n全部完成，共處理 {len(txt_files)} 個檔案")

if __name__ == "__main__":
    main()
