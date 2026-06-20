import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# 1. 讀取資料
# =========================
df = pd.read_csv("merged_monthly_data.csv")

# 確保資料依月份排序
df = df.sort_values("year_month").reset_index(drop=True)

# =========================
# 2. 特徵與目標
# =========================
X = df[["weighted_score", "NASDAQCOM"]]
y = df["target_next_month_price"]

# =========================
# 3. Walk-forward validation
#    前 n 筆先拿來當最小訓練集
# =========================
initial_train_size = 12   # 你可以改成 6、8、10，看資料量
ridge_alpha = 1.0
lasso_alpha = 0.1

ridge_records = []
lasso_records = []

for i in range(initial_train_size, len(df)):
    X_train = X.iloc[:i]
    y_train = y.iloc[:i]
    X_test = X.iloc[i:i+1]
    y_test = y.iloc[i:i+1]

    # =========================
    # Ridge
    # =========================
    ridge = Ridge(alpha=ridge_alpha)
    ridge.fit(X_train, y_train)
    ridge_pred = ridge.predict(X_test)[0]

    ridge_records.append({
        "year_month": df.iloc[i]["year_month"],
        "weighted_score": df.iloc[i]["weighted_score"],
        "NASDAQCOM": df.iloc[i]["NASDAQCOM"],
        "actual_next_month_price": y_test.values[0],
        "pred_next_month_price": ridge_pred,
        "error": ridge_pred - y_test.values[0]
    })

    # =========================
    # Lasso
    # =========================
    lasso = Lasso(alpha=lasso_alpha, max_iter=10000)
    lasso.fit(X_train, y_train)
    lasso_pred = lasso.predict(X_test)[0]

    lasso_records.append({
        "year_month": df.iloc[i]["year_month"],
        "weighted_score": df.iloc[i]["weighted_score"],
        "NASDAQCOM": df.iloc[i]["NASDAQCOM"],
        "actual_next_month_price": y_test.values[0],
        "pred_next_month_price": lasso_pred,
        "error": lasso_pred - y_test.values[0]
    })

# =========================
# 4. 轉成 DataFrame
# =========================
ridge_result = pd.DataFrame(ridge_records)
lasso_result = pd.DataFrame(lasso_records)

# =========================
# 5. 評估函式
# =========================
def evaluate_result(result_df, model_name):
    y_true = result_df["actual_next_month_price"]
    y_pred = result_df["pred_next_month_price"]

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f"\n{model_name} Walk-forward 結果")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²  : {r2:.4f}")

# =========================
# 6. 印出評估
# =========================
evaluate_result(ridge_result, "Ridge")
evaluate_result(lasso_result, "Lasso")

# =========================
# 7. 存成 CSV
# =========================
ridge_result.to_csv("~/final_project/math_prediction/ridge_walk_forward_predictions.csv", index=False)
lasso_result.to_csv("~/final_project/math_prediction/lasso_walk_forward_predictions.csv", index=False)

print("\n已儲存：")
print("- ridge_walk_forward_predictions.csv")
print("- lasso_walk_forward_predictions.csv")
