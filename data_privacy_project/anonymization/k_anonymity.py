"""
K-anonymity anonymization algorithm goes here.
"""

from helper.filebase import FileBase
from helper.anonymization import AnonymizationHelper
class KAnonymity():
        
    @staticmethod
    def is_dataset_k_anonymous(raw_dataset,DGHs,k_value):
        column_based_group_dic = {} 
        for row in raw_dataset:
            key = ""
            for column in row.keys():
                if column in DGHs:
                    key += row[column]+"_"            
            if key in column_based_group_dic:
                column_based_group_dic[key] += 1
            else: column_based_group_dic[key] = 1
        
        return column_based_group_dic[min(column_based_group_dic, key=column_based_group_dic.get)] >= k_value
        
    
    @staticmethod
    def anonymize(raw_dataset,DGHs,k_length):
        """
        Parameters
        ----------
        raw_dataset : Array
            Array of dictionary that contains raw data
        DGHs : Dict
            Dictionary of all dgh files combined
        k_length : int
            K-anonymous length.
    
        Returns
        -------
        clusters : Array
            An array of anonymized data.
        """
        clusters = []
        
        for i in range(len(raw_dataset)):
            if i % k_length == 0:
                clusters.append([])
            clusters[-1].append(raw_dataset[i])
        
        if len(clusters[-1]) < k_length:
            clusters[-2].extend(clusters[-1])
            del clusters[-1]
    
        for cluster in clusters:
            is_k_anonymous = False
    
            while not is_k_anonymous:
                is_k_anonymous = True ## assume it's k anonymous
                non_anonymous_columns = []
                
                #collect keys the values are not the same.
                for i in range(len(cluster)-1):
                    for key in cluster[0].keys():
                        if(key in DGHs and cluster[i][key] != cluster[i+1][key]):
                            is_k_anonymous = False
                            if(key not in non_anonymous_columns):
                                non_anonymous_columns.append(key)
                
                ## update levels only for one that is deeper than the other.
                for i in range(len(cluster)):
                    for key in non_anonymous_columns:
                        temp = AnonymizationHelper.find_DGH_item(DGHs[key], cluster[i][key])
                        temp2 = AnonymizationHelper.find_DGH_item(DGHs[key], cluster[(i+1) % k_length][key])
                        if(int(temp["level"]) >= int(temp2["level"]) and temp["parent"] != None):
                            cluster[i][key] = temp["parent"]["name"]
                 
        anonymized_dataset = []

        for cluster in clusters:        #restructure according to previous indexes
            for item in cluster:
                anonymized_dataset.append(item)
        return anonymized_dataset
