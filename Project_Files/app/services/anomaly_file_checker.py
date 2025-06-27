import pandas as pd

def detect_anomalies_from_csv(csv_file, kpi_column, threshold):
    try:
        df = pd.read_csv(csv_file)
        anomalies = []

        year_column = next((col for col in df.columns if 'year' in col.lower()), None)

        if kpi_column not in df.columns:
            return {"anomalies": [], "error": f"KPI column '{kpi_column}' not found in CSV."}

        if year_column is None:
            return {"anomalies": [], "error": "No 'Year' column found in CSV."}

        for _, row in df.iterrows():
            try:
                value = float(row[kpi_column])
                if value > float(threshold):
                    year = row[year_column]
                    # 🔁 Convert to native Python types to avoid JSON serialization issues
                    anomalies.append([int(year), float(value)])
            except (ValueError, TypeError):
                continue

        return {"anomalies": anomalies}

    except Exception as e:
        return {"anomalies": [], "error": f"Exception occurred: {str(e)}"}
