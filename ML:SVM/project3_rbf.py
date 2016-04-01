from scipy.io.arff import loadarff
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report,auc,roc_curve
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


parameters_rbf = {'gamma':[0.001,0.01,0.1,1,10,100], 'C':[1,10,100,1000,10000,100000,1000000]}
rbf = svm.SVC(kernel= 'rbf')
clf_rbf= GridSearchCV(rbf, parameters_rbf)
clf_rbf.fit(diab_X_train, diab_y_train)
diab_X_test_result_rbf = clf_rbf.predict(diab_X_test)
print clf_rbf.best_estimator_


target = diab_y_test
prediction = diab_X_test_result_rbf
accuracy = accuracy_score(target, prediction)
print "accuracy: ", accuracy
cm = confusion_matrix(target, prediction)
print "confusion matrix: \n", cm
report = classification_report(target, prediction)
print "classification_report: \n", report


y_score = clf_rbf.fit(diab_X_train, diab_y_train).decision_function(diab_X_test)
fpr, tpr, thresholds = roc_curve(target,y_score, pos_label='tested_positive')
roc_auc = auc(fpr, tpr)
print "Area under the ROC curve : %f" % roc_auc


plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc, lw=4, color ="#0000ff", marker='s',markerfacecolor="red") 
plt.plot([0, 1], [0, 1], 'k--') 
plt.xlim([-0.005, 1.0])  
plt.ylim([0.0, 1.005])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve of RBF')
plt.legend(loc="lower right")
plt.show()



