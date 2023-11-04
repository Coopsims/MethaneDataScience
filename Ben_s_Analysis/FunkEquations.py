'''

All equations here are useful for predicting ppm based on a figaro CH4 sensor.

'''
import numpy as np
from sympy import log

# Given variables
a = 1.361119
b = -0.758095
c = 0.118785
d = 2.432037
e = 0.942663
f = 0.568506
g = 0.673565
h = 0.938100
i = -0.308766
j = -47.899685
k = 1.201892
l = 3.291883
m = 1.936693
n = 11.455196
o = -2.409027


def Funk_Equation_LowPPM2(X):
    R, H, T = X
    stuff = a ** ((-1 * R / (H ** b)) * c + d) * e ** (-1 * H * f + g) \
            * h ** (-1 * T * i + j) * k ** (-1 * R ** (1 / (T * l)) * m + n) + o
    return stuff


def Funk_Equation_LowPPM(X):
    R, H, T = X
    stuff = 0.972102 ** ((((-1 * R) / (H ** -0.664524)) * -1.681143) + (-1 * H * 1.118612) + (-1 * T * -1.307406)
                         + (((-1 * T) / (H ** 0.236542)) * 1.625877) - 187.456885) - 3.086685
    return stuff


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


def Funk_Equation_FullPPM(X):
    R, H, T = X
    stuff = 0.981309 ** ((((-1 * R) / (H ** -0.359548)) * -15.121040) + (-1 * H * 0.671743) + (-1 * T * -0.008924)
                         - 428.596019) + 17.898183
    return stuff


'''
Temperature was included for this equation as it needs to compromise between the lower ppm needing it and the 
higher ppm not. This equation was trained on 0ppm to 1000ppm with: 
steps:0,2,5,10,20,50,200,400,600,800,1000 PPM 
temperatures: 35, 20, 8  
humidity: 0%, 15%, 30%, 45%, 60%

For inputting data it should be in vector form: [Resistance Ratio, Humidity, Temperature]
resistance Ratio = (𝑉𝑜𝑢𝑡 * (5−𝑉𝑟𝑒𝑓))/(𝑉𝑟𝑒𝑓 * (5−𝑉𝑜𝑢𝑡))
humidity should be entered in the form of a number between 0-100
temperature is in celsius

'''
