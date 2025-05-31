import pm4py
import numpy as np
import pandas as pd
import os
import tqdm
import math
import datetime
import multiprocessing

from pm4py.algo.evaluation.replay_fitness.variants import token_replay as fitness_tbr
from pm4py.algo.evaluation.generalization.variants import token_based as generalization_tbr
from pm4py.algo.evaluation.precision.variants import etconformance_token as precision_tbr

import maxes.utils
from maxes.xes_loader2 import XesLog
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def experiment_process(args):
    job_index = args["job_index"]
    lock = args["lock"]
    # rng_seed = args["rng_seed"]
    rng_seed = datetime.datetime.now().microsecond
    file_key = args['file_key']
    file_path = args["file_path"]
    fold_size = args["fold_size"]
    fold_size_attempts_count = args["fold_size_attempts_count"]
    fold_generation_attempts_count = args["fold_generation_attempts_count"]

    log_pm4py = pm4py.read_xes(file_path, show_progress_bar=False)
    net, im, fm = pm4py.discover_petri_net_inductive(log_pm4py)

    traces_concept_names = log_pm4py['case:concept:name'].unique()
    rng = np.random.default_rng(rng_seed)

    results = []

    traces_count = len(traces_concept_names)
    progress_bar_total = fold_size_attempts_count * math.ceil(traces_count / fold_size) * fold_generation_attempts_count

    progress_bar = None
    with lock:
        progress_bar = tqdm.tqdm(
            desc=f"JID={job_index}, FS={fold_size}",
            total=progress_bar_total,
            position=job_index + 1,
            leave=False
        )

    for fold_size_attempt in range(fold_size_attempts_count):
        shuffled_traces_concept_names = list(traces_concept_names)
        rng.shuffle(shuffled_traces_concept_names)

        folds = chunks(traces_concept_names, fold_size)

        for fold_index, fold in enumerate(folds):
            filtered_log_df = log_pm4py[log_pm4py['case:concept:name'].isin(fold)]

            # load log
            log = XesLog()
            log.df = filtered_log_df
            log.update_traces_from_df()

            # Initialize generator
            xes_generator = XesGenerator3(attributes_models=[])
            xes_generator.fit(log)

            for fold_generation_attempt in range(fold_generation_attempts_count):
                generated_log = None

                try:
                    generated_log = xes_generator.generate()
                except maxes.utils.CustomStackOverflowException as e:
                    results.append({
                        "file_key": file_key,
                        "fold_size": fold_size,
                        "fold_size_attempt": fold_size_attempt,
                        "fold_index": fold_index,
                        "fold_generation_attempt": fold_generation_attempt,

                        "perc_fit_traces": 0,
                        "average_trace_fitness": 0,
                        "log_fitness": 0,
                        "percentage_of_fitting_traces": 0,
                        "generalization": 0,
                        "precision": 0,

                        "success": False
                    })

                    with lock:
                        progress_bar.update(1)

                    continue

                generated_log = xes_generator.generate()
                for trace_index, trace in enumerate(generated_log.traces):
                    trace.attributes["concept:name"] = str(trace_index)

                generated_log.update_df(with_trace_attributes=True)
                generated_log_pm4py = generated_log.df

                fitness = fitness_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})
                generalization = generalization_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})
                precision = precision_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})

                results.append({
                    "file_key": file_key,
                    "fold_size": fold_size,
                    "fold_size_attempt": fold_size_attempt,
                    "fold_index": fold_index,
                    "fold_generation_attempt": fold_generation_attempt,

                    "perc_fit_traces": fitness["perc_fit_traces"],
                    "average_trace_fitness": fitness["average_trace_fitness"],
                    "log_fitness": fitness["log_fitness"],
                    "percentage_of_fitting_traces": fitness["percentage_of_fitting_traces"],
                    "generalization": generalization,
                    "precision": precision,

                    "success": True
                })

                with lock:
                    progress_bar.update(1)

    with lock:
        progress_bar.close()

    return results

def experiment_main(file_key, file_path, fold_sizes, fold_size_attempts_count, fold_generation_attempts_count, lock):
    fold_sizes.sort()

    params = []
    for i, fold_size in enumerate(fold_sizes):
        params.append({
            "job_index": i,
            "lock": lock,
            "file_key": file_key,
            "file_path": file_path,
            "fold_size": fold_size,
            "fold_size_attempts_count": fold_size_attempts_count,
            "fold_generation_attempts_count": fold_generation_attempts_count
        })

    results = []
    process_pool = multiprocessing.Pool()
    for result in tqdm.tqdm(process_pool.imap_unordered(experiment_process, params), total=len(params), position=0):
        results.extend(result)

    results = pd.DataFrame(results)

    export_path = os.path.join("output", f"experiment-46-5_{file_key}.csv")
    results.to_csv(export_path)

if __name__ == '__main__':
    lock = multiprocessing.Manager().Lock()


    # experiment_main(
    #     file_key="simple",
    #     file_path="/vt/md/maxes/maxes/data/other/simple.xes",
    #     fold_sizes=[
    #         # below size
    #         1, 2, 3, 4, 5,
    #         6, 8, 10,
    #         12, 14, 16, 18, 20,
    #         30, 40, 50, 60, 70, 80, 90, 100,
    #         100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
    #         1000, 1500, 2000, 2500, 3000,

    #         # size
    #         3512,
    #     ],
    #     fold_size_attempts_count=3,
    #     fold_generation_attempts_count=3,
    #     lock=lock
    # )



    # experiment_main(
    #     file_key="bpic2020__request_for_payment",
    #     file_path="/vt/md/maxes/maxes/data/bpic2020/processed/request_for_payment.xes",
    #     fold_sizes=[
    #         # below size
    #         1, 2, 3, 4, 5,
    #         6, 8, 10,
    #         12, 14, 16, 18, 20,
    #         30, 40, 50, 60, 70, 80, 90, 100,
    #         100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
    #         1000, 2000, 3000, 4000, 5000, 6000,

    #         # size
    #         6886,
    #     ],
    #     fold_size_attempts_count=1,
    #     fold_generation_attempts_count=1,
    #     lock=lock
    # )



    # TODO
    # experiment_main(
    #     file_key="software_data_analytics__alarm_system",
    #     file_path="/vt/md/maxes/maxes/data/software_data_analytics/processed/alarm_system.xes",
    #     fold_sizes=[
    #         # below size
    #         1,  2,  3,  4,

    #         # size
    #         5,
    #     ],
    #     fold_size_attempts_count=1,
    #     fold_generation_attempts_count=1,
    #     lock=lock
    # )



    # experiment_main(
    #     file_key="photo_copier",
    #     file_path="/vt/md/maxes/maxes/data/photo_copier/event-log.xes",
    #     fold_sizes=[
    #         # below size
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18, 20, 22, 24, 26, 28, 30,
    #         35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95,

    #         # size
    #         100,
    #     ],
    #     fold_size_attempts_count=1,
    #     fold_generation_attempts_count=1,
    #     lock=lock
    # )



    # experiment_main(
    #     file_key="ccc19",
    #     file_path="/vt/md/maxes/maxes/data/ccc19/data/CCC19 - Log XES.xes",
    #     fold_sizes=[
    #         # below size
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18,

    #         # size
    #         20,
    #     ],
    #     fold_size_attempts_count=3,
    #     fold_generation_attempts_count=3,
    #     lock=lock
    # )




    experiment_main(
        file_key="activities_edited_hh104_labour",
        file_path="/vt/md/maxes/maxes/data/Activities of daily living of several individuals_1_all/data/edited_hh104_labour.xes/edited_hh104_labour.xes",
        fold_sizes=[
            # below size
            1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
            12, 14, 16, 18, 20,
            25, 30,
            35, 40,

            # size
            43,
        ],
        fold_size_attempts_count=3,
        fold_generation_attempts_count=3,
        lock=lock
    )
