"""
Clustering anonymization algorithm goes here.
"""
import sys
from copy import deepcopy
from anonymization.k_anonymity import KAnonymity
from helper.anonymization import AnonymizationHelper

class Clustering():
    
    @staticmethod
    def anonymize(raw_dataset, DGHs, k: int):
        """ Clustering-based anonymization a dataset, given a set of DGHs.
    
        Args:
            raw_dataset_file (str): the path to the raw dataset file.
            DGH_folder (str): the path to the DGH directory.
            k (int): k-anonymity parameter.
        """
        for i in range(len(raw_dataset)): ##set indexing to not lose original places of records
            raw_dataset[i]["index"] = i
            raw_dataset[i]['is_marked'] = False
    
        clusters = []
        
        min_distance_value = None
        min_distance = sys.maxsize
        
        original_records_of_last_anonymized = []
        for i in range(len(raw_dataset)-1): 
            # if i is not used before, then take it into account
            if raw_dataset[i]["is_marked"]: 
                continue 
            
            clusters.append([raw_dataset[i]])            
            raw_dataset[i]["is_marked"] = True
            
            # TODO:optimize to only keep len(cache) = k and contains k - min data and read from there
            cache_lm_for_value_i = {}
            
            for counter in range(k-1):
                min_distance_value = None
                min_distance = sys.maxsize
                for j in range(i+1,len(raw_dataset)):
                    #if j is used before then ignore it!
                    if raw_dataset[j]["is_marked"]:
                        continue 
                  
                    if j not in cache_lm_for_value_i:
                        cache_lm_for_value_i[j] = AnonymizationHelper.calculate_lm(DGHs, KAnonymity.anonymize([raw_dataset[i].copy(), raw_dataset[j].copy()],DGHs,2)[0])
                    
                    res = cache_lm_for_value_i[j]
                    if res < min_distance:
                        min_distance = res
                        min_distance_value = raw_dataset[j] 
                
                if min_distance_value != None:
                    min_distance_value["is_marked"] = True 
                    clusters[-1].append(min_distance_value)
                
            if len(clusters[-1]) < k:
                clusters[-2] = original_records_of_last_anonymized + clusters[-1]
                del clusters[-1]
                clusters[-1] = KAnonymity.anonymize(clusters[-1], DGHs, len(clusters[-1]))[0]
            else: 
                original_records_of_last_anonymized = deepcopy(clusters[-1])
                clusters[-1] = KAnonymity.anonymize(clusters[-1], DGHs, k)[0]
        
        anonymized_dataset = [None] * len(raw_dataset) 
         
        #restructure according to previous indexes
        for cluster in clusters:        
            for item in cluster: 
                anonymized_dataset[item['index']] = item 
                del item['index']
                del item["is_marked"]
        
        return anonymized_dataset
