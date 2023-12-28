'''

All equations here are useful for predicting ppm based on a figaro CH4 sensor.

'''
import numpy as np
from sympy import log
# a = 0.369232 b = 0.111613 c = -4.714868 d = -0.003684 e = -6.026000 f = 2.455307 g = 0.000230 h = 2.455943 i = -5.899531 j = -2.571275
def Funk_Equation_LowPPM(X):
    R, H, T = X
    ppm_prediction = 0.369232 ** ((((-1 * R) / (H ** 0.111613)) * -4.714868) + (-1 * H * -0.003684) + (-1 * T * -6.026000)
                         + (((-1 * T*2.455307) / (H ** 0.000230)) * 2.455943) -5.899531)  - 2.571275
    return ppm_prediction


'''
At lower ppm temperature has an effect on the resistance ratio meaning this equation is more complex
This equation was trained on 0ppm to 50ppm with 
steps: 0,2,5,10,20,50
temperatures: 35, 20, 8
and humidity 0%, 15%, 30%, 45%, 60%

For inputting data it should be in vector form: [Resistance Ratio, Humidity, Temperature]
resistance Ratio = (𝑉𝑜𝑢𝑡 * (5−𝑉𝑟𝑒𝑓))/(𝑉𝑟𝑒𝑓 * (5−𝑉𝑜𝑢𝑡))
humidity should be entered in the form of a number between 0-100
temperature is in celsius

'''


def Funk_Equation_HighPPM(X):
    R, H, T = X
    stuff = 1.160462 ** ((((-1 * R) / (H ** -0.315336)) * 2.038874) + (-1 * H * -0.060370) + 54.293157) + 14.308195
    return stuff


'''
At higher ppm temperature doesn't have an effect on the resistance ratio as such is not useful in the equation.
This equation does not have temperature, but I still kept it as an input to make switching between equations easier. 
This equation was trained on 0ppm to 1000ppm with: 
steps:0,200,400,600,800,1000 PPM
temperatures: 35, 20, 8
and humidity 0%, 15%, 30%, 45%, 60%

For inputting data it should be in vector form: [Resistance Ratio, Humidity, Temperature]
resistance Ratio = (𝑉𝑜𝑢𝑡 * (5−𝑉𝑟𝑒𝑓))/(𝑉𝑟𝑒𝑓 * (5−𝑉𝑜𝑢𝑡))
humidity should be entered in the form of a number between 0-100
temperature is in celsius

'''