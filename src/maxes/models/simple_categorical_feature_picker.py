from collections import defaultdict

import maxes.utils

class SimpleCategoricalFeaturePicker:
    def __init__(self): pass

    def fit(self, data):
        self.counts_ = defaultdict(lambda: 0)

        for case in data:
            self.counts_[case[0]] += 1

        return self

    def sample(self, n_samples = 1):
        return maxes.utils.choices(self.counts_, n_samples)
