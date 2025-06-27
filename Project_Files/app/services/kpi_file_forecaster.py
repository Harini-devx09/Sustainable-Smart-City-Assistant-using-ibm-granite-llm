import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_kpi(df: pd.DataFrame) -> dict:
    try:
        # Assume the dataframe has columns like: ["Year", "Water_Usage"]
        if df.shape[1] < 2:
            return {"error": "CSV must have at least 2 columns: X and Y"}

        df.columns = ['X', 'Y']  # rename for generalization
        X = df[['X']]
        y = df['Y']

        model = LinearRegression()
        model.fit(X, y)

        next_year = max(X['X']) + 1
        predicted = model.predict([[next_year]])[0]

        return {
            "input_years": X['X'].tolist(),
            "input_values": y.tolist(),
            "next_year": next_year,
            "predicted_value": round(predicted, 2)
        }
    except Exception as e:
        return {"error": str(e)}
