# This class takes a csv file_Grid name and return rows of the file_Grid
import csv
import pandas as pd

class CSVDFReader():

    def csvdfReader(self,inputfile):
        self.df_file = pd.read_csv (inputfile)
        print(f'{inputfile} is read and added successfully')
        return self.df_file
