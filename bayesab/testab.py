import numpy as np
import scipy.stats as stats


class Distribution:
    def infer_prosterior(self, data):
        pass

    def sample(self, n):
        pass

    def transform_to_evidence_distrib(self, data):
        return data


# Bernoulli distribution with beta prior
class Bernoulli(Distribution):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def infer_prosterior(self, data):
        alpha = sum(data) + self.alpha
        beta = len(data) - sum(data) + self.beta
        return Bernoulli(alpha, beta)

    def sample(self, n):
        return np.random.beta(self.alpha, self.beta, n)

    def transform_to_evidence_distrib(self, data):
        return [np.random.binomial(1,i) for i in data]


class TestResults():
    def __init__(self, **kwargs):
        self.kwargs = kwargs


    def __str__(self):
        results = 'P (A > B) by {}%: {}%\n'.format(self.kwargs['target_lift'], self.kwargs['p_success']) \
                + 'A vs B KS stat: {} p-value: {}\n'.format(self.kwargs['a_b_difference'].statistic, self.kwargs['a_b_difference'].pvalue) \
                + 'A sample vs A KS stat: {} p-value: {}\n'.format(self.kwargs['a_fit'].statistic, self.kwargs['a_fit'].pvalue) \
                + 'B sample vs B KS stat: {} p-value: {}\n'.format(self.kwargs['b_fit'].statistic, self.kwargs['b_fit'].pvalue)


        return results


def testAB(a, b, distribution, monte_carlo_samples=1000, p_lift=0):
    prosterior_a = distribution.infer_prosterior(a)
    prosterior_b = distribution.infer_prosterior(b)

    sample_a = prosterior_a.sample(monte_carlo_samples)
    sample_b = prosterior_b.sample(monte_carlo_samples)

    lifts = [(a - b) / b for a,b in zip(sample_a,sample_b)]

    conf_a_gt_b = len(list(filter(lambda i: i > p_lift, lifts))) / len(lifts)

    bi_sample_a = prosterior_a.transform_to_evidence_distrib(sample_a)
    bi_sample_b = prosterior_b.transform_to_evidence_distrib(sample_b)

    return TestResults(p_success = conf_a_gt_b * 100,
                       target_lift = p_lift,
                       a_b_difference =  stats.ks_2samp(a, b),
                       a_fit = stats.ks_2samp(a, bi_sample_a),
                       b_fit = stats.ks_2samp(b, bi_sample_b),
                       prosterior_a = prosterior_a,
                       prosterior_b = prosterior_b)
