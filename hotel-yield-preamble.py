import numpy
from binomialPoisson import *
import math

hugeNumber = float("inf")

stages       = 10
roomCapacity = 20

roomRates  = numpy.array([100,150,200,250,300])

beta0 = 3
beta1 = 0.01
beta2 = -0.01
beta3 = 0.0004
