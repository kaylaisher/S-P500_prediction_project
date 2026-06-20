import pandas as pd

# =========================
# 1. 讀取資料
# =========================
sentiment_df = pd.read_csv("~/final_project/the_guardian_test/each_month_score.csv")
nasdaq_df = pd.read_csv("~/final_project/nasdaq_data/first_trade_day_of_month.csv")

# =========================
# 2. 統一月份欄位格式
# =========================
# 把 year + month 合成 year_month，例如 2024-1 -> 2024-01
sentiment_df["year_month"] = (
    sentiment_df["year"].astype(str) + "-" +
    sentiment_df["month"].astype(str).str.zfill(2)
)

# 讓 NASDAQ 的 year_month 也是字串
nasdaq_df["year_month"] = nasdaq_df["year_month"].astype(str)

# =========================
# 3. 合併兩份資料
# =========================
df = pd.merge(
    sentiment_df[["year_month", "weighted_score"]],
    nasdaq_df[["year_month", "observation_date", "NASDAQCOM"]],
    on="year_month",
    how="inner"
)

# =========================
# 4. 排序
# =========================
df = df.sort_values("year_month").reset_index(drop=True)

# =========================
# 5. 建立 next-month target
# =========================
df["target_next_month_price"] = df["NASDAQCOM"].shift(-1)

# =========================
# 6. 去掉最後一筆沒有 next month 的資料
# =========================
df = df.dropna(subset=["target_next_month_price"])

# =========================
# 7. 存成新 CSV
# =========================
df.to_csv("~/final_project/math_prediction/merged_monthly_data.csv", index=False)

print(df)
