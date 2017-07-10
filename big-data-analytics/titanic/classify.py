from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, accuracy_score
from matplotlib import pyplot as plt
import pandas
import numpy as np
import sys
import titanic_data

# Predictors
pred = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked", "Title"]
training_data = titanic_data.get_training_data()
test_data = titanic_data.get_test_data()

# The algorithms, logistic regression and random forest
logReg = LogisticRegression(random_state=1)
rfc = RandomForestClassifier(random_state=1, n_estimators=50, min_samples_split=4, min_samples_leaf=2)

#If -tweak argument is passed, run the grid search for finding best rfc estimator
if len(sys.argv) > 1 and sys.argv[1] == "-tweak":
    rfc = RandomForestClassifier()
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
    grid = GridSearchCV(rfc, parameters, scoring=acc_scorer, cv = 5)
    grid = grid.fit(training_data[pred], training_data["Survived"])

    # Set the rfc to the best combination of parameters
    rfc = grid.best_estimator_

    # Fit the best algorithm to the data.
    rfc.fit(training_data[pred], training_data["Survived"])

kf = KFold(training_data.shape[0], n_folds=5, random_state=1)

logReg_training_predictions = []
rfc_training_predictions = []


for train, test in kf:
    train_predictors = (training_data[pred].iloc[train,:])
    train_target = training_data["Survived"].iloc[train]

    logReg.fit(train_predictors, train_target)
    logReg_test_predictions = logReg.predict(training_data[pred].iloc[test,:])
    logReg_training_predictions.append(logReg_test_predictions)

    rfc.fit(train_predictors, train_target)
    rfc_test_predictions = rfc.predict(training_data[pred].iloc[test,:])
    rfc_training_predictions.append(rfc_test_predictions)

#Flatten arrays
logReg_training_predictions = np.concatenate(logReg_training_predictions, axis=0)
rfc_training_predictions = np.concatenate(rfc_training_predictions, axis=0)

#Calculate accuracies and print them
logReg_accuracy = sum(logReg_training_predictions[i] == training_data["Survived"][i] for i in range(len(logReg_training_predictions))) / len(logReg_training_predictions)
rfc_accuracy = sum(rfc_training_predictions[i] == training_data["Survived"][i] for i in range(len(rfc_training_predictions))) / len(rfc_training_predictions)
print("Logistic regression - 5-fold validation accuracy: " +  str(logReg_accuracy))
print("Random forest classifier - 5-fold validation accuracy: " +  str(rfc_accuracy))

#Make predictions on test set and save to file
logReg_test_predictions = logReg.predict(test_data[pred])
submission = pandas.DataFrame({
        "PassengerId": test_data["PassengerId"],
        "Survived": logReg_test_predictions
    })
submission.to_csv("logReg.csv", index=False)

rfc_test_predictions = rfc.predict(test_data[pred])
submission = pandas.DataFrame({
        "PassengerId": test_data["PassengerId"],
        "Survived": rfc_test_predictions
    })
submission.to_csv("rfc.csv", index=False)
