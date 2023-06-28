#
#Stages: The stages in the problem are the days t = 1, 2, ..., 10 before day 10.
#States: The states within each stage are the number of available rooms for the night of day 10.
#Decision: The decision to be made at each stage and state is the price to charge for the rooms on day 10.
#Source of uncertainty: The source of uncertainty is the number of rooms that customers will attempt to book at a given price, modeled by a Poisson random variable with mean M(t, P).
#Interpretation of the value function f_t(i): The value function f_t(i) represents the maximum expected revenue obtainable from the remaining i rooms on day t until day 10.

import math
import numpy as np
from binomialPoisson import *

# Python code for Poisson and Binomial distribution
#   Prof. Jonathan Eckstein

import numpy
import math


# Returns the distribution of a Poisson variable with mean "mean",
# truncated so its largest possible value is "maxVal".
#
# Uses that first term is exp(-M) and then
# Each successive term is previous one times M/i

def poisson(mean, maxVal):
    dist = np.zeros(maxVal+1)
    log_term = -mean
    for i in range(maxVal):
        log_dist_i = log_term + i * np.log(mean) - np.log(math.factorial(i))
        dist[i] = np.exp(log_dist_i)
    dist[maxVal] = np.exp(-np.sum(dist))
    return dist



# Returns the binomial distribution with n trials and p chance of
# success per trial
#
# Uses symmetry of the binomial coefficients (n choose k) and (n choose n-k)
# Only loops up through floor(n/2) and computes two terms per iteration
# Computes each binomial coefficient based on the previous one

def binomial(n,p) :
    dist = numpy.zeros(n+1)
    factorialTerm = 1.0
    k = 0
    while True :
        # Following two statements are redundant when k == n/2, but no matter
        dist[k]   = factorialTerm*(p**k)*(1-p)**(n-k)
        dist[n-k] = factorialTerm*(p**(n-k))*(1-p)**k
        factorialTerm *= (n - k)
        k += 1
        if k > n/2 :
            break
        factorialTerm /= k
    return dist

# Constants
beta0 = 3
beta1 = 0.01
beta2 = -0.01
beta3 = 0.0004
prices = [100, 150, 200, 250, 300]
days = 10
rooms = 20

# Mean function
def M(t, P):
    return (beta0 + beta1 * t) * math.exp((beta2 + beta3 * t) * P)

# Dynamic programming function
def hotel_yield_management():
    revenue = [[0] * (rooms + 1) for _ in range(days + 1)]

    for t in range(days - 1, -1, -1):
        for i in range(rooms + 1):
            max_rev = None
            for P in prices:
                mean = M(t + 1, P)
                max_val = min(i, math.ceil(mean))
                probs = poisson(max_val, math.ceil(mean))
                expected_rev = sum([probs[k] * (P * k + revenue[t + 1][i - k]) for k in range(max_val + 1)])
                if max_rev is None or expected_rev > max_rev:
                    max_rev = expected_rev
            revenue[t][i] = max_rev

    return revenue

# Calculate the dynamic programming solution and optimal pricing policy
revenue = hotel_yield_management()
policy = []

remaining_rooms = rooms

for t in range(days):
    max_rev = None
    best_price = 0
    for P in prices:
        max_val = min(remaining_rooms, math.ceil(M(t + 1, P)))
        probs = poisson(max_val, math.ceil(M(t + 1, P)))
        expected_rev = sum([probs[k] * (P * k + revenue[t + 1][remaining_rooms - k]) for k in range(max_val + 1)])
        if max_rev is None or expected_rev > max_rev:
            max_rev = expected_rev
            best_price = P
    policy.append(best_price)
    remaining_rooms -= best_price

# Output the results
print("Optimal pricing policy:", policy)
print("Maximum expected revenue:", revenue[0][20])