import pandas as pd
import os

class readData:
    """
    A class used to read xlsx files generetated by BBVA (Normally called movimientos.xlsx) and merge them into a dataframe.
    ...
    Attributes
    ----------
    excel_files: list
        contains the xlsx files name
    predata: list
        with process_data() method stores all the pandas dataframes read from the xlsx files
    df: pandas dataframe
        with concat_Data() merge all the dataframes from attribute predata in this attribute
    size: int
        the size of xlsx files
    
    Methods
    -------
    process_data()
        Read the xlsx files and store them on predata
    
    row_Filtering()
        # Due to data clutter, it organizes the data, create columns names and stores it on attribute predata
    
    concat_Data()
        Merge the dataframes contained on predata.
 
    """
    def __init__(self):
        self._path = os.listdir()
        self._excel_files = [x for x in self._path if '.xlsx' in x and '$' not in x]
        self.predata = []

    def process_Data(self):
        """
        Parameters: none
        Returns: none
        Read the xlsx files and store them on predata
        """
        for xlsx in self._excel_files:
            self.predata.append(pd.read_excel(xlsx))
    
    def row_Filtering(self, a= 3, b = -2):
        """
        Parameters
        ----------
        a: int
            the first row containing data
        b: int
            the last row containing data
        Returns: none
        Due to data clutter, it organizes the data, create columns names and stores it on predata
        """
        cont = 0
        for predata in self.predata:
            data = pd.DataFrame()
            self.cuenta = predata.columns[0]
            data['Fecha'] = predata.iloc[a:b,0]
            data['Descripcion'] = predata.iloc[a:b,1]
            data['Cargo'] = predata.iloc[a:b,2] 
            data['Abono'] = predata.iloc[a:b,3]
            data['Saldo'] = predata.iloc[a:b,4]
            self.predata[cont] = data
            cont+=1

    def concat_Data(self):
        """
        Parameters: none
        Returns: none
        Merge the dataframes contained on predata.
        """
        self.df = self.predata[0]
        for predata in self.predata:
            self.df = pd.merge(self.df, predata, on = ['Descripcion','Fecha','Cargo','Abono','Saldo'],how ='outer' )
    @property
    def size(self):
        return len(self.predata)

    @property
    def excel_files(self):
        return self._excel_files
