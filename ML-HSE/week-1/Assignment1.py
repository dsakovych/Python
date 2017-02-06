import pandas
import numpy
import operator
data = pandas.read_csv('titanic.csv', index_col='PassengerId')

columns = list(data.columns.values)
print columns

male_count = 0
female_count = 0
male_names = []
male_fnames = []
female_names = []
female_fnames = []
names_count_f = {}
names_count_m = {}

# counting male and female (Male = 577 Female = 314)
for i in range(1, len(data['Sex'])+1):
    if data['Sex'][i] == 'male':
        male_count += 1
        male_names.append(data['Name'][i])
    else:
        female_count += 1
        female_names.append(data['Name'][i])
print "Male =", male_count, "Female =", female_count

# counting percent of survived (38.38%)
survived = round(float(sum(data['Survived'])) / len(data['Survived'])*100,2)
print "Survived (%)", survived

# Mean = 29.7 Median = 28.0
age =  data['Age'][numpy.logical_not(numpy.isnan(data['Age']))]
print "Mean =", round(numpy.mean(age),2), "Median =", numpy.median(age)

# Pirson correlation (0.41483769862)
print "Pirson corr =", numpy.corrcoef(data['SibSp'],data['Parch'])[0,1]

#parsing male names
for i in range(len(male_names)):
    male_names[i] = male_names[i].split()
    for j in range(len(male_names[i])):
        if "." in male_names[i][j]:
            male_fnames.append(male_names[i][j+1])
            
#parsing female names
for i in range(len(female_names)):
    female_names[i] = female_names[i].split()
    for j in range(len(female_names[i])):
        if "Miss." == female_names[i][j] or "Dr." == female_names[i][j]:
            female_fnames.append(female_names[i][j+1])
        elif female_names[i][j].startswith('(') and female_names[i][j].endswith(')') :
            female_fnames.append(female_names[i][j][1:len(female_names[i][j])])
        elif female_names[i][j].startswith('('):
            female_fnames.append(female_names[i][j][1:])
            
# Anna - 14, William - 35            
for name in female_fnames:
    names_count_f[name] = names_count_f.get(name, 0) + 1
for name in male_fnames:
    names_count_m[name] = names_count_m.get(name, 0) + 1
print "Most popular female name", sorted(names_count_f.items(), key = operator.itemgetter(1), reverse = True)[0]
print "Most popular male name", sorted(names_count_m.items(), key = operator.itemgetter(1), reverse = True)[0]

# 1st class passengers: 24.24%
print "1st class passengers (%):",round(float(sum([item for item in data['Pclass'] if item == 1])) * 100 / len(data['Pclass']),2)
