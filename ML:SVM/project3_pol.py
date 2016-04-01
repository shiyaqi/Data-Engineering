from scipy.io.arff import loadarff
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, auc, roc_curve
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt


data,meta = loadarff(open('uci-diabetes.arff','r'))
diab_y = np.array(data['class'])
train = np.array(data[['preg','plas','pres','skin','insu','mass','pedi','age']])
diab_X = np.asarray(train.tolist(), dtype=np.float32)


scaler=MinMaxScaler()
diab_X_scal = scaler.fit_transform(diab_X)


np.random.seed(0)
indices = np.random.permutation(len(diab_X))
diab_X_train = diab_X_scal[indices[:-256]]
diab_y_train = diab_y[indices[:-256]] 
diab_X_test = diab_X_scal[indices[-256:]] 
diab_y_test = diab_y[indices[-256:]]


parameters_pol = {'degree':[1,2,3,4], 'C':[1,10,100,1000,10000,100000]}
pol = svm.SVC(kernel= 'poly')
clf_pol= GridSearchCV(pol, parameters_pol)
clf_pol.fit(diab_X_train, diab_y_train)
diab_X_test_result_pol = clf_pol.predict(diab_X_test)
print "Best estimator:",clf_pol.best_estimator_


target = diab_y_test
prediction = diab_X_test_result_pol
accuracy = accuracy_score(target, prediction)
print "accuracy: ", accuracy
cm = confusion_matrix(target, prediction)
print "confusion matrix: \n", cm
report = classification_report(target, prediction)
print "classification_report: \n", report


y_score = clf_pol.fit(diab_X_train, diab_y_train).decision_function(diab_X_test)
fpr, tpr, thresholds = roc_curve(target,y_score, pos_label='tested_positive')
roc_auc = auc(fpr, tpr)
print "Area under the ROC curve : %f" % roc_auc


plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc, lw=4, color ="#ff00ff", marker='s',markerfacecolor="red") 
plt.plot([0, 1], [0, 1], 'k--') 
plt.xlim([-0.005, 1.0])  
plt.ylim([0.0, 1.005])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve of Polynomial')
plt.legend(loc="lower right")
plt.show()

