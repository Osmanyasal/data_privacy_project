import numpy as np
import datasets.read_cifar as cifar
import os


class LaplaceNoise():
    def __init__(self, eps_val_start, eps_val_end, sens_val_start, sens_val_end, num):
        self.dataset = cifar.get_CIFAR10_data()
        self.eps_vals = np.linspace(eps_val_start,eps_val_end, num)
        self.sensitivity_vals = np.linspace(sens_val_start,sens_val_end, num)
        
        
    def addLaplaceNoise(self, idx, sens_ind, eps_ind, ind):
        """
        Adds laplace noise to the selected image with selected sensitivity and epsilon values.
        0th, 1st, 2nd, 3rd indices of the dataset include x_train, y_train, x_test, y_test, respectively. 
        ind variable refers to the index of the corresponding x image set.
        """
        
        new_arr = np.zeros(self.dataset[ind][idx].shape)
        for i in range(self.dataset[ind][idx].shape[0]):
            for j in range(self.dataset[ind][idx].shape[1]):
                new_arr[i][j] = self.dataset[ind][idx][i][j] \
                + np.random.laplace(0, self.sensitivity_vals[sens_ind] / self.eps_vals[eps_ind])
        return new_arr
    
    def anonymize(self, is_train=True):
        """
        Adds laplace noise to all images in the dataset.
        """
        
        ind = -1
        train = ""
        if is_train == True:
            ind = 0
            train = "train"
        else:
            ind = 2
            train = "test"
        
        #anonymized_images = {}

        for eps in range(len(self.eps_vals)):
            for sensitivity in range(len(self.sensitivity_vals)):
                anonymized_images = np.array([self.addLaplaceNoise(0, sensitivity, eps, ind)])
                for img in range(1,len(self.dataset[ind])):
                    anonymized_images = np.append(anonymized_images,[self.addLaplaceNoise(img, sensitivity, eps, ind)],axis=0) 
                    print(img)
                save_anonymized_eps_and_sens(anonymized_images,self.eps_vals[eps],\
                                             self.sensitivity_vals[sensitivity], word = train)    
                    
                    
                    #if (self.eps_vals[eps],self.sensitivity_vals[sensitivity]) not in anonymized_images.keys():
                    #    anonymized_images[(self.eps_vals[eps],self.sensitivity_vals[sensitivity])] =\
                    #    np.array([self.addLaplaceNoise(img, sensitivity, eps, ind)])
                    #else:
                    #    anonymized_images[(self.eps_vals[eps],self.sensitivity_vals[sensitivity])] =\
                    #    np.append(anonymized_images[(self.eps_vals[eps],self.sensitivity_vals[sensitivity])],\
                    #              [self.addLaplaceNoise(img, sensitivity, eps, ind)],axis=0)          
        
    def save_anonymized(self, imgs_dict, directory = "data/", word="train"):
        for imgs in imgs_dict.keys():
            eps = imgs[0]
            sens = imgs[1]
            isExist = os.path.exists(directory)
            if not isExist:
               # Create a new directory because it does not exist
               os.makedirs(directory)
            np.save(directory + word + "_" + str(eps)+"_" + str(sens),imgs_dict[imgs])
            
    def save_anonymized_eps_and_sens(self, imgs, eps, sens, directory = "data/", word="train"):
        isExist = os.path.exists(directory)
        if not isExist:
 
           os.makedirs(directory)
        np.save(directory + word + "_" + "%".join(str(eps).split("."))+"_" + "%".join(str(sens).split(".")),imgs)
        