import pandas as pd

import Analyze as an
import SensorInformation as si

"""
This class holds all of the information pertaining to a single csv file
"""


# 0.21079
class Data():

    def __init__(self, csvFile, slope):

        # Store File name and file as dataframe
        self.fileName = csvFile
        self.file = pd.read_csv(csvFile)
        self.file['%Humidity'] = pd.to_numeric(self.file['%Humidity'], errors='coerce')
        self.file['Temp(c)'] = pd.to_numeric(self.file['Temp(c)'], errors='coerce')
        self.file = self.file.dropna(subset=['Temp(c)', '%Humidity', 'Target ppm'])
        self.file.reset_index(drop=True, inplace=True)

        self.testSpots = an.selectPeriods(self.file, 225)

        self.dataVOut = self.file.loc[:, 'Vout0':'Vout15']
        self.dataVRef = self.file.loc[:, 'Vref0':'Vref15']

        # # getting the resistance of each sensor and appending it to general file
        # for s in range(0, 16):
        #     tempResistance = ((self.file['Vref' + str(s)] * (5 - self.file['Vout' + str(s)])) / (
        #             (self.file['Vout' + str(s)]) * (5 - self.file['Vref' + str(s)])))
        #     tempFrame = pd.DataFrame(tempResistance, columns=['Resistance' + str(s)])
        #     self.file = pd.concat([self.file, tempFrame], axis=1)

        # getting the resistance of each sensor and appending it to general file
        for s in range(0, 16):
            # Selecting the reference Vout values being used from the data and calculating the mean
            reference0 = self.dataVOut.iloc[self.testSpots[0][0]:self.testSpots[0][1]]['Vout' + str(s)]
            reference0_avg = reference0.mean()

            # Calculating resistance
            tempResistance = ((reference0_avg * (5 - self.file['Vout' + str(s)])) /
                      (self.file['Vout' + str(s)] * (5 - reference0_avg)))

            # Ensuring tempResistance is a Series and has the same index as self.file
            if not isinstance(tempResistance, pd.Series):
                tempResistance = pd.Series(tempResistance, index=self.file.index)

            # Creating a DataFrame from tempResistance
            tempFrame = pd.DataFrame({f'Resistance{s}': tempResistance})

            # Concatenating with the main DataFrame
            self.file = pd.concat([self.file, tempFrame], axis=1)


        self.resistance = self.file.loc[:, 'Resistance0':'Resistance15']

        self.dataRatio = self.dataVOut.to_numpy() / self.dataVRef.to_numpy()
        self.dataRatio = pd.DataFrame(self.dataRatio)

        #self.partitionSpots = an.autoSelectData(self.resistance, slope)

        self.dataTarget = self.file.loc[:, 'Target ppm']
        self.dataHumid = self.file.loc[:, '%Humidity']
        self.dataTemp = self.file.loc[:, 'Temp(c)']
        # # Find the column name that starts with 'humidity' and ends with '%' or starts with '%' and ends with 'humidity' (case-insensitive)
        # humidity_column = next((col for col in self.file.columns if (col.lower().startswith('humidity') and col.endswith('%')) or (col.startswith('%') and col.lower().endswith('humidity'))), None)
        #
        # if humidity_column:
        #     self.dataHumid = self.file.loc[:, humidity_column]
        # else:
        #     print("No matching humidity column found")
        #
        # Temp_column = next((col for col in self.file.columns if (col.lower().startswith('temp') and col.endswith('(c)')) or ( col.lower().endswith('temp(c)'))), None)
        #
        # if humidity_column:
        #     self.dataTemp = self.file.loc[:, Temp_column]
        # else:
        #     print("No matching humidity column found")


        self.sensors = []
        for s in range(0, 16):  # for each sensor
            self.sensors.append(si.sensor(self.fileName, s))