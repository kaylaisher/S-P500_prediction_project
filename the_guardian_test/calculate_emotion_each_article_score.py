'''
import pandas as pd

# 讀取 CSV
df = pd.read_csv("~/final_project/the_guardian_test/emotion_tendency.csv", encoding="utf-8-sig")

# 確保 score 是數值
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# 建立一個字典來存每個 source 的累積分數
source_scores = {}

# 逐筆資料處理
for _, row in df.iterrows():
    source = row["source"]
    tendency = str(row["tendency"]).strip().lower()
    score = row["score"]

    # 如果 score 不合法就跳過
    if pd.isna(score):
        continue

    # 初始化該 source
    if source not in source_scores:
        source_scores[source] = 0.0

    # 根據情緒正負決定加總方式
    if tendency == "positive":
        source_scores[source] += score
    elif tendency == "negative":
        source_scores[source] -= score

# 印出結果
for source, total_score in source_scores.items():
    print(f"{source}: {round(total_score, 4)}")
'''
import pandas as pd
from pathlib import Path

# 檔案路徑
input_path = Path("~/final_project/the_guardian_test/emotion_tendency.csv").expanduser()
output_path = Path("~/final_project/the_guardian_test/daily_score.csv").expanduser()

# 讀取 CSV
df = pd.read_csv(input_path, encoding="utf-8-sig")

# 確保 score 是數值
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# 建立 signed_score
def get_signed_score(row):
    score = row["score"]
    tendency = str(row["tendency"]).strip().lower()

    if pd.isna(score):
        return None

    if tendency == "positive":
        return score
    elif tendency == "negative":
        return -score
    else:
        return 0.0

df["signed_score"] = df.apply(get_signed_score, axis=1)

# 移除無效資料
df = df.dropna(subset=["signed_score"])

# 依 source 分組，計算總分
grouped = df.groupby("source", as_index=False).agg(
    year=("year", "first"),
    total_score=("signed_score", "sum"),
    sentence_count=("sentence", "count")
)

# 從 source 拆出 month 和 article_index
# 例如：2024-01-1_sentences -> month=01, article_index=1
grouped["month"] = grouped["source"].str.extract(r"^\d{4}-(\d{2})-\d+_")[0]
grouped["article_index"] = grouped["source"].str.extract(r"^\d{4}-\d{2}-(\d+)_")[0]

# 計算 weighted_score
grouped["weighted_score"] = grouped["total_score"] / grouped["sentence_count"]


# 調整欄位順序
result = grouped[["year", "month", "article_index", "weighted_score"]].copy()
result["weighted_score"] = result["weighted_score"].round(4)

# 寫入新的 CSV
result.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"已輸出到：{output_path}")
print(result)
