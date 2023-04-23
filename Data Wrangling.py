# Importing Packages

import sys
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

#--------------------------------------------------------------------------------------------------#

class DataReading:

    def __init__(self, data_july_path, data_aug_path, data_sept_path, data_oct_path, data_nov_path):
        self.df_july = pd.read_csv(r'{}'.format(data_july_path))
        self.df_aug = pd.read_csv(r'{}'.format(data_aug_path))
        self.df_sept = pd.read_csv(r'{}'.format(data_sept_path))
        self.df_oct = pd.read_csv(r'{}'.format(data_oct_path))
        self.df_nov = pd.read_csv(r'{}'.format(data_nov_path))

    def combine_data(self):
        df = self.df_july.append([self.df_aug, self.df_sept, self.df_oct, self.df_nov])
        return df

    def backup_data(self):
        df = self.combine_data()
        df_backup = df.copy(deep=True)
        return df_backup


class DataCleaning:

    def __init__(self, combine_df):
        self.df = combine_df

    # Considering the quotes where (Sold date > Created date)
    def filtering_quotes(self):
        df = self.df
        df['CreatedDate'] = pd.to_datetime(df['CreatedDate'])
        df['Date_Sold__c'] = pd.to_datetime(df['Date_Sold__c'],errors='coerce')
        df = df[(df['Date_Sold__c'] >= df['CreatedDate']) | df['Date_Sold__c'].isnull()]
        return df

    def correcting_quotes_status(self):
        df = self.filtering_quotes()

        # removing quotes which do not have any status
        df.dropna(how='any',subset=['Status__c'], inplace=True)

        conditiona = [(df['Status__c'] == 'Sold') & df['Date_Sold__c'].isnull(),
                      (df['Status__c'] != 'Sold') & df['Date_Sold__c'].notnull()]

        values = ['Closed','Sold']

        df['Status_new'] = np.select(conditiona,values)
        df['Status_new'] = np.where(df['Status_new'] == '0',df['Status__c'],df['Status_new'])

        # Correcting Sold flag based on Status of quote
        df['Sold__c'] = np.where(df['Status_new'] == 'Sold','Yes','No')

        print(df['Sold__c'].value_counts())

        return df
    



#------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    
    obj1 = DataReading('myWork/data/july.csv', 'myWork/data/august.csv', 'myWork/data/sept.csv',
                       'myWork/data/oct.csv', 'myWork/data/nov.csv')

    df = obj1.combine_data()

    obj2 = DataCleaning(df)
    obj2.correcting_quotes_status()