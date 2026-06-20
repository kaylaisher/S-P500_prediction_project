import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# 1. 讀取資料
# =========================
df = pd.read_csv("merged_monthly_data.csv")

# 依月份排序
df = df.sort_values("year_month").reset_index(drop=True)

# =========================
# 2. 定義特徵與目標
# =========================
# endog: NASDAQ 當月價格
# exog: 當月情緒分數
endog = df["NASDAQCOM"]
exog = df[["weighted_score"]]

# =========================
# 3. Walk-forward 設定
# =========================
initial_train_size = 12   # 你可以改成 6、8、10
order = (1, 0, 0)         # ARIMAX 的簡單起手式
seasonal_order = (0, 0, 0, 0)  # 非季節版本

records = []

for i in range(initial_train_size, len(df)):
    y_train = endog.iloc[:i]
    X_train = exog.iloc[:i]
    
    y_test = endog.iloc[i:i+1]
    X_test = exog.iloc[i:i+1]

    # =========================
    # 4. 建模
    # =========================
    model = SARIMAX(
        y_train,
        exog=X_train,
        order=order,
        seasonal_order=seasonal_order,
        trend="c",
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    result = model.fit(disp=False)

    # =========================
    # 5. 預測下一期
    # =========================
    pred = result.forecast(steps=1, exog=X_test)
    pred_value = pred.iloc[0]

    records.append({
        "year_month": df.iloc[i]["year_month"],
        "weighted_score": df.iloc[i]["weighted_score"],
        "actual_nasdaq": y_test.values[0],
        "pred_nasdaq": pred_value,
        "error": pred_value - y_test.values[0]
    })

# =========================
# 6. 結果轉成 DataFrame
# =========================
result_df = pd.DataFrame(records)

# =========================
# 7. 評估
# =========================
y_true = result_df["actual_nasdaq"]
y_pred = result_df["pred_nasdaq"]

mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
r2 = r2_score(y_true, y_pred)

print("\nARIMAX Walk-forward 結果")
print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R²  : {r2:.4f}")

# =========================
# 8. 存成 CSV
# =========================
result_df.to_csv("arimax_walk_forward_predictions.csv", index=False)

print("\n已儲存：arimax_walk_forward_predictions.csv")
