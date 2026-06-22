import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

n = 5000

data = pd.DataFrame({
    "crowd_density": np.random.randint(0, 100, n),
    "injured_count": np.random.randint(0, 20, n),
    "delay_minutes": np.random.randint(0, 60, n)
})

severity_score = (
    data["crowd_density"] +
    data["injured_count"] * 5 +
    data["delay_minutes"]
)

data["severity"] = pd.cut(
    severity_score,
    bins=[0, 50, 100, 150, 1000],
    labels=["Low", "Medium", "High", "Critical"]
)

X = data.drop("severity", axis=1)
y = data["severity"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "severity_model.pkl")

print("severity_model.pkl created")