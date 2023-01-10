# -*- coding: utf-8 -*-

from enum import Enum


class ML_Methods(Enum):
    BOTTOMUP = "bottomup",
    CLUSTERING = "clustering",
    K_ANONYMITY = "k_anonymity",
    RANDOM = "random",
    
    @staticmethod
    def get_type(type_name):
        
        if type_name == AnonymizationTypes.BOTTOMUP.value[0]:
            return AnonymizationTypes.BOTTOMUP
        
        if type_name == AnonymizationTypes.CLUSTERING.value[0]:
            return AnonymizationTypes.CLUSTERING
        
        if type_name == AnonymizationTypes.K_ANONYMITY.value[0]:
            return AnonymizationTypes.K_ANONYMITY
        
        if type_name == AnonymizationTypes.RANDOM.value[0]:
            return AnonymizationTypes.RANDOM


class AnonymizationTypes(Enum):
    BOTTOMUP = "bottomup",
    CLUSTERING = "clustering",
    K_ANONYMITY = "k_anonymity",
    RANDOM = "random",
    
    @staticmethod
    def get_type(type_name):
        
        if type_name == AnonymizationTypes.BOTTOMUP.value[0]:
            return AnonymizationTypes.BOTTOMUP
        
        if type_name == AnonymizationTypes.CLUSTERING.value[0]:
            return AnonymizationTypes.CLUSTERING
        
        if type_name == AnonymizationTypes.K_ANONYMITY.value[0]:
            return AnonymizationTypes.K_ANONYMITY
        
        if type_name == AnonymizationTypes.RANDOM.value[0]:
            return AnonymizationTypes.RANDOM

class AnonymizationHelper():
     
    
    @staticmethod
    def find_DGH_item(dgh_levels, dgh_name):
        """
        Find DGH item in the DGH levels
        
        Args:
            dgh_levels : dgh_level format\n
            dgh_name : dgh string name
    
        Returns:
            DGH item
        """
        for level in dgh_levels.keys():
            for item in dgh_levels[level]:
                if(item["name"] == dgh_name):
                    return item
         
        return {"name":None,"level":None,"parent":None,"child":[],"is_valid":False}

    
    @staticmethod
    def find_decended_leaf_count(dgh_levels,dgh_name):
        dgh_item = AnonymizationHelper.find_DGH_item(dgh_levels, dgh_name)
           
        if not dgh_item["is_valid"]:
            return 0
        elif len(dgh_item["child"]) == 0:
            return 1
        else:
            total_decended_leaf_count = 0
            for child in dgh_item["child"]:
                total_decended_leaf_count += AnonymizationHelper.find_decended_leaf_count(dgh_levels, child["name"])
                
        return total_decended_leaf_count

    
    decended_leaf_count_cache = {}
    @staticmethod
    def calculate_lm(DGHs,raw_dataset):
        cost_lm = 0
        w = 1 / len(DGHs)
        global decended_leaf_count_cache
        for item in raw_dataset:
            for key in item.keys():
                if key in DGHs: 
                   #add education_Scholar education_Graduate ...
                   if key+"_"+item[key] not in decended_leaf_count_cache:
                       decended_leaf_count_cache[key+"_"+item[key]] = \
                           AnonymizationHelper.find_decended_leaf_count(DGHs[key], item[key])
                   
                   #add education_Any, age_Any
                   if key+"_"+DGHs[key][0][0]["name"] not in decended_leaf_count_cache:
                       decended_leaf_count_cache[key+"_"+DGHs[key][0][0]["name"]] = \
                           AnonymizationHelper.find_decended_leaf_count(DGHs[key], DGHs[key][0][0]["name"])
                                                                                                     
                   cost_lm += w * ((decended_leaf_count_cache[key+"_"+item[key]] -1) / 
                                  (decended_leaf_count_cache[key+"_"+DGHs[key][0][0]["name"]]-1))
        
        return cost_lm
        
    @staticmethod
    def cost_MD(raw_dataset, anonymized_dataset, DGHs) -> float:
        """Calculate Distortion Metric (MD) cost between two datasets.
    
        Args:
            raw_dataset_file (str): the path to the raw dataset file.
            anonymized_dataset_file (str): the path to the anonymized dataset file.
            DGH_folder (str): the path to the DGH directory.
    
        Returns:
            float: the calculated cost.
        """ 
        assert(len(raw_dataset)>0 and len(raw_dataset) == len(anonymized_dataset)
            and len(raw_dataset[0]) == len(anonymized_dataset[0]))
        cost_md = 0
        for i in range(len(raw_dataset)):
            original_item = raw_dataset[i]
            anonymized_item = anonymized_dataset[i]
            for key in original_item.keys():
                if key in DGHs:
                    cost_md += abs(AnonymizationHelper.find_DGH_item(DGHs[key], original_item[key])["level"] -\
                        AnonymizationHelper.find_DGH_item(DGHs[key], anonymized_item[key])["level"])
                
            
        
        return cost_md
    
    @staticmethod
    def cost_LM(raw_dataset, anonymized_dataset, DGHs) -> float:
        """Calculate Loss Metric (LM) cost between two datasets.
    
        Args:
            raw_dataset_file (str): the path to the raw dataset file.
            anonymized_dataset_file (str): the path to the anonymized dataset file.
            DGH_folder (str): the path to the DGH directory.
    
        Returns:
            float: the calculated cost.
        """
         
        assert(len(raw_dataset)>0 and len(raw_dataset) == len(anonymized_dataset)
            and len(raw_dataset[0]) == len(anonymized_dataset[0]))
         
        return AnonymizationHelper.calculate_lm(DGHs, anonymized_dataset)          
                
