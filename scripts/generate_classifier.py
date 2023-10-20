import pandas as pd
import numpy as np
import joblib
from ast import literal_eval

from sklearn.linear_model import SGDClassifier

datafile_path = "data/posts_with_embeddings.csv"

df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(literal_eval).apply(
    np.array
)  # convert string to array

# X_train, X_test, y_train, y_test = train_test_split(
#     list(df.embedding.values), df.score, test_size=0.2, random_state=42
# )


clf = SGDClassifier()
clf.fit(list(df.embedding.values), df.score)

joblib.dump(clf, "data/posts_model.pkl", compress=9)

# preds = clf.predict(X_test)
# probas = clf.predict_proba(X_test)


# report = classification_report(y_test, preds)
