from CleanData import cleanData
from ReadData import readData
from EDA import edaMonth, allMonths

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():
    logger.info(' Reading Data...')
    reader = readData()
    logger.info(' Founded {} excel files: {}. Beginning row filtering ...'.format(len(reader.excel_files),reader.excel_files))
    reader.process_Data()
    reader.row_Filtering()
    logger.info('Concatenating data...')
    reader.concat_Data()
    logger.info('Beginning data cleaning ...')
    cleaner = cleanData(reader.df)
    cleaner.start_clean()
    logger.info('Beginning monthly EDA ...')
    analizer = edaMonth(cleaner.df)
    analizer.start_Eda()
    analizer2 = allMonths(cleaner.df)
    logger.info('Done successfully!')
    return cleaner.df, analizer.df, reader.cuenta, analizer.fechas_df_month

if __name__ == '__main__':
    logger.info(' Reading Data...')
    reader = readData()
    logger.info(' Founded {} excel files: {}. Beginning row filtering ...'.format(len(reader.excel_files),reader.excel_files))
    reader.process_Data()
    reader.row_Filtering()
    logger.info('Concatenating data...')
    reader.concat_Data()
    logger.info('Beginning data cleaning ...')
    cleaner = cleanData(reader.df)
    cleaner.start_clean()
    logger.info('Beginning monthly EDA ...')
    analizer = edaMonth(cleaner.df)
    analizer.start_Eda()
    logger.info('Plotting ...')
    analizer.plotting()
    analizer2 = allMonths(cleaner.df)
    logger.info('Writting data ...')
    analizer2.save_Data()
    logger.info('Done successfully!')