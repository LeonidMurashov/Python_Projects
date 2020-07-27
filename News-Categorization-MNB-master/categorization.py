"""
Author: Andrés Soto Villaverde
The objective of this program is to show how to use Multinomial Naive Bayes
method to classify news according to some predefined classes.
The News Aggregator Data Set comes from the UCI Machine Learning Repository.
Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml].
Irvine, CA: University of California, School of Information and Computer Science.
This specific dataset can be found in the UCI ML Repository at this URL:
http://archive.ics.uci.edu/ml/datasets/News+Aggregator
"""

# importing useful libraries
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# importing news aggregator data via Pandas (Python Data Analysis Library)
news = pd.read_csv("uci-news-aggregator.csv")
# function head gives us the first 5 items in a column (or
# the first 5 rows in the DataFrame)
print(news.head())
# we want to predict the category of a news article based only on its title

categories = news['CATEGORY']
titles = news['TITLE']
N = len(titles)
print('Number of news',N)
labels = list(set(categories))
print('possible categories',labels)
for l in labels:
    print('number of ',l,' news',len(news.loc[news['CATEGORY'] == l]))

# categories are literal labels, but it is better for
# machine learning algorithms just to work with numbers, so we will
# encode them
# LabelEncoder: encode labels with value between 0 and n_classes-1.
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
ncategories = encoder.fit_transform(categories)

# Now we should split our data into two sets:
# 1) a training set which is used to discover potentially predictive relationships, and
# 2) a test set which is used to evaluate whether the discovered relationships
#    hold and to assess the strength and utility of a predictive relationship.
Ntrain = int(N * 0.7)
from sklearn.utils import shuffle
titles, ncategories = shuffle(titles, ncategories, random_state=0)

X_train = titles[:Ntrain]
print('X_train.shape',X_train.shape)
y_train = ncategories[:Ntrain]
print('y_train.shape',y_train.shape)
X_test = titles[Ntrain:]
print('X_test.shape',X_test.shape)
y_test = ncategories[Ntrain:]
print('y_test.shape',y_test.shape)

# CountVectorizer implements both tokenization and occurrence counting
# in a single class
from sklearn.feature_extraction.text import CountVectorizer
# TfidfTransformer: Transform a count matrix to a normalized tf or tf-idf
# representation
from sklearn.feature_extraction.text import TfidfTransformer
# MultinomialNB: implements the naive Bayes algorithm for multinomially
# distributed data, and is one of the two classic naive Bayes variants
# used in text classification
from sklearn.naive_bayes import MultinomialNB
# Pipeline: used to chain multiple estimators into one.
# All estimators in a pipeline, except the last one,
# must be transformers (i.e. must have a transform method).
# The last estimator may be any type (transformer, classifier, etc.).
from sklearn.pipeline import Pipeline
print('Training...')

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
                     ])
# clf.fit: Fit Naive Bayes classifier according to X, y
text_clf = text_clf.fit(X_train, y_train)
print('Predicting...')
# clf.predict: Perform classification on an array of test vectors X.
predicted = text_clf.predict(X_test)

# sklearn.metrics module includes score functions, performance metrics
# and pairwise metrics and distance computations.
from sklearn import metrics
# accuracy_score: computes subset accuracy; used to compare set of
#       predicted labels for a sample to the corresponding set of true labels
print('accuracy_score',metrics.accuracy_score(y_test,predicted))
print('Reporting...')

# classification_report: Build a text report showing the main classification metrics
print(metrics.classification_report(y_test, predicted, target_names=labels))