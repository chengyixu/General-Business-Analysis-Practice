import numpy as np
import pandas as pd

# Define input variables
num_techs = [2, 3, 4, 5]
phone_probs = [0.03, 0.04, 0.04, 0.07, 0.06, 0.07, 0.09, 0.05, 0.03, 0.04, 0.02, 0.03, 0.04, 0.06, 0.06, 0.07, 0.07, 0.05, 0.04, 0.03, 0.01]
major_prob = 0.28

# Define output variables
tech_hours = np.zeros(5)
total_hours = 0
phones_repaired = 0
total_cost = 0

# Define simulation model
def sim_model(num_techs):
    global tech_hours, total_hours, phones_repaired, total_cost
    tech_hours = np.zeros(5)
    total_hours = 0
    phones_repaired = 0
    total_cost = 0
    
    for day in range(1000):
        # Determine the number of phones to be repaired
        num_phones = np.random.choice(range(10, 31), p=phone_probs)
        
        # Determine the number of major repairs
        num_major = np.random.binomial(num_phones, major_prob)
        
        # Determine the number of minor repairs
        num_minor = num_phones - num_major
        
        # Assign phones to technicians
        phones_per_tech = num_minor // num_techs
        for i in range(num_techs):
            tech_hours[i] = phones_per_tech * 0.75 + (num_major * 0.75) / num_techs + (num_minor % num_techs) * 0.45 / num_techs
        
        # Calculate total hours and cost
        total_hours += tech_hours.sum()
        phones_repaired += num_phones
        if num_techs < num_minor:
            total_cost += num_minor * 0.45 + num_major * 0.75 + (num_minor - num_techs) * 0.85
        else:
            total_cost += num_minor * 0.45 + num_major * 0.75
        
    return total_cost / 1000

# Run simulations with different numbers of technicians
results = []
for n in num_techs:
    result = [sim_model(n) for i in range(100)]
    results.append(np.mean(result))

# Print the results
for i in range(len(num_techs)):
    print(f"Average cost per day with {num_techs[i]} technicians: {results[i]:.2f}")
