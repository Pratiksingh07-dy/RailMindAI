from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

texts = [
    "passenger fell from train",
    "medical emergency in coach",
    "signal failure",
    "overcrowded platform",
    "theft reported",
    "fight between passengers",
    "train technical issue",
    "security threat"
]

labels = [
    "Safety",
    "Medical",
    "Technical",
    "Crowd",
    "Security",
    "Security",
    "Technical",
    "Security"
]

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

model.fit(texts, labels)

joblib.dump(model, "incident_classifier.pkl")

print("incident_classifier.pkl created")