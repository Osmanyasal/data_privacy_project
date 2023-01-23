"""
Read - write dataset
Read and trasnform DGHs
Saving report outputs.
other operations that include files.
"""
import csv
import glob
import os

class FileBase():
    
    @staticmethod
    def read_dataset(dataset_file: str):
        """ Read a dataset into a list and return.
        Args:
            dataset_file (str): path to the dataset file.
        Returns:
            list[dict]: a list of dataset rows.
        """
        result = []
        with open(dataset_file) as f:
            records = csv.DictReader(f)
            for row in records:
                result.append(row)
        return result
    
    @staticmethod
    def write_dataset(dataset, dataset_file: str) -> bool:
        """ Writes a dataset to a csv file.
        Args:
            dataset: the data in list[dict] format
            dataset_file: str, the path to the csv file
        Returns:
            bool: True if succeeds.
        """
        assert len(dataset)>0, "The anonymized dataset is empty."
        keys = dataset[0].keys()
        with open(dataset_file, 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(dataset)
        return True
    
    @staticmethod
    def read_DGHs(DGH_folder: str) -> dict:
        """ Read all DGH files from a directory and put them into a dictionary.
    
        Args:
            DGH_folder (str): the path to the directory containing DGH files.
    
        Returns:
            dict: a dictionary where each key is attribute name and values
                are DGHs in your desired format.
        """
        DGHs = {}
        for DGH_file in glob.glob(DGH_folder + "/*.txt"):
            attribute_name = os.path.basename(DGH_file)[:-4]
            DGHs[attribute_name] = FileBase.__read_DGH(DGH_file)
    
        return DGHs

    @staticmethod
    def __read_DGH(DGH_file: str):
        """ Reads one DGH file and returns in desired format.
    
        Args:
            DGH_file (str): the path to DGH file.
        """
        dgh_levels = {}
        with open(DGH_file) as dgh_file:
            file_content = dgh_file.readlines()
            for line in file_content:
                cls_name = line.strip() 
                cls_height = (len(line) - len(line.lstrip())) #this count tabs
                cls_item = {"name" : cls_name,"level":cls_height,"parent":None,"child":[],"is_valid":True}
                if cls_height not in dgh_levels:
                    dgh_levels[cls_height] = []
                
                if cls_height > 0:
                    cls_item["parent"] = dgh_levels[cls_height-1][-1]
                    dgh_levels[cls_height-1][-1]["child"].append(cls_item)
                    
                dgh_levels[cls_height].append(cls_item)
                
        return dgh_levels        
                
