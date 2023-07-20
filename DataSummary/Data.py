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

        self.dataVOut = self.file.loc[:, 'Vout0':'Vout15']
        self.dataVRef = self.file.loc[:, 'Vref0':'Vref15']

        # getting the resistance of each sensor and appending it to general file
        for s in range(0, 16):
            # Find the rows where 'Target ppm' is 0, select the last 225 of these, and compute the mean
            mean_of_last_225 = self.file.loc[self.file['Target ppm'] == 0, 'Vout' + str(s)].tail(225).mean()

            tempResistance = (mean_of_last_225 * (5 - self.file['Vout' + str(s)])) / ((self.file['Vout' + str(s)]) * (5 - mean_of_last_225))

            tempResistance.reset_index(drop=True, inplace=True)
            tempResistance.name = 'Resistance' + str(s)
            tempFrame = pd.DataFrame(tempResistance)


            self.file = pd.concat([self.file, tempFrame], axis=1)





        self.resistance = self.file.loc[:, 'Resistance0':'Resistance15']

        self.dataRatio = self.dataVOut.to_numpy() / self.dataVRef.to_numpy()
        self.dataRatio = pd.DataFrame(self.dataRatio)

        self.dataTarget = self.file.loc[:, 'Target ppm']

        self.dataHumid = self.file.loc[:, 'Humidity%']

        self.testSpots = an.selectPeriods(self.file, 225)

        self.sensors = []
        for s in range(0, 16):  # for each sensor
            self.sensors.append(si.sensor(self.fileName, s))