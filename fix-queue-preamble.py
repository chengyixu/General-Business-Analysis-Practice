import numpy
from binomialPoisson import *

hugeNumber = float("inf")

queueCapacity = 15
chanceCanFix  = 0.85
waitCost      = 9.0
inflowRate    = 3
costToFix     = numpy.array([  0.0, 100.0, 110.0, 120.0, 130.0, 
                                    190.0, 200.0, 210.0, 220.0])
maxCanFix     = 8
overflowCost  = 150.0

initialWaiting = 2

stages = 12

discountRate = 0.001
beta = 1.0/(1.0 + discountRate)
