import pandas as pd
import calendar
import datetime

class edaMonth:
    """
    A class used to receive a dataframe, 
    ...
    Attributes
    ----------
    df: pandas dataframe
        


    Methods
    -------
    """
    def __init__(self, dataframe):
        """
        Parameters 
        ----------
        dataframe: 
        """
        self.df = dataframe
        
    def start_Eda(self):
        self.df.set_index('Fecha', inplace = True)
        df_month = self.df.resample('M').sum()
        df_month['Cargo'] = df_month['Cargo']*-1
        df_month['Mes'] =[calendar.month_name[x] for x in df_month.index.month]
        self.fechas_df_month = df_month.index
        df_month.set_index('Mes', inplace = True)
        self.df = df_month.loc[:,'Cargo':'Abono']

    def plotting(self):
        today = datetime.date.today()
        plot = self.df.plot(figsize = (10,7),title = 'Monthly EDA until {}'.format(today),kind = 'bar', stacked = True)
        fig = plot.get_figure()
        fig.savefig('output_{}.png'.format(today))

class allMonths:
    def __init__(self, dataframe):
        self.df = dataframe.sort_values(by='Fecha', ascending=False)
        self.payments = self.df[self.df['Cargo']< 0].sort_values(by='Fecha', ascending=False)
        self.deposits = self.df[self.df['Abono'] > 0].sort_values(by='Fecha', ascending=False)

    def save_Data(self):
        today = datetime.date.today()
        try:
            self.payments.to_excel('Movimientos_{}.xlsx'.format(today), sheet_name = 'Cargos')
        except:
            with pd.ExcelWriter('Movimientos_{}.xlsx'.format(today), mode ='a' ) as writer:
                self.payments.to_excel('Movimientos_{}.xlsx'.format(today), sheet_name = 'Cargos')
                self.deposits.to_excel(writer, sheet_name = 'Abonos')
                self.df.to_excel(writer, sheet_name = 'Movimientos')
        else:
            with pd.ExcelWriter('Movimientos_{}.xlsx'.format(today), mode ='a' ) as writer:
                self.deposits.to_excel(writer, sheet_name = 'Abonos')
                self.df.to_excel(writer, sheet_name = 'Movimientos')


