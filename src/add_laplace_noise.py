#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import read_cifar as cifar
import ml_models

def add_laplace_noise(real_img, sensitivity: float, epsilon: float):
    """
    Adds laplace noise to the real image.

    """

    new_arr = np.zeros(real_img.shape)
    for i in range(real_img.shape[0]):
        for j in range(real_img.shape[1]):
            new_arr[i][j] = real_img[i][j] + np.random.laplace(0, sensitivity / epsilon)
    return new_arr


def calculate_average_error(actual_img, noisy_img):
    """
    Calculates error.

    Args: Actual image (np array), Noisy image (np array)
    Returns: Error (Err) in the noisy histogram (float)
    """


    return (
        sum(
            [
                abs(actual_val - noise_val)
                for actual_val, noise_val in zip(np.concatenate(actual_img).ravel(), np.concatenate(noisy_img).ravel())
            ]
        )
        / (actual_img.shape[0]*actual_img.shape[1])
    )


x_train, y_train, x_val, y_val, x_test, y_test = cifar.get_CIFAR10_data()
noise_vals = np.linspace(1e-5,1, num=10)
sensitivity = np.linspace(2, 1e-2, num=10)
last = 0
for n in noise_vals:
    for s in sensitivity:
        trs = []
        ts = []
        for tr in x_train:
            trs.append(add_laplace_noise(tr,s,n))
        
        for te in x_test:
            ts.append(add_laplace_noise(te,s,n))
    print(n)
    print(s)
    logi = ml_models.logistic_regression(trs,y_train,ts,y_test)
    print(logi)
    print("*****")
    if last != 0 and last < logi:
        break
    
print("LAST EPS : ", n)
print("LAST SENSITIVITY: ", s)
