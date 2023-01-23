from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import json


class ML_Methods:
    
    def __init__(self, dataset, type_):
        self.dataset = dataset
        self.type_ = type_
        self.metrics = []
        
    def run(self):
        
        if self.type_ == "lr":
            self.metrics.append(self.logistic_regression(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
        if self.type_ == "dt":
            self.metrics.append(self.decision_tree(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
        if self.type_ == "rf":
            self.metrics.append(self.random_forest(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
        if self.type_ == "svm":
            self.metrics.append(self.SVM(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
        if self.type_ == "all":
            self.metrics.append(self.logistic_regression(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
            self.metrics.append(self.decision_tree(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
            self.metrics.append(self.random_forest(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
            self.metrics.append(self.SVM(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3]))
        return self.metrics
    
    
    def logistic_regression(self,x_train,y_train,x_test,y_test):

        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        log_reg= LogisticRegression(penalty='l2', tol=0.0001, max_iter=100000, C=1,random_state=42)
        log_reg.fit(x_train_flatten, y_train_flatten)
        y_pred = log_reg.predict(x_test_flatten)
        prec = precision_score(y_test, y_pred,pos_label='positive', average='micro')
        recall = recall_score(y_test, y_pred,pos_label='positive', average='micro')
        f_score = f1_score(y_test, y_pred,pos_label='positive', average='micro')
        accuracy = accuracy_score(y_test, y_pred)
        print({"precision":prec,"recall":recall,"F1-score":f_score,"Accuracy":accuracy})
        return {"LR_precision":prec,"LR_recall":recall,"LR_F1-score":f_score,"LR_Accuracy":accuracy}


    def decision_tree(self,x_train,y_train,x_test,y_test):
        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        clf= tree.DecisionTreeClassifier(max_depth=30,random_state=0,criterion='entropy')
        clf.fit(x_train_flatten,y_train_flatten)
        #fin_acc = clf.score(x_test_flatten,y_test_flatten)
        y_pred = clf.predict(x_test_flatten)
        prec = precision_score(y_test, y_pred,pos_label='positive', average='micro')
        recall = recall_score(y_test, y_pred,pos_label='positive', average='micro')
        f_score = f1_score(y_test, y_pred,pos_label='positive', average='micro')
        accuracy = accuracy_score(y_test, y_pred)
        print({"precision":prec,"recall":recall,"F1-score":f_score,"Accuracy":accuracy})
        return {"DT_precision":prec,"DT_recall":recall,"DT_F1-score":f_score,"DT_Accuracy":accuracy}
        


    def random_forest(self,x_train,y_train,x_test,y_test):
        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        clf  = RandomForestClassifier(n_estimators=100)

        # fit the training data to the model
        clf.fit(x_train_flatten, y_train_flatten)
        y_pred = clf.predict(x_test_flatten)
        prec = precision_score(y_test, y_pred,pos_label='positive', average='micro')
        recall = recall_score(y_test, y_pred,pos_label='positive', average='micro')
        f_score = f1_score(y_test, y_pred,pos_label='positive', average='micro')
        accuracy = accuracy_score(y_test, y_pred)
        print({"precision":prec,"recall":recall,"F1-score":f_score,"Accuracy":accuracy})
        return {"RF_precision":prec,"RF_recall":recall,"RF_F1-score":f_score,"RF_Accuracy":accuracy}
        
    def SVM(self,x_train,y_train,x_test,y_test):
        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        mySVC = svm.SVC(C=0.5, kernel='poly', random_state=0,probability=True)
        mySVC.fit(x_train_flatten, y_train_flatten)
        
        y_pred = mySVC.predict(x_test_flatten)
        prec = precision_score(y_test, y_pred,pos_label='positive', average='micro')
        recall = recall_score(y_test, y_pred,pos_label='positive', average='micro')
        f_score = f1_score(y_test, y_pred,pos_label='positive', average='micro')
        accuracy = accuracy_score(y_test, y_pred)
        print({"precision":prec,"recall":recall,"F1-score":f_score,"Accuracy":accuracy})
        return {"SVM_precision":prec,"SVM_recall":recall,"SVM_F1-score":f_score,"SVM_Accuracy":accuracy}
    
    def generate_log(self,e,s):
        output_file = open("log_eps_" + str(e) + "_sens_" + str(s) +".txt", 'w', encoding='utf-8')
        for dic in dic_list:
            json.dump(self.metrics, output_file) 
            output_file.write("\n")
        output_file.close()