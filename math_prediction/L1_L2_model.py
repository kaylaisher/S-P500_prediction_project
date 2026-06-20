import pandas as pd
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import numpy as np


# =========================
# 1. 讀取資料
# =========================
df = pd.read_csv("merged_monthly_data.csv")

# =========================
# 2. 建立特徵與目標
# =========================
X = df[["weighted_score", "NASDAQCOM"]]
y = df["target_next_month_price"]

# =========================
# 3. 時間序列切分
#    不要隨機切分
# =========================
split_idx = int(len(df) * 0.7)

X_train = X.iloc[:split_idx]
X_test = X.iloc[split_idx:]
y_train = y.iloc[:split_idx]
y_test = y.iloc[split_idx:]

# =========================
# 4. Ridge
# =========================
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
ridge_pred = ridge.predict(X_test)

# =========================
# 5. Lasso
# =========================
lasso = Lasso(alpha=0.1, max_iter=10000)
lasso.fit(X_train, y_train)
lasso_pred = lasso.predict(X_test)

# =========================
# 6. 評估函式
# =========================
def evaluate_model(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    print(f"\n{model_name} 評估結果")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²  : {r2:.4f}")

# =========================
# 7. 輸出結果
# =========================
evaluate_model(y_test, ridge_pred, "Ridge")
evaluate_model(y_test, lasso_pred, "Lasso")

# =========================
# 8. 看預測值
# =========================
result = df.iloc[split_idx:].copy()
result["ridge_pred"] = ridge_pred
result["lasso_pred"] = lasso_pred

print("\n預測結果：")
print(result[["year_month", "weighted_score", "NASDAQCOM", "target_next_month_price", "ridge_pred", "lasso_pred"]])

# =========================
# 9. 存成 CSV
# =========================
result.to_csv("~/final_project/math_prediction/ridge_lasso_70_30_predictions.csv", index=False)
