__author__ = 'Anna'
import numpy as np
import os
import sklearn.cross_validation as cv
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import sklearn.feature_selection as fs
from sklearn.grid_search import GridSearchCV
import sklearn.metrics as metrics
import matplotlib.pyplot as plt


if __name__ == '__main__':
    path = os.getcwd()[:-3]+ 'data.csv'
    datatypes = ('category',str),('congestive_heart_failure',int),
    data = np.genfromtxt(path, delimiter=",",skip_header=1)

    features = data[:,0:4]
    outcome = data[:,4]
    features_train, features_test, outcome_train, outcome_test = cv.train_test_split(features, outcome, test_size=0.3, random_state=2)

    scaler = StandardScaler().fit(features_train)
    scaled_features_train = scaler.transform(features_train)
    scaled_features_test = scaler.transform(features_test)

#Part1
#Classifiers
    logistic = LogisticRegression()
    native_bayes = GaussianNB()
    svr = svm.SVC(kernel='linear', probability = True)

#Feature Selection Methods
    #PCA
    pca = PCA()
    variance_ratio = pca.fit(scaled_features_train).explained_variance_ratio_
    print "variance_ratio:",variance_ratio #[ 0.2632312   0.25187499  0.24653997  0.23835384]

    #RFE
    rfe_logistic = fs.RFE(logistic, 1) #Change the number of features from 4 to 1
    rank_logistic = rfe_logistic.fit(scaled_features_train,outcome_train).ranking_
    print "rank_logistic:",rank_logistic
    # 4: [1 1 1 1]
    # 3: [1 2 1 1]
    # 2: [1 3 1 2]
    # 1: [2 4 1 3]

    rfe_svr = fs.RFE(svr, 1) #Change the number of features from 4 to 1
    rank_svr = rfe_svr.fit(scaled_features_train,outcome_train).ranking_
    print "rank_svr:",rank_svr
    # 4: [1 1 1 1]
    # 3: [1 1 1 2]
    # 2: [1 2 1 3]
    # 2: [2 3 1 4]

#Grid search for svc
    # Set parameter grid
    parameters = [{'C': [0.01, 0.1, 1, 10, 100, 1000],
                   'gamma': [0.0001,0.001, 0.01, 0.1, 1, 10],
                   'kernel': ['linear']},
                  {'C': [0.01, 0.1, 1, 10, 100, 1000],
                 'gamma': [0.0001,0.001, 0.01, 0.1, 1, 10],
                 'kernel': ['rbf']},
                  {'C': [0.01, 0.1, 1, 10, 100, 1000],
                  'gamma': [0.0001,0.001, 0.01, 0.1, 1, 10],
                  'degree': [2,3,4,5],
                  'kernel': ['poly']}]

    # Set empty classifier
    svr_grid = svm.SVC(probability = True)
    clf = GridSearchCV(svr_grid, parameters)
    clf.fit(scaled_features_train, outcome_train)
    support_vector = clf.best_estimator_
    print "best parameters:", clf.best_params_
    print "best estimator:", clf.best_estimator_

#Evaluate models of Naive Bayes, Logistic regression, Support vector for 4 and 3 features
    figurenum = 0
    for clf, name, the_color, selected_train, selected_test in [(native_bayes, 'Naive Bayes 4 features','red',
                                                               scaled_features_train,scaled_features_test),
                                                              (logistic, 'Logistic 4 features','blue',
                                                               scaled_features_train,scaled_features_test),
                                                              (support_vector, 'Support Vector 4 features','yellow',
                                                               scaled_features_train,scaled_features_test),
                                                              (native_bayes, 'Naive Bayes 3 features','red',
                                                               scaled_features_train[:,[0,2,3]],
                                                               scaled_features_test[:,[0,2,3]]),
                                                              (logistic,'Logistic 3 features','blue',
                                                               scaled_features_train[:,[0,2,3]],
                                                               scaled_features_test[:,[0,2,3]]),
                                                              (support_vector, 'Support Vector 3 features','yellow',
                                                               scaled_features_train[:,[0,2,3]],
                                                               scaled_features_test[:,[0,2,3]])]:
        clf.fit(selected_train,outcome_train)
        y_pred = clf.predict(selected_test)
        y_score = clf.predict_proba(selected_test)[:,1]

        #Evaluate the Classifications
        fpr, tpr, thresholds = metrics.roc_curve(outcome_test, y_score, pos_label=1)
        confusion = metrics.confusion_matrix(outcome_test, y_pred)
        TP = confusion[1, 1]
        TN = confusion[0, 0]
        FP = confusion[0, 1]
        FN = confusion[1, 0]
        sensitivity = TP/float(TP+FN)
        specificity = TN/float(FP+TN)
        accuracy = metrics.accuracy_score(outcome_test, y_pred)
        f1 = metrics.fbeta_score(outcome_test,y_pred,beta=1)
        AUC = metrics.roc_auc_score(outcome_test, y_score)

        #Plot the ROC
        figurenum += 1
        plt.figure(figurenum)
        plt.plot(fpr,tpr,color=the_color)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.xlim([0.0, 1.05])
        plt.ylim([0.0, 1.05])
        plt.title("Roc for %s"
                  % (name))
        plt.text(0.7,0.4,"sensitivity: %f, \nspecificit: %f, \naccuracy: %f, \nf1: %f, \nAUC: %f "
                  % (sensitivity,specificity,accuracy,f1,AUC))

##Part2
#Randome Forest
    rfc = RandomForestClassifier(n_estimators=100)
    for clf, name, the_color, selected_train, selected_test in [(rfc, 'Randome Forest 4 features','red',
                                                                scaled_features_train,scaled_features_test),
                                                                (rfc, 'Randome Forest 3 features(no los)','red',
                                                                scaled_features_train[:,[0,1,2]],
                                                                scaled_features_test[:,[0,1,2]])]:
        clf.fit(selected_train,outcome_train)
        y_pred = clf.predict(selected_test)
        y_score = clf.predict_proba(selected_test)[:,1]
        print name,rfc.feature_importances_

        #Evaluate the Classification
        fpr, tpr, thresholds = metrics.roc_curve(outcome_test, y_score, pos_label=1)
        confusion = metrics.confusion_matrix(outcome_test, y_pred)
        TP = confusion[1, 1]
        TN = confusion[0, 0]
        FP = confusion[0, 1]
        FN = confusion[1, 0]
        sensitivity = TP/float(TP+FN)
        specificity = TN/float(FP+TN)
        accuracy = metrics.accuracy_score(outcome_test, y_pred)
        f1 = metrics.fbeta_score(outcome_test,y_pred,beta=1)
        AUC = metrics.roc_auc_score(outcome_test, y_score)

        #Plot the ROC
        figurenum += 1
        plt.figure(figurenum)
        plt.plot(fpr,tpr,color=the_color)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.xlim([0.0, 1.05])
        plt.ylim([0.0, 1.05])
        plt.title("Roc for %s"
                  % (name))
        plt.text(0.7,0.4,"sensitivity: %f, \nspecificit: %f, \naccuracy: %f, \nf1: %f, \nAUC: %f "
                  % (sensitivity,specificity,accuracy,f1,AUC))
    plt.show()