"""
Bottomup anonymization algorithm goes here.
"""
import sys
import itertools
from helper.anonymization import AnonymizationHelper
from copy import deepcopy

class BottomUp():
    
    @staticmethod
    def combinations(items,level):
        return list(itertools.combinations_with_replacement(items,r=level))
             
    @staticmethod
    def group_combinations(column_combinations):
        """
        Group all combinations into a dictionary.
        """
        levels = []
        for combination in column_combinations:
            node = {}
            for node_item in combination:
                if node_item not in node:
                    node[node_item] = 1
                else : node[node_item] += 1
            levels.append(node)
            
            
        return levels
    
    @staticmethod
    def is_column_combination_valid(combination,DGHs):
        
       for column in combination.keys():
          if combination[column] > (len(DGHs[column]) -1):
              return False
       return True

    @staticmethod
    def anonymize(raw_dataset, DGHs, k: int):
        """ Bottom up-based anonymization a dataset, given a set of DGHs.
    
        Args:
            raw_dataset_file (str): the path to the raw dataset file.
            DGH_folder (str): the path to the DGH directory.
            k (int): k-anonymity parameter.
            output_file (str): the path to the output dataset file.
        """
        original_dataset = deepcopy(raw_dataset)
    
        node_level = 0
        node_level_min_cost_lm_val = sys.maxsize
        node_level_min_cost_columns = []
        k_is_found_on_level = False
        
        keys = []
        for key in raw_dataset[0].keys():
            if key in DGHs:
                keys.append(key)
        
        while True:
            print("searching level:",node_level)
            all_combinations = BottomUp.group_combinations(BottomUp.combinations(keys, node_level))
            for combination in all_combinations:
                
                if not BottomUp.is_column_combination_valid(combination,DGHs):
                    continue
                
                raw_dataset = BottomUp.column_anonymize_by_column_name_level(raw_dataset, DGHs, combination)
                if BottomUp.is_dataset_k_anonymous(raw_dataset,DGHs,k):
                        k_is_found_on_level = True
    
                        lm_result = AnonymizationHelper.calculate_lm(DGHs, raw_dataset)
                        
                        ## uncomment if you want to see the column combinations that satisfy k-anonymity
                        #print("found one:",lm_result,combination)
                        if lm_result < node_level_min_cost_lm_val:
                            node_level_min_cost_lm_val = lm_result
                            node_level_min_cost_columns = deepcopy(combination)
                
                raw_dataset = deepcopy(original_dataset)
            #end for
            
            if k_is_found_on_level: break
            node_level += 1
    
        print(node_level,node_level_min_cost_lm_val,node_level_min_cost_columns)
        raw_dataset = BottomUp.column_anonymize_by_column_name_level(original_dataset, DGHs, node_level_min_cost_columns)
        return raw_dataset
       
        