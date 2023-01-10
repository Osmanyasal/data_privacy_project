"""
Random anonymization algorithm goes here.
"""
import numpy as np
from helper.filebase import FileBase
from helper.k_anonymity import KAnonymity
class RandomAnonymizer():
    
    @staticmethod
    def anonymize(raw_dataset, DGHs, k: int,
        output_file: str, s: int):
        """ K-anonymization a dataset, given a set of DGHs and a k-anonymity param.
    
        Args:
            raw_dataset_file (str): the path to the raw dataset file.
            DGH_folder (str): the path to the DGH directory.
            k (int): k-anonymity parameter.
            output_file (str): the path to the output dataset file.
            s (int): seed of the randomization function
        """
        
        for i in range(len(raw_dataset)): ##set indexing to not lose original places of records
            raw_dataset[i]['index'] = i
    
        raw_dataset = np.array(raw_dataset)
        np.random.seed(s) ## to ensure consistency between runs
        np.random.shuffle(raw_dataset)  ##shuffle the dataset to randomize
    
        clusters = []
        D = len(raw_dataset)
        
        clusters = KAnonymity.anonymize(raw_dataset,DGHs,k)
        anonymized_dataset = [None] * D
    
        for cluster in clusters:        #restructure according to previous indexes
            for item in cluster:
                anonymized_dataset[item['index']] = item
                del item['index']
    
        return anonymized_dataset
        


    