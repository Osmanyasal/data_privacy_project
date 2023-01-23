"""
WHERE PROGRAM BEGINS.
"""
import sys
import glob
import numpy as np
import itertools

import helper.parser as cli_parser
from helper.filebase import FileBase 
from helper.anonymization import AnonymizationTypes
from helper.ml_methods import ML_Methods
from anonymization.k_anonymity import KAnonymity
from anonymization.clustering import Clustering
from anonymization.bottomup import BottomUp
from anonymization.random import RandomAnonymizer
from anonymization.laplace_noise import LaplaceNoise

def anonymization_preprocessing(dic):
    return FileBase.read_dataset(dic["dataset"])

if __name__ == "__main__":
    dic = cli_parser.parse(sys.argv)
    if dic["is_tabular"]:
        dghs = FileBase.read_DGHs(dic["dgh_folder"])
        dataset = FileBase.read_dataset(dic["dataset"])
        
        for model in dic["anonymization"]:
            dataset = anonymization_preprocessing(dic)
            
            if model == AnonymizationTypes.K_ANONYMITY:
                for group_count in range(dic["start_k"],dic["end_k"]+1):
                    anonymized_dataset = KAnonymity.anonymize(dataset, dghs, group_count)
                    print(KAnonymity.is_dataset_k_anonymous(anonymized_dataset, dghs, group_count))
                    FileBase.write_dataset(anonymized_dataset, "k_anonymity_"+str(group_count)+".csv")
            elif model == AnonymizationTypes.CLUSTERING:
                for group_count in range(dic["start_k"],dic["end_k"]+1):
                    anonymized_dataset = Clustering.anonymize(dataset, dghs, group_count)
                    print(KAnonymity.is_dataset_k_anonymous(anonymized_dataset, dghs, group_count))
                    FileBase.write_dataset(anonymized_dataset, "clustering_"+str(group_count)+".csv")
            elif model == AnonymizationTypes.BOTTOMUP:
                for group_count in range(dic["start_k"],dic["end_k"]+1):
                    anonymized_dataset = BottomUp.anonymize(dataset, dghs, group_count)
                    print(KAnonymity.is_dataset_k_anonymous(anonymized_dataset, dghs, group_count))
                    FileBase.write_dataset(anonymized_dataset, "bottomup_"+str(group_count)+".csv")
            elif model == AnonymizationTypes.RANDOM:
                for group_count in range(dic["start_k"],dic["end_k"]+1):
                    anonymized_dataset = RandomAnonymizer.anonymize(dataset, dghs, group_count,dic["seed"])
                    print(KAnonymity.is_dataset_k_anonymous(anonymized_dataset, dghs, group_count))
                    FileBase.write_dataset(anonymized_dataset, "random_"+str(group_count)+".csv")
        
    else:
        eps_start, eps_end = dic["start_eps"], dic["end_eps"]
        sens_start, sens_end = dic["start_sens"], dic["end_sens"]
        num = dic["number"]
        laplace = LaplaceNoise(eps_start, eps_end, sens_start, sens_end, num)
        if len(glob.glob("data/*")) == 0:
            anonymized_train_images = laplace.anonymize()
            #laplace.save_anonymized(anonymized_train_images)
            anonymized_test_images = laplace.anonymize(False)
            #laplace.save_anonymized(anonymized_test_images,word="test")
        
        methods = dic["ml_methods"]
        eps = laplace.eps_vals
        sens = laplace.sensitivity_vals
        combinations = list(itertools.product(eps,sens))
        y_train = laplace.dataset[1]
        y_test = laplace.dataset[5]
        for e, s in combinations:
            name_e = "%".join(str(e).split(".")) 
            name_s = "%".join(str(s).split("."))
            path = name_e + "_" + name_s + ".npy"
            if len(glob.glob("data/train_" + path)) > 0 and len(glob.glob("data/test_" + path)) > 0:
                x_train = np.load("data/train_" + path)[1:,:,:]
                x_test = np.load("data/test_" + path)[1:,:,:]
            ml_instance = ML_Methods([x_train,y_train,x_test,y_test],methods)
            ml_instance.run()
            ml_instance.generate_log(name_e,name_s)
                
                
                
         
        