'''
import pandas as pd

# 讀取 CSV
df = pd.read_csv("NASDAQCOM.csv")

# 把日期欄轉成 datetime
df["observation_date"] = pd.to_datetime(df["observation_date"])

# 依日期排序，避免資料原本順序亂掉
df = df.sort_values("observation_date")

# 取出年月
df["year_month"] = df["observation_date"].dt.to_period("M")

# 每個月取第一筆交易日資料
monthly_first = df.groupby("year_month").first().reset_index()

print(monthly_first)
'''

import pandas as pd

# 讀取 CSV
df = pd.read_csv("NASDAQCOM.csv")

# 把日期欄轉成 datetime
df["observation_date"] = pd.to_datetime(df["observation_date"])

# 依日期排序
df = df.sort_values("observation_date")

# 取出年月
df["year_month"] = df["observation_date"].dt.to_period("M").astype(str)

# 每個月取第一筆交易日資料
monthly_first = (
    df.groupby("year_month", as_index=False)
      .first()
)

# 只保留你要的欄位
monthly_first = monthly_first[["year_month", "observation_date", "NASDAQCOM"]]

# 把日期轉回字串格式，方便存 CSV
monthly_first["observation_date"] = monthly_first["observation_date"].dt.strftime("%Y-%m-%d")

# 存成新的 CSV
monthly_first.to_csv("first_trade_day_of_month.csv", index=False)

print(monthly_first)
