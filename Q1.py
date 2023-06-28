#
#The stages are the weeks, from week 1 to week 12.
#The states are the number of units carried over from the previous week.
#The decision to be made is the number of units to attempt to repair.
#The source of uncertainty is the probability that the repair operation for each unit will succeed or fail (85% chance of success and 15% chance of failure).
#The value function f_t(i) represents the expected present value of the cost of the operation at week t with i units carried over from the previous week.

import numpy as np
from binomialPoisson import *

# Constants
num_weeks = 12
max_units = 15
repair_probs = binomial(8, 0.85)
repair_costs = np.array([0, 100, 110, 120, 130, 190, 200, 210, 220])
external_cost = 150
waiting_cost = 9
interest_rate = 0.001

# Initialize the value function table
value_table = np.zeros((num_weeks + 1, max_units + 1))
policy_table = np.zeros((num_weeks, max_units + 1))

# Iterate over weeks in reverse
for week in range(num_weeks - 1, -1, -1):
    # Iterate over the number of carried-over units
    for carried_units in range(max_units + 1):
        total_units = carried_units + 3
        min_cost = float('inf')
        best_repair_decision = -1

        # Iterate over possible repair decisions
        for repair_decision in range(min(8, total_units) + 1):
            expected_cost = repair_costs[repair_decision]
            waiting_units = total_units - repair_decision

            # Iterate over successful repairs
            for successful_repairs in range(repair_decision + 1):
                remaining_units = waiting_units - successful_repairs
                if remaining_units > max_units:
                    external_repair_units = remaining_units - max_units
                    remaining_units = max_units
                    expected_cost += external_cost * external_repair_units

                remaining_cost = waiting_cost * remaining_units + repair_probs[successful_repairs] * value_table[week + 1, remaining_units]
                expected_cost += remaining_cost / (1 + interest_rate)

            if expected_cost < min_cost:
                min_cost = expected_cost
                best_repair_decision = repair_decision

        value_table[week, carried_units] = min_cost
        policy_table[week, carried_units] = best_repair_decision

print("Optimal number of units to attempt to repair each week:")
print(policy_table)

