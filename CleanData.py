import pandas as pd

class cleanData:
    def __init__(self, dataframe):
        self.data = dataframe


    def start_clean(self):    
        self.data = self.data.fillna(value = 0)
        #self.data.convert_dtypes().dtypes #Marca error en Mac, pero no causa efectos colaterales
        self.data['Fecha'] = pd.to_datetime(self.data['Fecha'], format ='%d/%m/%Y')
        self.df = pd.concat([self.data[['Fecha','Descripcion']], self.data.loc[:,'Cargo':'Saldo'].apply(lambda x: x.str.replace(',', '').astype(float), axis=1).fillna(value = 0)],axis = 1)
        self.df['Cargo'] = self.df['Cargo'] *-1