##
# Goal: understand the impact of early peeking + stopping
##
import numpy as np
from bayesab.testab import testAB, Bernoulli
import pandas as pd
import matplotlib
from multiprocessing import Pool, TimeoutError
import time
import os
import random
import sys
import tqdm


samples = 10000
max_samples = 100000
peeks = list(range(1, max_samples, 1000))



total_results = []


def calculate_sample(sample):
    # seed the random for multiproc reasons
    np.random.seed(sample + random.randint(0, 100))
    v_a = np.random.binomial(1, .5, max_samples)
    v_b = np.random.binomial(1, .3, max_samples)
    sample_results = {'step':[], 'sample': sample}
    for i in range(len(peeks)):
        peek = peeks[i]
        sample_results['step'].append(peek)
        s_map = testAB(v_a[:peek], v_b[:peek], Bernoulli(1,1)).stats_map()
        for key, value in s_map.items():
            if key in sample_results:
                sample_results[key].append(value)
            else:
                sample_results[key] = [value]
    return pd.DataFrame.from_dict(sample_results)

pool = Pool(processes=8)

total_results_th = []


for data in tqdm.tqdm(pool.imap(calculate_sample, range(samples)), total=samples):
    total_results_th.append(data)

#total_results_th = pool.map(calculate_sample, range(samples))
total_results = pd.concat(total_results_th)

total_results.to_csv('./b_early_stop_simulation_results_{}_{}_v2.csv'.format(samples, max_samples))
#
# import seaborn as sns
# sns.set(style="darkgrid")
#
# # Load an example dataset with long-form data
#
# # Plot the responses for different events and regions
# sns.lineplot(x="step", y="p_success",
#              data=total_results, estimator=None, units='sample')
# matplotlib.pyplot.show()
# sns.lineplot(x="step", y="a_b_difference",
#              data=total_results, estimator=None, units='sample')
#
# matplotlib.pyplot.show()
#
# sns.lineplot(x="step", y="a_fit",
#              data=total_results, estimator=None, units='sample')
#
# matplotlib.pyplot.show()
#
# sns.lineplot(x="step", y="b_fit",
#              data=total_results, estimator=None, units='sample')
#
#
# matplotlib.pyplot.show()
#
# sns.lineplot(x="step", y="a_loss_ratio",
#              data=total_results, estimator=None, units='sample')
#
#
# matplotlib.pyplot.show()
#

