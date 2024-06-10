# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,accuracy_score
from sklearn.model_selection import TimeSeriesSplit,train_test_split
from sklearn.cluster import KMeans
import matplotlib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report,accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.svm import LinearSVC
import pylab as pl
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

df=pd.read_csv("athlete_events.csv")

# %%
df

# %%
df.head()

# %%
df.info()

# %%
df.describe()

# %%
df.dtypes

# %%
df.ndim

# %%
df.shape

# %%
df.isna().sum()

# %%
#DNW:Did Not win , missing values of medal are filled with DNW
df['Medal'].fillna("DNW",inplace=True)

# %%
df_noc=pd.read_csv("noc_regions.csv")

# %%
df_noc

# %%
df_noc=df_noc.drop("notes",axis=1)

# %%
df_noc

# %%
df_noc.rename(columns={"region":"country"},inplace=True)

# %%
df_noc

# %%
df.sample(4)

# %%
#joining both dataset
olympics_merge=df.merge(df_noc,left_on='NOC',right_on='NOC',how='left')

# %%
olympics_merge.sample()

# %%
print(olympics_merge.loc[olympics_merge['country'].isnull(),['NOC', 'Team']].drop_duplicates())

# %%
# Replace missing Teams by the values 1. SGP - Singapore
                                    # 2. ROT - Refugee Olympic Athletes
                                    # 3. UNK - Unknown
                                    # 4. TUV - Tuvalu
#olympics_merge.loc[olympics_merge['Country'].isnull(), ['Country']] = olympics_merge['Team']

# %%
olympics_merge.loc[olympics_merge['country'].isnull(), ['country']] = olympics_merge['Team']

# %%
olympics_merge

# %%
print(olympics_merge.loc[olympics_merge['country'].isnull(),['NOC', 'Team']].drop_duplicates())

# %%
olympics_merge['country'] = np.where(olympics_merge['NOC']=='SGP', 'Singapore', olympics_merge['country'])
olympics_merge['country'] = np.where(olympics_merge['NOC']=='ROT', 'Refugee Olympic Athletes', olympics_merge['country'])
olympics_merge['country'] = np.where(olympics_merge['NOC']=='UNK', 'Unknown', olympics_merge['country'])
olympics_merge['country'] = np.where(olympics_merge['NOC']=='TUV', 'Tuvalu', olympics_merge['country'])

# %%
olympics_merge

# %%
olympics_merge.drop("Team",axis=1,inplace=True)

# %%
olympics_merge.sample()

# %%
olympics_merge.rename(columns={'country':'Team'},inplace=True)

# %%
olympics_merge.head(2)

# %%
print(olympics_merge.loc[olympics_merge['Team'].isnull(),['NOC', 'Team']].drop_duplicates())

# %%
olympics_merge.isnull().sum()

# %%
for i in ["Age","Height","Weight"]:
    sns.histplot(olympics_merge[i],kde=True)
    plt.show()

# %%
for i in ["Age","Weight",]:
    olympics_merge[i]=olympics_merge[i].fillna(olympics_merge[i].mean())

# %%
olympics_merge["Height"]=olympics_merge["Height"].fillna(olympics_merge["Height"].mean())

# %%
olympics_merge.isnull().sum()

# %%
olympics_merge.info()

# %%
olympics_merge['Sex']=np.where(olympics_merge['Sex']=='M',1,0)

# %%
olympics_merge.sample(2)

# %%
olympics_merge["Medal"].unique()

# %%
olympics_merge['Event'].unique()

# %%
olympics_merge['Sport'].unique()

# %%
olympics_merge1=olympics_merge

# %%
olympics_merge1

# %%
from sklearn.preprocessing import LabelEncoder 
le=LabelEncoder()

# %%
olympics_merge1['Medal']=le.fit_transform(olympics_merge1['Medal'])

# %%
olympics_merge1

# %%
olympics_merge1['Medal'].unique()

# %%
summer=olympics_merge1.loc[(olympics_merge1['Year']>1960)&(olympics_merge1['Season']=="Summer"), :]
summer.head(5)

# %%
summer=summer.reset_index()
summer.head(10)

# %%
summer.sample()

# %%
#extracting unique events in a new list

# %%
summerlistunique=summer.Event.unique()
len(summerlistunique)


# %%
summerlistunique

# %%
summer.drop(['Season'],axis=1,inplace=True)
summer.drop(['NOC'],axis=1,inplace=True)
summer.drop(['Games'],axis=1,inplace=True)
summer.drop(['City'],axis=1,inplace=True)
summer.drop(['Year'],axis=1,inplace=True)
summer.drop(['Sport'],axis=1,inplace=True)
summer.drop(['ID'],axis=1,inplace=True)
summer.drop(['Name'],axis=1,inplace=True)
summer.drop(['index'],axis=1,inplace=True)

# %%
summer

# %%
#created a column for encoded team and encoded events in numerical form in original dataset 
summer['Team_encode']=le.fit_transform(summer['Team'])
summer['Event_encode']=le.fit_transform(summer['Event'])

# %%
#storing the team names and corresponding encoded numerical values into a new csv file after sorting them according to team name 
TeamKeys=summer[['Team','Team_encode']].copy()
TeamKeys.drop_duplicates(subset="Team",inplace=True)
TeamKeys.to_csv("keystoteam.csv")

# %%
TeamKeys.head(4)

# %%
#storing event names and corresponding encoded numerical values into a new csv file after sorting them according to the event name
EventKeys=summer[['Event','Event_encode']].copy()
EventKeys.drop_duplicates(subset="Event",inplace=True)
EventKeys.to_csv("keystoevent.csv")

# %%
EventKeys.head(4)

# %%
summer

# %%
summer.drop(['Event'],axis=1,inplace=True)
summer.drop(['Team'],axis=1,inplace=True)

# %%
summer

# %%
y=summer['Medal']

# %%
y

# %%
x=summer.drop("Medal",axis=1)

# %%
x

# %%
X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size=0.30, random_state=99)

# %%
x

# %%
y

# %%
X_test

# %%
Y_test

# %%
#ALGORITHM 1 LOGISTIC REGRESSION 

# %%
lr=LogisticRegression()

lr.fit(X_train,Y_train)

Y_pred=lr.predict(X_test)

sk_report=classification_report(digits=6,y_true=Y_test,y_pred=Y_pred)
print("Accuracy",round(accuracy_score(Y_pred,Y_test)*100,2))
print(sk_report)
print(pd.crosstab(Y_test,Y_pred,rownames=['Actual'],colnames=['Predicted'],margins=True))

# %%
#ALGORITHM 2 DECESSION TREE

# %%
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, Y_train)
Y_pred = decision_tree.predict(X_test)
acc_decision_tree1 = round(decision_tree.score(X_test, Y_test) * 100, 2)
sk_report = classification_report(digits=6, y_true=Y_test, y_pred=Y_pred)
print("Accuracy", acc_decision_tree1)
print(sk_report)
### Confusion Matrix
print(pd.crosstab(Y_test, Y_pred,rownames=['Actual'],colnames=['Predicted'],margins=True))

# %%
#ALGORITHM 3 RANDOM FOREST

# %%
random_forest = RandomForestClassifier(n_estimators=200)
random_forest.fit(X_train,Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_test, Y_test)
acc_random_forest1=round(random_forest.score(X_test, Y_test)*100,2)
k_report = classification_report(
    digits=6,
    y_true=Y_test,
    y_pred=Y_pred)
print("Accuracy" , acc_random_forest1)
print(sk_report)
pd.crosstab(Y_test, Y_pred,rownames=['Actual'],colnames=['Predicted'],margins=True)

# %%
x.sample(5)

# %%
y.sample(5)

# %%
summer.sample(4)

# %%
random_forest.predict([[1,19.0,173.0,70.0,87,163]])

# %%
import pickle
from joblib import dump,load

dump(random_forest,'olympics_model.pkl')
model_file = open(r"D:\Anu George\Wahy labs\Projects\Olympics\olympics_model1.pkl","wb")
pickle.dump(random_forest,model_file)


