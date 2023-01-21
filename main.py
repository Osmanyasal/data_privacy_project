"""
WHERE PROGRAM BEGINS.
"""
import sys
import helper.parser as cli_parser
from helper.filebase import FileBase 
from helper.anonymization import AnonymizationTypes
from anonymization.k_anonymity import KAnonymity
from anonymization.laplace_noise import LaplaceNoise

def anonymization_preprocessing():
    pass

if __name__ == "__main__":
    dic = cli_parser.parse(sys.argv)
    if dic["is_tabular"]:
        dghs = FileBase.read_DGHs(dic["dgh_folder"])
        dataset = FileBase.read_dataset(dic["dataset"])
        
        for model in dic["anonymization"]:
            anonymization_preprocessing()
            if model == AnonymizationTypes.K_ANONYMITY:
                for i in range(dic["start_k"],dic["end_k"]+1):
                    anonymized_dataset = KAnonymity.anonymize(dataset, dghs, i)
                    print(KAnonymity.is_dataset_k_anonymous(anonymized_dataset, dghs, i))
                
            if model == AnonymizationTypes.CLUSTERING:
                pass
            if model == AnonymizationTypes.BOTTOMUP:
                pass
            if model == AnonymizationTypes.RANDOM:
                pass
        
    else:
        eps_start, eps_end = dic["start_eps"], dic["end_eps"]
        sens_start, sens_end = dic["start_sens"], dic["end_sens"]
        num = dic["number"]
        laplace = LaplaceNoise(eps_start, eps_end, sens_start, sens_end, num)
        anonymized_train_images = laplace.anonymize()
        laplace.save_anonymized(anonymized_train_images)
        anonymized_test_images = laplace.anonymize(False)
        laplace.save_anonymized(anonymized_test_images,word="test")
        
        
