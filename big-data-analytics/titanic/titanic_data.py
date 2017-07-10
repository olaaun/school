import pandas
import re

train = pandas.read_csv("train.csv")
test = pandas.read_csv("test.csv")

def get_training_data():
    return transform_titanic_data(train)

def get_test_data():
    return transform_titanic_data(test)

# Returns the title of person given the name
def get_title(name):
    title_search = re.search(' ([A-Za-z]+)\.', name)
    if title_search:
        return title_search.group(1)
    return ""


def transform_titanic_data(data):

    #Transforming the data set
    #Add median age to missing age values
    data["Age"] = data["Age"].fillna(train["Age"].median())

    #Change gender and embarked to numeric values
    data.loc[data["Sex"] == "male", "Sex"] = 0
    data.loc[data["Sex"] == "female", "Sex"] = 1
    data["Embarked"] = data["Embarked"].fillna("S")
    data.loc[data["Embarked"] == "S", "Embarked"] = 0
    data.loc[data["Embarked"] == "C", "Embarked"] = 1
    data.loc[data["Embarked"] == "Q", "Embarked"] = 2

    data["Fare"] = data["Fare"].fillna(data["Fare"].median())

    titles = data["Name"].apply(get_title)
    # Map each title to an integer
    # Some titles are very rare, so they're compressed into the same codes as other titles
    title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Dr": 5, "Rev": 6, "Major": 7, "Col": 7, "Mlle": 8, "Mme": 8, "Don": 9, "Lady": 10, "Countess": 10, "Jonkheer": 10, "Sir": 9, "Capt": 7, "Ms": 2, "Dona": 2}
    for k,v in title_mapping.items():
        titles[titles == k] = v

    # Add in the title column
    data["Title"] = titles
    return data

if __name__ == "__main__":
    print(get_training_data())
