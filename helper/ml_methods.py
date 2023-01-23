from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm



class ML_Methods():
    def __init__(self, dataset, type_):
        self.dataset = dataset
        self.type_ = type_
    def run(self):
        if self.type_ == "lr":
            metrics = logistic_regression(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3])
        if self.type_ == "dt":
            metrics = decision_tree(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3])
        if self.type_ == "rf":
            metrics = random_forest(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3])
        if self.type_ == "svm":
            metrics = SVM(self.dataset[0],self.dataset[1],self.dataset[2],self.dataset[3])
        return metrics
    
    
    def logistic_regression(x_train,y_train,x_test,y_test):

        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        log_reg= LogisticRegression(penalty='l2', tol=0.0001, max_iter=1000, C=1,random_state=42)
        score = log_reg.fit(x_train_flatten, y_train_flatten).score(x_test_flatten, y_test_flatten)
        

        return score


    def decision_tree(x_train,y_train,x_test,y_test):
        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        clf= tree.DecisionTreeClassifier(max_depth=30,random_state=0,criterion='entropy')
        clf.fit(x_train_flatten,y_train_flatten)
        fin_acc = clf.score(x_test_flatten,y_test_flatten)
        return fin_acc


    def random_forest(x_train,y_train,x_test,y_test):
        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        clf  = RandomForestClassifier(n_estimators=100)

        # fit the training data to the model
        clf.fit(x_train_flatten, y_train_flatten)


        score = clf.score(x_test_flatten,y_test_flatten)
        return score

    def SVM(x_train,y_train,x_test,y_test):
        number_of_train = x_train.shape[0]
        number_of_test = x_test.shape[0]

        x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
        x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
        y_train_flatten = y_train
        y_test_flatten = y_test

        mySVC = svm.SVC(C=0.5, kernel='poly', random_state=0,probability=True)
        mySVC.fit(x_train_flatten, y_train_flatten)

        return mySVC.score(x_test_flatten,y_test_flatten)