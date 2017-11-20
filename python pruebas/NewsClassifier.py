#!/usr/bin/python
import os, sys
import glob
import json

pathDataBBC = 'C:/Users/Carlo/Desktop/TFG/TFG/python pruebas/News data-sets from BBC'
pathDataWebhose = 'C:/Users/Carlo/Desktop/TFG/TFG/python pruebas/Test data sets from BBC and New york times'
listAllNews = []
ListAllTest = []

#Data-set from BBC.
#Data,We will use 0 for business, 1 for Entertainment and so on
for filename in os.listdir(pathDataBBC + "/business"):
    file = open(pathDataBBC + "/business/" + filename, "r") 
    listAllNews += [(file.read(),0)]
    
for filename in os.listdir(pathDataBBC + "/entertainment"):
    file = open(pathDataBBC + "/entertainment/" + filename, "r") 
    listAllNews += [(file.read(),1)]

for filename in os.listdir(pathDataBBC + "/politics"):
    file = open(pathDataBBC + "/politics/" + filename, "r") 
    listAllNews += [(file.read(),2)]

for filename in os.listdir(pathDataBBC + "/sport"):
    file = open(pathDataBBC + "/sport/" + filename, "r") 
    listAllNews += [(file.read(),3)]

for filename in os.listdir(pathDataBBC + "/tech"):
    file = open(pathDataBBC + "/tech/" + filename, "r") 
    listAllNews += [(file.read(),4)]

#Test,We will use 0 for business, 1 for Entertainment and so on
for filename in os.listdir(pathDataBBC+ "/business_test"):
    file = open(pathDataBBC + "/business_test/" + filename, "r") 
    ListAllTest += [(file.read(),0)]
    
for filename in os.listdir(pathDataBBC+ "/entertainment_test"):
    file = open(pathDataBBC + "/entertainment_test/" + filename, "r") 
    ListAllTest += [(file.read(),1)]

for filename in os.listdir(pathDataBBC+ "/politics_test"):
    file = open(pathDataBBC + "/politics_test/" + filename, "r") 
    ListAllTest += [(file.read(),2)]

for filename in os.listdir(pathDataBBC+ "/sport_test"):
    file = open(pathDataBBC + "/sport_test/" + filename, "r") 
    ListAllTest += [(file.read(),3)]

for filename in os.listdir(pathDataBBC+ "/tech_test"):
    file = open(pathDataBBC + "/tech_test/" + filename, "r") 
    ListAllTest += [(file.read(),4)]

#Uncomment for the data-set from webhose
""" 
for filename in os.listdir(pathDataWebhose + "/Train_tech"):
    try:
        jsonFile = open(pathTest + "/Train_tech/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        listAllNews += [(values["text"],4)]
    except ValueError:
        pass
    
for filename in os.listdir(pathDataWebhose + "/Train_politics"):
    try:
        jsonFile = open(pathTest + "/Train_politics/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        listAllNews += [(values["text"],2)]
    except ValueError:
        pass
    
for filename in os.listdir(pathDataWebhose + "/Train_financial"):
    try:
        jsonFile = open(pathTest + "/Train_financial/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        listAllNews += [(values["text"],0)]
    except ValueError:
        pass

for filename in os.listdir(pathDataWebhose + "/Train_entertainment"):
    try:
        jsonFile = open(pathTest + "/Train_entertainment/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        listAllNews += [(values["text"],1)]
    except ValueError:
        pass

for filename in os.listdir(pathDataWebhose + "/Test_tech"):
    try:
        jsonFile = open(pathTest + "/Test_tech/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        ListAllTest += [(values["text"],4)]
    except ValueError:
        pass
    
for filename in os.listdir(pathDataWebhose + "/Test_politics"):
    try:
        jsonFile = open(pathTest + "/Test_politics/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        ListAllTest += [(values["text"],2)]
    except ValueError:
        pass
    
for filename in os.listdir(pathDataWebhose + "/Test_financial"):
    try:
        jsonFile = open(pathTest + "/Test_financial/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        ListAllTest += [(values["text"],0)]
    except ValueError:
        pass

for filename in os.listdir(pathDataWebhose + "/Test_entertainment"):
    try:
        jsonFile = open(pathTest + "/Test_entertainment/" + filename, "r")
        values = json.load(jsonFile)
        jsonFile.close()
        ListAllTest += [(values["text"],1)]
    except ValueError:
        pass
"""


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
text_clf = text_clf.fit([x[0] for x in listAllNews], [x[1] for x in listAllNews])



import numpy as np
predicted = text_clf.predict([x[0] for x in ListAllTest])
print (np.mean(predicted == [x[1] for x in ListAllTest]))

from sklearn.linear_model import SGDClassifier
text_clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                         ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, max_iter=5, random_state=42))])

text_clf_svm = text_clf_svm.fit([x[0] for x in listAllNews], [x[1] for x in listAllNews])
predicted_svm = text_clf_svm.predict([x[0] for x in ListAllTest])
print (np.mean(predicted_svm == [x[1] for x in ListAllTest]))

from sklearn.model_selection import GridSearchCV
parameters_svm = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False),'clf-svm__alpha': (1e-2, 1e-3)}

gs_clf_svm = GridSearchCV(text_clf_svm, parameters_svm, n_jobs=-1)
gs_clf_svm = gs_clf_svm.fit([x[0] for x in listAllNews], [x[1] for x in listAllNews])


print (gs_clf_svm.best_score_)
print (gs_clf_svm.best_params_)

    
