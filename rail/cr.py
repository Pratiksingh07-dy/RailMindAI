import pandas as pd
import numpy as np

n = 5000

df = pd.DataFrame({
    "hour": np.random.randint(0,24,n),
    "day_of_week": np.random.randint(0,7,n),
    "station_id": np.random.randint(1,50,n),
    "rainfall": np.random.uniform(0,50,n),
    "temperature": np.random.uniform(20,40,n),
    "rush_hour": np.random.randint(0,2,n)
})

score = df["hour"]*0.3 + df["rush_hour"]*20 + df["rainfall"]*0.1

df["crowd_level"] = pd.cut(
    score,
    bins=[-1,15,25,35,100],
    labels=[0,1,2,3]
)

df.to_csv("crowd_data.csv",index=False)