# Lab 8 #
## Part1 ##
### Introduction
In the "Classifiers and Parameter" section, I compared the performance of each classification model based on the result of feature selection.
Because variance of each features are vary similar to each other(from PCA), and all the features are ranked as important when preforming RFE,
I expect all models will have better performance when trained with 4 features, however, for logistic regression, there is no significant difference
between 3 features and 4 features. A further discussion is conduct under the section of "Feature Selections" regards to the conflict between my assumption
and observation. 

### Classifiers and Parameter ###
 1. Naive Bayes
   * 4 features : ![Naive Bayes 4 features](/img/figure_1.png)
   * 3 features with no ctm2 : ![Naive Bayes 3 features](/img/figure_4.png)
   * Observation: All metrics are improved when trained with 4 features.
   * Limitation of Naive Bayes: Native Bayes assume each features are not correlated, thus, if trained with features what are correlated to 
    each other, the weights of the features which are correlated will be double counted in the model. In this data set, there is no strong
    correlations among features.(see correlations below) 
 2. Logistic Regression
   * 4 features : ![Logistic Regression 4 features](/img/figure_2.png)
   * 3 features with no ctm2 : ![Logistic Regression 3 features](/img/figure_5.png)
   * Observation: Only AUC is slightly improved, the rest of metrics are not improved when trained with 4 features.  
 3. Support Vector 
   * Grid search is used to choose the best parameters
   * best estimator: SVC(C=1000, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma=0.01, kernel='rbf',
  max_iter=-1, probability=True, random_state=None, shrinking=True,
  tol=0.001, verbose=False)
   * kernel: rbf
   * C: 1000
   * gamma: 0.01
   * 4 features : ![Support Vector 4 features](/img/figure_3.png)
   * 3 features with no ctm2 : ![Support Vector 3 features](/img/figure_6.png)
   * * Observation: All metrics expect sensitivity are improved when trained with 4 features.
   
   
### Feature Selections
Two methods are used for feature Selections: Principal component analysis (PCA) and Recursive Feature Elimination (RFE).
 
 1. PCA
   * explained variance ratio: 0.2632312,  0.25187499, 0.24653997, 0.23835384
   * All features carry vary similar variance, with 'cmt1' has the most variance and 'length of stay' has the least variance.
 2. RFE 
   * The feature ranking by using support vector with linear kernel vs logistic regression . The ranking represts when 4,3,2,1 features are selected
    
    support vector vs logistic regression
     
     4: [1 1 1 1]  vs 4: [1 1 1 1]
     
     3: [1 1 1 2]  vs 3: [1 2 1 1]
   
     2: [1 2 1 3]  vs 2: [1 3 1 2]
    
     1: [2 3 1 4]  vs 1: [2 4 1 3]
   * When 4 features are selected, RFE ranks all the features as equally important. This results is in line with the result of PCA which shows similar variances for all features . 
   * When 3 features are selected, using logistic regression will drop 'ctm2' whereas using support vector with linear kernel will drop 'length of stay'.
     
     From the previous result that we get from PCA, it is easy to understand that since 'length of stay' has the smallest variance(0.238) among all the features,
   it will be more likely dropped by RFE. 
     
     Surprisingly, cmt2, which carries the 2nd large variance are supposed to be ranked as more important 
   than 'age' and 'length of stay', is dropped by RFE when doing logistic regression. In order to explore the reason for this, we should look at the 
   correlations between features with the outcome[(The result is from explore_lab8.R file)](/explore_lab8.R). 
   
                            ctm2         age         los      outcome        ctm1
               ctm2     1.000000000 0.005175999 0.017086237 -0.001908418 0.008931643
               age      0.005175999 1.000000000 0.024405957  0.671186343 0.004103147
               los      0.017086237 0.024405957 1.000000000  0.010523374 0.006062019
               outcome -0.001908418 0.671186343 0.010523374  1.000000000 0.011641440
               ctm1     0.008931643 0.004103147 0.006062019  0.011641440 1.000000000
   Because logistic regression essentially is a linear model between features and the log probability of outcome, the correlation between each
   feature and the outcome will indicate the significant level of each feature. As we see from the result above, even though 'ctm2' has a variance of
   0.252, it has the least correlation(0.0019) with outcome, thus it is understandable why ctm2 is the least important feature when using logistic model
   to do RFE. 
   * When 2 features or 1 feature are selected, the most important feature is 'age' for both logistic and Support vector model. This result is in line
    with the correlations that we got, that 'age' has the strongest positive correlation with the outcome. 
    
      This also indicates that although PCA is good for exploring how spread out the data is on each dimension, it does not reflect the correlation between each dimension and the outcome. 
    A feature with large variance carries a lot of information but may have a weak correlation with the the outcome. Additionally, Simpson paradox indicates
    ['a trend appears in different groups of data but disappears or reverses when these groups are combined'](https://en.wikipedia.org/wiki/Simpson%27s_paradox),
    further analysis can be done on 'ctm2' to see if the simpson paradox exist on that dimension. 
    
#### Conclusion for Part 1 ####
  1. Adding feature 'ctm2' will improve the performance of Support Vector Machine with kernel of RBF and Naive Bayes model. 
  2. 'ctm2' has a correlation with the outcome close to 0, thus, logistic regression shows similar performances when using 4 features and using 3 features without 'ctm2'.
  3. PCA can be used to reduce the features that have small variance, it is insufficient to demonstrate the correlation between features and outcomes.
  4. SFE can be used to reduce the features that have the weakest correlation between features and outcome.   
   
## Part2 
### Classifiers and Parameter ###
1. Random Forest                                                             
  * 4 features : ![Random forest 4 features](/img/figure_rfc-4.png)  
  * 3 features with no 'length of stay' : ![Random forest 3 features](/img/figure_rfc-3.png)  
  * Parameter for both 4 and 3 features are : n_estimators=100
  * Observation: Trained with 3 features(with no 'length of stay') has slightly better performance than 4 features. This is because 
   random forest is overfitted with redundant information. 
    
2. Which features are "most" important?  That is, based on your interpretation
   of the random forest output, would you choose to select only a subset of
   features if you were to use another model such as a support vector machine? 
  * 4 features: feature importance : 0.20755659,  0.20583559,  0.53251126,  0.05409655 
    
     'age' is the most important feature and 'length of stay' is the least important feature.
   
  * Based on the result of random forest, I reduced the feature 'length of stay'. The performance of the model are vary close with 4 features
  and 3 features. Thus, I will suggest to use 3 features without 'length of stay' to train the random forest model to achieve a better performance with 
  a lower cost. 