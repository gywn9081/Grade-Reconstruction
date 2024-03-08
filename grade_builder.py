import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Remove to run with out graphing
import seaborn as sns
sns.set_theme()

# Set-up numpy generator
rg = np.random.default_rng()

# Add known values
low = 0
high = 50
d_mean = 5.93
d_median = 15
q2 = 10
q3 = 20

# When samples is lower graphs drawn needs to go up in order to smooth
samples = 180

# Following are parameters for confindence
entries_left = samples - 2
error = 0.01
max_mods = 10
modify_values = True

mod_step_size = d_mean / 100

# Scale with to be constant
left_width = (q2 - low)
q2_width = (d_median - q2)
q3_width = (q3 - d_median)
right_width = (high - q3)

# Vals directly depended on set vars
samples_per_space = int(samples / 4)
array_array = []
test_array = np.array([low, high])

# Usable offsets
width_array = [left_width, q2_width, q3_width, right_width]
values_offset = [low, q2, d_median, q3]


# Number of graphs to make
num_graphs = 18000

for x in range(num_graphs):
    for offset, width in zip(values_offset, width_array):
        test_array = np.sort(np.concatenate(
            [test_array, (rg.random(size=samples_per_space) * width) + offset]))
    array_array.append(pd.Series(test_array))
    test_array = np.array([low, high])
test_array = pd.concat(array_array, axis=1)
test_array = test_array.mean(axis=1)


steps = 0

while (modify_values):
    steps += 1
    # (abs(test_array.median() - d_median) > error)
    if (((test_array.mean() - d_mean) > error)):
        if (steps > max_mods):
            break
        # if ((steps % int(num_graphs / 4)) == 0):
        test_array = np.sort(test_array)

        offset_mod = int(
            (rg.random(size=1)[0] * (test_array.shape[0] / 2)) + 1)
        # print(offset_mod)
        test_array[-1::offset_mod] += mod_step_size
        test_array[offset_mod] -= mod_step_size
    break

# Reduce number of bins until not to noisy
# This will just give a general shape
sns.histplot(data=test_array, bins=(10))

print(f'Target Mean: {d_mean}, Target Median {d_median}')
print(f'Mean: {test_array.mean()}, Median: {np.median(test_array)}')
print(
    f'Mean Error {d_mean - test_array.mean()}, Median Error {d_median - np.median(test_array)}')
print(f'Mod steps taken {steps}')
