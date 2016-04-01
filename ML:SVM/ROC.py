import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# For ROC curves, scores predicted by SVMs, can either be probability estimates of the positive class or confidence values.
#y_pred = svc.predict_proba(diabetes_X_test) # tests the classifier on the test set
#y_pred = svc.decision_function(diabetes_X_test) # tests the classifier on the test set
# decision_function (distance from class boundary) is better to use than predict_proba
#   (prob of belonging in either class)

# Here we have continuous values, such as would be returned from prediction on diabetes data set 
#  with svc.predict_proba and svc.decision_function, but not with svc.predict
prediction = np.array([.1, .19, .29, .39, .49, .59, .69, .79, .89, .99])
target = np.array(['tested_negative','tested_negative','tested_negative','tested_positive','tested_positive','tested_negative','tested_negative','tested_positive','tested_positive','tested_positive'])
fpr, tpr, thresholds = roc_curve(target, prediction, pos_label='tested_positive')

#Note that when the target values are integers you don't need to pass in pos_label
#target = np.array([0,0,0,1,1,0,0,1,1,1])
#fpr, tpr, thresholds = roc_curve(target, prediction)

print thresholds

roc_auc = auc(fpr, tpr)
print "Area under the ROC curve : %f" % roc_auc

# ROC Curve
# Recall (aka sensitivity) is TP rate, is fraction of actual pos that are predicted pos 
#     is on y-axis of ROC curve  TP rate =  TP / actual pos
# FP Rate (NOT precision) = is fraction of actual neg that are predicted pos, is 1-specificiy
#     is on x-axis of ROC curve: FP Rate = FP/ actual neg  = 1-TN_rate= 1-(TN/actual neg) 

# Plot 
plt.figure()
#plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc, lw=4 ) # plot ROC curve
# see color chart using hexadecimal RGB code: http://www.rapidtables.com/web/color/RGB_Color.htm
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc, lw=4, color ="#0000ff", marker='s',markerfacecolor="red") # color specified in hex RGB code

plt.plot([0, 1], [0, 1], 'k--') # also plot black dashed line (k=black) from (0,0) to (1,1)

# Set x and y ranges, labels, title and legend
plt.xlim([-0.005, 1.0])  #x range basically from 0 to 1: start range a bit to left of min x value to see thick line better
plt.ylim([0.0, 1.005])   #0 range basically from 0 to 1: extend range a bit above max y value to see thick line better
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()



