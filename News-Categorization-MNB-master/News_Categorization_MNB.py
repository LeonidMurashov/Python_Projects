
# coding: utf-8

# # News Categorization using Multinomial Naive Bayes
# ## by Andrés Soto

# Once upon a time, while searching by internet, I discovered [this site](https://www.kaggle.com/uciml/news-aggregator-dataset), where I found this challenge: 
# * Using the News Aggregator Data Set, can we predict the category (business, entertainment, etc.) of a news article given only its headline? 
# So I decided to try to do it using the Multinomial Naive Bayes method.

# The News Aggregator Data Set comes from the UCI Machine Learning Repository. 

# * Lichman, M. (2013). [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml). Irvine, CA: University of California, School of Information and Computer Science. 

# This specific dataset can be found in the UCI ML Repository at [this URL](http://archive.ics.uci.edu/ml/datasets/News+Aggregator).

# This dataset contains headlines, URLs, and categories for 422,937 news stories collected by a web aggregator between March 10th, 2014 and August 10th, 2014. News categories in this dataset are labelled:

# Label  |  Category	| News 
# -------|------------|----------
# b	|  business	|  <div style="text-align: right"> 115967 </div>
# t	|  science and technology	|  <div style="text-align: right"> 108344 </div> 
# e	| entertainment	|  <div style="text-align: right"> 152469 </div>
# m	|  health	|  <div style="text-align: right"> 45639 </div> 

# Multinomial Naive Bayes method will be used to predict the category (business, entertainment, etc.) of a news article given only its headline. The paper is divided in four sections. The first section is dedicated to importing the data set and getting some preliminary information about it. Second section explains how to divide data in two sets: the training set and the test set. Section number 3 is about training and testing the classification algorithm and obtaining results. Results analysis constitute the last section. 

# ## Import data

# To import the data from the CSV file, we will use [Pandas library](http://pandas.pydata.org/) which also offers data structures and operations for manipulating data tables. Therefore, we need to import Pandas library. 

# To embed plots inside the Notebook, we use the "%matplotlib inline" [magic command](http://ipython.readthedocs.io/en/stable/interactive/magics.html#).

# In[1]:

get_ipython().magic('matplotlib inline')
import pandas as pd 


# Now, we have to initialize some variables that will be used. They will be used to collect the news titles, its categories, as well as a list of the different possible categories (without repetitions).

# In[2]:

titles = [] # list of news titles
categories = [] # list of news categories
labels = [] # list of different categories (without repetitions)
nlabels = 4 # number of different categories
lnews = [] # list of dictionaries with two fields: one for the news and 
            # the other for its category


# The code for this section will be organized in two functions: one which imports the data and the other which counts the news in each category, its percentage and plots it. 

# In[3]:

def import_data():
    global titles, labels, categories
    # importing news aggregator data via Pandas (Python Data Analysis Library)
    news = pd.read_csv("uci-news-aggregator.csv")
    # function 'head' shows the first 5 items in a column (or
    # the first 5 rows in the DataFrame)
    print(news.head())
    categories = news['CATEGORY']
    titles = news['TITLE']
    labels = sorted(list(set(categories)))    


# Let's see how long it takes to import the data by %time [magic command](https://ipython.org/ipython-doc/3/interactive/magics.html).

# In[4]:

get_ipython().magic('time import_data()')


# The time to import the dat was 3.54 seconds. Let's analyze how many news we have from the different categories and its percentage. We will use the [class Counter](https://docs.python.org/3/library/collections.html#counter-objects) from the collections library, which keeps track of how many values contains a collection. Then we will tabulate the different categories and its percentage via a DataFrame.

# In[5]:

from collections import Counter

def count_data(labels,categories):    
    c = Counter(categories)
    cont = dict(c)
    # total number of news
    tot = sum(list(cont.values()))     
    d = {
        "category" : labels,
        "news" : [cont[l] for l in labels],
        "percent" : [cont[l]/tot for l in labels]
    }
   
    print(pd.DataFrame(d))   
    print("total \t",tot) 
    
    return cont

cont = count_data(labels,categories)


# Let's show a [pie plot](http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py) with the proportion of news by category.

# In[6]:

import pylab as pl # useful for drawing graphics

def categories_pie_plot(cont,tit):
    global labels
    sizes = [cont[l] for l in labels]
    pl.pie(sizes, explode=(0, 0, 0, 0), labels=labels,
        autopct='%1.1f%%', shadow=True, startangle=90)
    pl.title(tit)
    pl.show()
    
categories_pie_plot(cont,"Plotting categories")


# As we can see, the entertainment (e) category is the biggest one, which is more than three times bigger than health (m) category. In second place we have business (b) and technology (t), which are more than two times bigger than health category.

# ## Splitting the data 

# Now we should split our data into two sets:
# 1. a training set (70%) used to discover potentially predictive relationships, and
# 2. a test set (30%) used to evaluate whether the discovered relationships hold and to assess the strength and utility of a predictive relationship.

# Before splitting it, the data should be first permuted. [Shuffle](http://scikit-learn.org/stable/modules/generated/sklearn.utils.shuffle.html) is a method included in scikit-learn library which allows to do random permutations of collections. Then data could be splitted into a pair of train and test sets.

# In[7]:

from sklearn.utils import shuffle # Shuffle arrays in a consistent way

X_train = []
y_train = []
X_test = []
y_test = []

def split_data():
    global titles, categories
    global X_train, y_train, X_test, y_test,labels
    N = len(titles)
    Ntrain = int(N * 0.7)    
    # Let's shuffle the data
    titles, categories = shuffle(titles, categories, random_state=0)
    X_train = titles[:Ntrain]
    y_train = categories[:Ntrain]
    X_test = titles[Ntrain:]
    y_test = categories[Ntrain:]


# In[8]:

get_ipython().magic('time split_data()')


# Time required to split data is 1.28 seconds. Now let's analyze the proportion of news categories in the training set.

# In[9]:

cont2 = count_data(labels,y_train)


# Percentage are very much close to the ones obtained for the whole data set. 

# In[10]:

categories_pie_plot(cont2,"Categories % in training set")


# ## Train and test the classifier

# In order to train and test the classifier, the first step should be to tokenize and count the number of occurrence of each word that appears into the news'titles using for that [CountVectorizer class](http://scikit-learn.org/stable/modules/feature_extraction.html#common-vectorizer-usage). Each term found is assigned a unique integer index.
# Then the counters will be transformed to a TF-IDF representation using [TfidfTransformer class](http://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting). The last step creates the [Multinomial Naive Bayes classifier](http://scikit-learn.org/stable/modules/naive_bayes.html#multinomial-naive-bayes). 
# In order to make the training process easier, scikit-learn provides a [Pipeline class](http://scikit-learn.org/stable/modules/pipeline.html) that behaves like a compound classifier. 
# The [metrics module](http://scikit-learn.org/stable/modules/classes.html) allows to calculate score functions, performance metrics and pairwise metrics and distance computations. F1-score can be interpreted as a weighted average of the [precision and recall](https://en.wikipedia.org/wiki/Precision_and_recall).

# In[11]:

from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.naive_bayes import MultinomialNB 
from sklearn.pipeline import Pipeline 
from sklearn import metrics 
import numpy as np
import pprint

# lmats = [] # list of confussion matrix 
nrows = nlabels
ncols = nlabels
# conf_mat_sum = np.zeros((nrows, ncols))
# f1_acum = [] # list of f1-score

def train_test():
    global X_train, y_train, X_test, y_test, labels 
    #lmats, \
     #       conf_mat_sum, f1_acum, ncategories
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),
                         ])
    text_clf = text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)
    return predicted


# In[12]:

get_ipython().magic('time predicted = train_test()')


# To compare the predicted labels to the corresponding set of true labels we will use the [method accuracy_score from scikit-learn](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html), which gives an accuracy over 0.92

# In[13]:

metrics.accuracy_score(y_test, predicted)


# To show the main classification metrics we will use the [classification_report method](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html) from scikit-learn.

# In[14]:

print(metrics.classification_report(y_test, predicted, target_names=labels))


# We can see that, although the metrics (precision, recall and f1-score) in average give us 0.92, the results for category e (entertainment) are even better.

# [Confusion matrix](http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html) allows to detect if a classification algorithm is confusing two or more classes if you have an unequal number of observations in each class as in this case. An ideal classifier with 100% accuracy would produce a pure diagonal matrix which would have all the points predicted in their correct class. In case of class imbalance, confusion matrix normalization by class support size (number of elements in each class) can be interesting in order to have a visual interpretation of which class is being misclassified.

# In[15]:

mat = metrics.confusion_matrix(y_test, predicted,labels=labels)
cm = mat.astype('float') / mat.sum(axis=1)[:, np.newaxis]
cm


# Let's print a plot for the confussion matrix.

# In[16]:

import itertools
import matplotlib.pyplot as plt

def plot_confusion_matrix(cm, classes,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, '{:5.2f}'.format(cm[i, j]),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.colorbar()
    plt.show()


# In[17]:

plot_confusion_matrix(cm, labels, title='Confusion matrix')


# Confussion matrix columns represent the instances in a predicted class while rows represent the instances in an actual class. The diagonal elements represent the number of points for which the predicted label is equal to the true label, while off-diagonal elements are those that are mislabeled by the classifier. The higher the diagonal values of the confusion matrix the better, indicating many correct predictions.

# Now, let's see the relation between [f1-score](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html) and the percentage by category

# In[18]:

def resume_data(labels,y_train,f1s):
    c = Counter(y_train)
    cont = dict(c)
    tot = sum(list(cont.values()))
    nlabels = len(labels)
    d = {
        "category" : [labels[i] for i in range(nlabels)],
        "percent" : [cont[labels[i]]/tot for i in range(nlabels)],
        "f1-score" : [f1s[i] for i in range(nlabels)]
    }
   
    print(pd.DataFrame(d))   
    print("total \t",tot) 
    return cont


# In[19]:

f1s = metrics.f1_score(y_test, predicted, labels=labels, average=None)
cont3 = resume_data(labels,y_train,f1s)


# ## Results analysis

# As a resume, results show a good accuracy (0.9238) with a good average level for precision, recall and f1-score (0.92) Analyzing these results by category, results are even better for the entertainment category ('e') with 0.96 for f1-score, 0.97 for recall and 0.95 for precision. I would like to highlight that best result for prediction corresponds to health category ('m') with 0.97, but with a recall of 0.85. Other categories show a more even behavior.  
# Analyzing confusion matrix results, the higher index of points predicted in their correct class for category 'e' with 0.9719. This category presents a misclassification index of 0.014 for technology category ('t') and lower indexes for the other categories.
# On the contrary, category 'm' presents the worst hit rate with an indicator of 0.846, which has misclassification indexes of 0.062 with business category ('b'), of 0.0619 with category 'e' and of 0.03 with category 't'.
# Analyzing the number of news by category, category 'e' presents the higher percentage, 36%, with 45625 news. On the other hand, category 'm' presents the lower percentage, 10.79%, with just 13709 news. Thus, category 'e' is more than three times bigger than category 'm'. Categories 'b' and 't' present similar number of news and percentage: 'b' has 34729 news with 27%, and 't' has 32663 news with a 25%. Both categories, 'b' and 't', are more than two times bigger than category 'm'. According to these, better results seem to correspond with higher percentage categories. In future experiments, I would try to confirm this hypothesis.
# In this experience, we just trained the classification algorithm with one set of data, so we just have one set of results. Although the training set and the test set were selected by random, it is just a sample of the possible results. In future experiments, I would try to test which is the confidence of the experiment results. 
