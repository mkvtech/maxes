import pandas as pd
import numpy as np
import multiprocessing
import tqdm
import pm4py
from pm4py.algo.evaluation.replay_fitness.variants import token_replay as fitness_tbr
from pm4py.algo.evaluation.generalization.variants import token_based as generalization_tbr
from pm4py.algo.evaluation.precision.variants import etconformance_token as precision_tbr

import maxes.notebooks.utils
import maxes.utils
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3

def experiment(params):
    traces_count, samples_count = params
    results = []

    file_path = maxes.notebooks.utils.get_data_path("other/simple.xes")
    log = maxes.notebooks.utils.load_xes(file_path)

    log_pm4py = pm4py.read_xes(file_path, show_progress_bar=False)

    net, im, fm = pm4py.discover_petri_net_inductive(log_pm4py)

    # Initialize generator
    xes_generator = XesGenerator3(attributes_models=[], traces_count=traces_count)
    xes_generator.fit(log)

    for sample_index in range(samples_count):
        generated_log = xes_generator.generate()

        for trace_index, trace in enumerate(generated_log.traces):
            trace.attributes["concept:name"] = str(trace_index)

        generated_log.update_df(with_trace_attributes=True)
        generated_log_pm4py = generated_log.df

        fitness = fitness_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})
        generalization = generalization_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})
        precision = precision_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})

        results.append({
            'traces_count': traces_count,
            'sample_index': sample_index,
            'perc_fit_traces': fitness['perc_fit_traces'],
            'average_trace_fitness': fitness['average_trace_fitness'],
            'log_fitness': fitness['log_fitness'],
            'percentage_of_fitting_traces': fitness['percentage_of_fitting_traces'],
            'generalization': generalization,
            'precision': precision
        })

    return results

if __name__ == '__main__':
    # traces_count_ratios = np.arange(0.1, 1.1, 0.1)
    traces_count_ratios = np.array([
        0.001,
        0.002,
        0.003,
        0.004,
        0.005,
        0.006,
        0.007,
        0.008,
        0.009,
        0.01,
        0.02,
        0.03,
        0.04,
        0.05,
        0.06,
        0.07,
        0.08,
        0.09,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0
    ])
    samples_count = 100

    file_path = maxes.notebooks.utils.get_data_path("other/simple.xes")
    log = maxes.notebooks.utils.load_xes(file_path)

    traces_counts = np.rint(traces_count_ratios * len(log.traces))

    params = []
    for traces_count in traces_counts:
        params.append((int(traces_count), samples_count))

    results = []
    process_pool = multiprocessing.Pool()
    for result in tqdm.tqdm(process_pool.imap_unordered(experiment, params), total=len(params)):
        results.extend(result)

    results = pd.DataFrame(results)
    results.to_csv('output/experiment-46-1.csv')
