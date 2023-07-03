"""
@Author Ben Funk

TODO:

**MOST IMPORTANT**

- **COMPLETE** Load in all files and save to an array

- **COMPLETE** Save one line for each ppm for each test with all necessary variables
    - Target PPM
    - Mean Voltage Ratio
    - Humidity
    - Temperature
    - Confidence interval % (90, 95, 99, etc)
    - Low/High confidence interval
    - Any other thing I might find useful in the future

- **COMPLETE** Use Curvefit to fit model to equation

**PAST GOALS**

- **COMPLETE** save all class data to a file on exit
- **COMPLETE** data partitions and other useful information
- **COMPLETE** Format all information being saved better

- **NOT NEEDED** check and load in saved data from info file when a file is loaded in that has been loaded in the past.

- **COMPLETE** Get 95% CI for each equation.
- generate an equation based on the 95%
- print out regression equation

- **COMPLETE** Return SD Sample Mean etc

- Save selected data to a standardized file.

- Get an equation that can predict CH4 ppm with voltage and absolute humidity
- Return RMSE value
"""
import glob
import os

import pandas as pd

import Analyze as an
import Data as da


def main():
    path = r'/Users/benfunk/DataspellProjects/MethaneDataScience/Raw Data'
    summary = pd.DataFrame()  # empty dataframe to hold summary results
    selectedData = pd.DataFrame()
    for filename in glob.glob(os.path.join(path, '*.csv')):
        with open(os.path.join(os.getcwd(), filename)) as file:
            myData = da.Data(csvFile=file, slope=6.7e-05)

            fsummary = an.summarize(df=myData, N_sensors=16, partitionSpots=myData.testSpots)
            summary = pd.concat([summary, fsummary], ignore_index=True)

    summary_fname = os.path.join('/Users/benfunk/DataspellProjects/MethaneDataScience/Output', 'With low Data .csv')
    summary.to_csv(summary_fname)

if __name__ == '__main__':
    main()



#%%
