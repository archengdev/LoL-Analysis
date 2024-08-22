from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from test_train_data import get_data, MODES

# for mode in MODES:
#     # split data into training and test set
#     X_train, X_test, y_train, y_test = get_data("./9.19/processed_data.csv", mode)

#     # do logistic regression
#     clf = LogisticRegression(random_state=3)
#     clf.fit(X_train, y_train)
#     y_pred = clf.predict(X_test)

#     acc = accuracy_score(y_test, y_pred)
#     print("Accuracy:", acc*100)
# split data into training and test set

X_train, X_test, y_train, y_test = get_data("./9.19/processed_data.csv", 'mp')
# do logistic regression
clf = LogisticRegression(random_state=3)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc*100)

# Accuracy: 49.98263285863147