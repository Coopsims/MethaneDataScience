import numpy as np
import pandas as pd
import scipy.stats

import Data


def summarize(df: Data, N_sensors, partitionSpots):
    summary = pd.DataFrame()
    low, high = generateConfidinceInterval(partitionSpots, df.resistance, 16)
    for i in range(0, len(partitionSpots)):
        start = partitionSpots[i][0]
        end = partitionSpots[i][1]
        for s in [0, 3, 5, 7, 8, 10, 13, 15]:  # for each sensor

            sensordf = pd.DataFrame(
                [df.sensors[s].sensor, df.dataTarget.loc[start],
                 df.resistance.loc[start:end, 'Resistance' + str(s)].mean(),
                 df.file.loc[start:end, 'SHTTemp(C)'].mean(),
                 df.file.loc[start:end, 'Humidity%'].mean(),
                 low[i][s], high[i][s],
                 df.dataRatio.loc[start:end].mean(numeric_only=True).mean()]).T
            sensordf.columns = ['SensorID', 'Target PPM', 'Resistance', 'Temperature',
                                'RelativeHumidity',
                                'lowInterval', 'highInterval',
                                'Ratio']
            summary = pd.concat([summary, sensordf], ignore_index=True)  # append as new row in summary df

    return summary


def generateConfidinceInterval(partitionSpots, resistance, nSensors):
    lowInterval = []
    highInterval = []

    for item in partitionSpots:
        subLow = []
        subHigh = []
        for i in range(0, nSensors):
            lowEnd = item[0]
            highEnd = item[1]
            tempDF = resistance.loc[lowEnd:highEnd, 'Resistance' + str(i)]
            tempLowInterval, tempHighInterval = scipy.stats.t.interval(0.95, df=len(tempDF) - 1, loc=np.mean(tempDF),
                                                                       scale=np.std(tempDF))
            subLow.append(tempLowInterval)
            subHigh.append(tempHighInterval)
        lowInterval.append(subLow)
        highInterval.append(subHigh)

    return lowInterval, highInterval


def autoSelectData(resistance, slope):
    n = 200
    pointer1 = 0
    pointer2 = pointer1 + n
    selectedSpots = []
    # TODO: figure out optimal value for slopedif
    slopeDiff = slope
    currentSlope = 0
    lastSlope = 10
    len(resistance)
    while pointer2 <= len(resistance):

        if slopeDiff >= abs(currentSlope):
            testList = list(resistance[pointer1:pointer2].T.columns.values)
            b = np.polyfit(testList, resistance[pointer1:pointer2].T.mean(), 1)

            if currentSlope != 0:
                lastSlope = currentSlope
            currentSlope = b[0]
            pointer2 += n

            if pointer2 >= len(resistance) and slopeDiff >= abs(lastSlope):
                selectedSpots.append([pointer1, len(resistance) - 50])

        else:
            if slopeDiff >= abs(lastSlope):
                selectedSpots.append([pointer1, pointer2 - 50])
            pointer1 = pointer2
            pointer2 = pointer1 + n
            currentSlope = 0
            lastSlope = 10

    return selectedSpots


def selectPeriods(df, delta_t):
    pointer = 5
    endSpots = []
    setPoints = []
    while pointer < len(df) - 3:
        if (int(df.loc[pointer, 'Target ppm']) - int(df.loc[pointer - 1, 'Target ppm'])) != 0:
            endSpots.append(pointer - 1)
            pointer += 1
        else:
            pointer += 1
    endSpots.append(len(df) - 3)
    for item in endSpots:
        setPoints.append([item - delta_t, item])
    return setPoints
