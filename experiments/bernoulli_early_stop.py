##
# Goal: understand the impact of early peeking + stopping
##
import numpy as np
from bayesab.testab import testAB, Bernoulli

samples = 2
max_samples = 500
peeks = range(1, max_samples, 250)

v_a = np.random.binomial(1, .6, max_samples)
v_b = np.random.binomial(1, .48, max_samples)


total_results = []
for sample in range(samples):
    sample_results = []
    for peek in peeks:
        sample_results.append(testAB(v_a, v_b, Bernoulli(1,1)))
    total_results.append(sample_results)

print([str(j) for i in total_results for j in i])
