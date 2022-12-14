
"""Natural Language Processing Project on Sentimental Analysis.ipynb

# Importing the libraries
"""

!pip install wordcloud

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re


# NLTK
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Wordcloud
from wordcloud import wordcloud


nltk.download('stopwords')
nltk.download('wordnet')

# Sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Evaluation Metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

!pip install scikit-plot

from scikitplot.metrics import plot_confusion_matrix

"""# Import the dataset

Link: https://www.kaggle.com/praveengovi/emotions-dataset-for-nlp?select=train.txt
"""

df_train = pd.read_csv('/content/drive/MyDrive/Datasets/archive/train.txt',delimiter=';', names=['text','label'])
df_val = pd.read_csv('/content/drive/MyDrive/Datasets/archive/val.txt', delimiter=';', names=['text','label'])

df_train

df_val

df = pd.concat([df_train, df_val])
df.reset_index(inplace=True, drop=True)

df.head()

df.tail()

df.shape

df.sample(5)

df.head(2)

df.label.unique()

df.label.value_counts()

df.label.value_counts().plot.bar()

# Positive Sentiments - Joy, Love, Surprise - 1
# Negative Sentiments - Anger, Sadness, Fear - 0

df.head()

df['label'].replace(to_replace=['surprise', 'joy', 'love'], value=1, inplace=True)
df['label'].replace(to_replace=['anger', 'sadness','fear'], value=0, inplace=True)

df.head(10)

df.label.value_counts()

df.label.value_counts().plot.bar()

df.head()

"""* Lemmatizer: https://www.geeksforgeeks.org/python-lemmatization-approaches-with-examples/"""

lm = WordNetLemmatizer()

def tranformation(df_column):
  output = []
  for i in df_column:
    new_text = re.sub('[^a-zA-Z]',' ',str(i))
    new_text = new_text.lower()
    new_text = new_text.split()
    new_text = [lm.lemmatize(j) for j in new_text if j not in set(stopwords.words('english'))]
    output.append(' '.join(str(k) for k in new_text))
  
  return output

var = tranformation(df.text)

var

from wordcloud import WordCloud

# Word Cloud
plt.figure(figsize=(50,28))
word = ''
for i in var:
  for j in i:
    word += " ".join(j)

wc = WordCloud(width=1000, height= 500, background_color='white', min_font_size=10).generate(word)
plt.imshow(wc)

# Bag of Words model (BOW)

cv = CountVectorizer(ngram_range=(1,2))
traindata = cv.fit_transform(var)
X_train = traindata
y_train = df.label

X_train

model = RandomForestClassifier()

# Hyper Parameter Tuning

parameters = {'max_features':('auto', 'sqrt'),
              'n_estimators': [500, 1000, 1500],
              'max_depth': [5,10, None],
              'min_samples_leaf':[1, 2, 5, 10],
              'min_samples_split':[5, 10, 15],
              'bootstrap':[True, False]}

parameters

grid_search = GridSearchCV(model, 
                           parameters, 
                           cv=5,
                           return_train_score = True,
                           n_jobs=1)

grid_search.fit(X_train, y_train)

grid_search.best_params_

rfc = RandomForestClassifier(max_features= grid_search.best_params_['max_features'],
                             n_estimators= grid_search.best_params_['n_estimators'],
                             max_depth= grid_search.best_params_['max_depth'],
                             min_samples_leaf= grid_search.best_params_['min_samples_leaf'],
                             min_samples_split= grid_search.best_params_['min_samples_split'],
                             bootstrap= grid_search.best_params_['bootstrap'])

rfc.fit(X_train, y_train)

test_data = 
X_test, y_test

y_pred = rfc.predict(X_test)

# Model Evaluation
accuracy_score(y_test, y_pred)

def sentimental_analysis(input):
  new_input = tranformation(input)
  transformed_input = cv.transform(new_input)
  prediction = rfc.predict(transformed_input)
  if prediction == 0:
    print('Negative Sentiment')
  elif prediction == 1:
    print('Positive Sentiment')
  else:
    print('Invalid Sentiment')

input = "Today I was playing in the park and I fell"
inp = input("")

sentimental_analysis(inp)
