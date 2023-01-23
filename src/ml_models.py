#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

import datasets.read_cifar as cifar


def logistic_regression(x_train,y_train,x_test,y_test):
    
    number_of_train = x_train.shape[0]
    number_of_test = x_test.shape[0]
    
    x_train_flatten = x_train.reshape(number_of_train,x_train.shape[1]*x_train.shape[2]*x_train.shape[3])
    x_test_flatten = x_test.reshape(number_of_test,x_test.shape[1]*x_test.shape[2]*x_test.shape[3])
    y_train_flatten = y_train
    y_test_flatten = y_test
    
    log_reg= LogisticRegression(penalty='l2', tol=0.0001, max_iter=1000, C=1,random_state=42)
    score = log_reg.fit(x_train_flatten, y_train_flatten).score(x_test_flatten, y_test_flatten)
    print("test accuracy: {} ".format(score))
    #print("train accuracy: {} ".format(log_reg.fit(x_train_flatten, y_train_flatten).score(x_train_flatten, y_train_flatten)))

    return score
x_train, y_train, x_val, y_val, x_test, y_test = cifar.get_CIFAR10_data()
print(logistic_regression(x_train, y_train, x_test, y_test))