from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from test_train_data import get_data


# split data into training and test set
X_train, X_test, y_train, y_test = get_data("./9.19/processed_data.csv")

# do random forest
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=3)

rf_classifier.fit(X_train, y_train)

y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_rep)



"""
Accuracy: 0.49
Classification Report:
               precision    recall  f1-score   support

           0       0.49      0.51      0.50      2874
           1       0.49      0.48      0.48      2884

    accuracy                           0.49      5758
   macro avg       0.49      0.49      0.49      5758
weighted avg       0.49      0.49      0.49      5758
"""