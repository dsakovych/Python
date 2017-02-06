import pandas as pd

from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('titanic.csv', index_col='PassengerId')

# put the random state parameter = 241, else by default
clf = DecisionTreeClassifier(random_state=241)

columns = list(data.columns.values)

# removing all NaN values from Age column
data = data[data.Age.notnull()]

# making sex a boolean
data['Sex_nam'] = data['Sex']
data.loc[data['Sex'] == 'male', 'Sex_num'] = 1
data.loc[data['Sex'] == 'female', 'Sex_num'] = 0

# required arguments for our tree   
target = data['Survived'].values
features = data[ ['Pclass', 'Fare', 'Age', 'Sex_num'] ].as_matrix()

clf = clf.fit(features, target)
importances = clf.feature_importances_

# features importances: [(0.30343646953145248, 'Fare'), (0.1400052185312419, 'Pclass'), (0.30051221095823943, 'Sex'), (0.25604610097906622, 'Age')]
print dict(zip(importances, ['Pclass', 'Fare', 'Age', 'Sex'])).items()
