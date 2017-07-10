from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold, cross_val_score
import titanic_data
import numpy as np
from sklearn.model_selection import GridSearchCV
import pandas
from sklearn.metrics import make_scorer, accuracy_score

# The columns we'll use to predict the target
pred = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked", "Title"]
training_data = titanic_data.get_training_data()
test_data = titanic_data.get_test_data()

from sklearn.model_selection import GridSearchCV, train_test_split

# Choose the type of classifier.
clf = RandomForestClassifier()

# Choose some parameter combinations to try
parameters = {'n_estimators': [4, 6, 9],
              'max_features': ['log2', 'sqrt','auto'],
              'criterion': ['entropy', 'gini'],
              'max_depth': [2, 3, 5, 10],
              'min_samples_split': [2, 3, 5],
              'min_samples_leaf': [1,5,8]
             }

# Type of scoring used to compare parameter combinations
acc_scorer = make_scorer(accuracy_score)

# Run the grid search
grid_obj = GridSearchCV(clf, parameters, scoring=acc_scorer)
grid_obj = grid_obj.fit(training_data[pred], training_data["Survived"])

# Set the clf to the best combination of parameters
clf = grid_obj.best_estimator_

# Fit the best algorithm to the data.
clf.fit(training_data[pred], training_data["Survived"])
kf = KFold(training_data.shape[0], n_folds=5, random_state=1)

rfc_training_predictions = []
for train, test in kf:
    train_predictors = (training_data[pred].iloc[train,:])
    train_target = training_data["Survived"].iloc[train]

    clf.fit(train_predictors, train_target)
    rfc_test_predictions = clf.predict(training_data[pred].iloc[test,:])
    rfc_training_predictions.append(rfc_test_predictions)

rfc_training_predictions = np.concatenate(rfc_training_predictions, axis=0)

# Map predictions to outcomes (the only possible outcomes are 1 and 0)

rfc_accuracy = sum(rfc_training_predictions[i] == training_data["Survived"][i] for i in range(len(rfc_training_predictions))) / len(rfc_training_predictions)

print("Random forest classifier - 5-fold validation accuracy: " +  str(rfc_accuracy))
