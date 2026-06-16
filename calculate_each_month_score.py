import pandas as pd
from pathlib import Path

# 讀取 CSV
input_path = Path("~/final_project/the_guardian_test/daily_score.csv").expanduser()
df = pd.read_csv(input_path, encoding="utf-8-sig")

df = df.dropna(subset=["year", "month", "weighted_score"])

# 確保 weighted_score 是數值
df["weighted_score"] = pd.to_numeric(df["weighted_score"], errors="coerce")

# 移除無效資料
df = df.dropna(subset=["year", "month", "weighted_score"])

# 轉成整數（這樣 groupby 的 key 也會是整數）
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)

# 依 year 和 month 分組
monthly = df.groupby(["year", "month"], as_index=False).agg(
    total_weighted_score=("weighted_score", "sum"),
    article_count=("article_index", "nunique")
)

# 計算每月加權平均
monthly["weighted_monthly_score"] = monthly["total_weighted_score"] / monthly["article_count"]

# 先印出結果測試
for row in monthly.itertuples(index=False):
    print(f"{row.year}-{row.month}: {row.weighted_monthly_score:.4f}")
