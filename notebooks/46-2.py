import pandas as pd
import numpy as np
import multiprocessing
import tqdm
import os
import pm4py
from pm4py.algo.evaluation.replay_fitness.variants import token_replay as fitness_tbr
from pm4py.algo.evaluation.generalization.variants import token_based as generalization_tbr
from pm4py.algo.evaluation.precision.variants import etconformance_token as precision_tbr

from maxes.xes_loader2 import XesLoader
import maxes.notebooks.utils
import maxes.utils
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3

def experiment_process(args):

    job_index = args["job_index"]
    lock = args["lock"]
    file_key = args['file_key']
    file_path = args['file_path']
    traces_count = args['traces_count']
    samples_count = args['samples_count']

    progress_bar = None
    with lock:
        progress_bar = tqdm.tqdm(
            desc=f"JID={job_index}, TC={traces_count}",
            total=samples_count,
            position=job_index + 1,
            leave=False
        )

    results = []

    log = XesLoader().load(file_path)
    # log = maxes.notebooks.utils.load_xes(file_path)

    log_pm4py = pm4py.read_xes(file_path, show_progress_bar=False)

    net, im, fm = pm4py.discover_petri_net_inductive(log_pm4py)

    # Initialize generator
    xes_generator = XesGenerator3(attributes_models=[], traces_count=traces_count)
    xes_generator.fit(log)

    for sample_index in range(samples_count):
        try:
            generated_log = xes_generator.generate()
        except:
            results.append({
                'file_key': file_key,
                'traces_count': traces_count,
                'sample_index': sample_index,
                'perc_fit_traces': 0,
                'average_trace_fitness': 0,
                'log_fitness': 0,
                'percentage_of_fitting_traces': 0,
                'generalization': 0,
                'precision': 0,
                "success": False
            })
            continue

        for trace_index, trace in enumerate(generated_log.traces):
            trace.attributes["concept:name"] = str(trace_index)

        generated_log.update_df(with_trace_attributes=True)
        generated_log_pm4py = generated_log.df

        fitness = fitness_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})
        generalization = generalization_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})
        precision = precision_tbr.apply(generated_log_pm4py, net, im, fm, {'show_progress_bar': False})

        results.append({
            'file_key': file_key,
            'traces_count': traces_count,
            'sample_index': sample_index,
            'perc_fit_traces': fitness['perc_fit_traces'],
            'average_trace_fitness': fitness['average_trace_fitness'],
            'log_fitness': fitness['log_fitness'],
            'percentage_of_fitting_traces': fitness['percentage_of_fitting_traces'],
            'generalization': generalization,
            'precision': precision,
            "success": True
        })

        with lock:
            progress_bar.update(1)

    with lock:
        progress_bar.close()

    return results

def experiment_main(file_key, file_path, traces_counts, samples_count, lock):
    traces_counts.sort()
    traces_counts.reverse()

    file_path = maxes.notebooks.utils.get_data_path(file_path)

    params = []
    for i, traces_count in enumerate(traces_counts):
        params.append({
            "job_index": i,
            "lock": lock,
            "file_key": file_key,
            "file_path": file_path,
            "traces_count": int(traces_count),
            "samples_count": samples_count,
        })

    results = []
    process_pool = multiprocessing.Pool()
    for result in tqdm.tqdm(process_pool.imap_unordered(experiment_process, params), total=len(params), position=0):
        results.extend(result)

    results = pd.DataFrame(results)

    export_path = os.path.join("output", f"experiment-46-4_{file_key}.csv")
    results.to_csv(export_path)


if __name__ == '__main__':
    lock = multiprocessing.Manager().Lock()

    #     files = {
    #     'activities_detailed_labour': 'Activities of daily living of several individuals_1_all/data/activitylog_uci_detailed_labour.xes/activitylog_uci_detailed_labour.xes',
    #     'activities_detailed_weekends': 'Activities of daily living of several individuals_1_all/data/activitylog_uci_detailed_weekends.xes/activitylog_uci_detailed_weekends.xes',
    #     'activities_edited_hh102_labour': 'Activities of daily living of several individuals_1_all/data/edited_hh102_labour.xes/edited_hh102_labour.xes',
    #     'activities_edited_hh102_weekends': 'Activities of daily living of several individuals_1_all/data/edited_hh102_weekends.xes/edited_hh102_weekends.xes',
    #     'activities_edited_hh104_labour': 'Activities of daily living of several individuals_1_all/data/edited_hh104_labour.xes/edited_hh104_labour.xes',
    #     'activities_edited_hh104_weekends': 'Activities of daily living of several individuals_1_all/data/edited_hh104_weekends.xes/edited_hh104_weekends.xes',
    #     'activities_edited_hh110_labour': 'Activities of daily living of several individuals_1_all/data/edited_hh110_labour.xes/edited_hh110_labour.xes',
    #     'activities_edited_hh110_weekends': 'Activities of daily living of several individuals_1_all/data/edited_hh110_weekends.xes/edited_hh110_weekends.xes',
    # }

    # 	file_key	traces_count	events_count_mean
    # 0	activities_detailed_labour	25	55.680000
    # 1	activities_detailed_weekends	10	48.800000
    # 2	activities_edited_hh102_labour	18	64.000000
    # 3	activities_edited_hh102_weekends	7	60.000000
    # 4	activities_edited_hh104_labour	43	97.674419
    # 5	activities_edited_hh104_weekends	18	96.000000
    # 6	activities_edited_hh110_labour	21	66.190476
    # 7	activities_edited_hh110_weekends	6	61.333333

    # experiment_main(
    #     file_key="activities_detailed_labour",
    #     file_path="Activities of daily living of several individuals_1_all/data/activitylog_uci_detailed_labour.xes/activitylog_uci_detailed_labour.xes",
    #     traces_counts=[
    #         # over size
    #         55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
    #         30, 35, 40, 45, 50,

    #         # below size
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18, 20, 22, 24,
    #         12, 14, 16, 18, 20, 22, 24,

    #         # size
    #         25,
    #         25,
    #     ],
    #     samples_count=20,
    #     export_path="output/experiment-46_activities_detailed_labour.csv"
    # )

    # experiment_main(
    #     file_key="activities_detailed_weekends",
    #     file_path="Activities of daily living of several individuals_1_all/data/activitylog_uci_detailed_weekends.xes/activitylog_uci_detailed_weekends.xes",
    #     traces_counts=[
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10
    #     ],
    #     samples_count=10,
    #     export_path="output/experiment-46_activities_detailed_weekends.csv"
    # )

    # experiment_main(
    #     file_key="activities_edited_hh102_labour",
    #     file_path="Activities of daily living of several individuals_1_all/data/edited_hh102_labour.xes/edited_hh102_labour.xes",
    #     traces_counts=[
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18
    #     ],
    #     samples_count=10,
    #     export_path="output/experiment-46_activities_edited_hh102_labour.csv"
    # )

    # experiment_main(
    #     file_key="activities_edited_hh102_weekends",
    #     file_path="Activities of daily living of several individuals_1_all/data/edited_hh102_weekends.xes/edited_hh102_weekends.xes",
    #     traces_counts=[
    #         1,  2,  3,  4,  5,  6,  7
    #     ],
    #     samples_count=10,
    #     export_path="output/experiment-46_activities_edited_hh102_weekends.csv"
    # )







    # experiment_main(
    #     file_key="activities_edited_hh104_labour",
    #     file_path="Activities of daily living of several individuals_1_all/data/edited_hh104_labour.xes/edited_hh104_labour.xes",
    #     traces_counts=[
    #         # below size
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18, 20,
    #         25, 30,
    #         35, 40,

    #         # size
    #         43,

    #         # over size
    #         45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
    #     ],
    #     samples_count=20,
    #     lock=lock
    # )

    # experiment_main(
    #     file_key="ccc19",
    #     file_path="/vt/md/maxes/maxes/data/ccc19/data/CCC19 - Log XES.xes",
    #     traces_counts=[
    #         # below size
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18,

    #         # size
    #         20,

    #         # over size
    #         25, 30,
    #         35, 40,
    #     ],
    #     samples_count=20,
    #     lock=lock
    # )

    # experiment_main(
    #     file_key="photo_copier",
    #     file_path="/vt/md/maxes/maxes/data/photo_copier/event-log.xes",
    #     traces_counts=[
    #         # below size
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18, 20, 22, 24, 26, 28, 30,
    #         35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95,

    #         # size
    #         100,

    #         # over size
    #         110, 120, 130, 140, 150, 160, 170, 180, 190, 200
    #     ],
    #     samples_count=20,
    #     lock=lock
    # )

    # experiment_main(
    #     file_key="software_data_analytics__alarm_system",
    #     file_path="/vt/md/maxes/maxes/data/software_data_analytics/processed/alarm_system.xes",
    #     traces_counts=[
    #         # below size
    #         1,  2,  3,  4,

    #         # size
    #         5,

    #         # over size
    #         6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
    #     ],
    #     samples_count=40,
    #     lock=lock
    # )

    # experiment_main(
    #     file_key="bpic2020__request_for_payment",
    #     file_path="/vt/md/maxes/maxes/data/bpic2020/processed/request_for_payment.xes",
    #     traces_counts=[
    #         # below size
    #         1, 2, 3, 4, 5,
    #         6, 8, 10,
    #         12, 14, 16, 18, 20,
    #         30, 40, 50, 60, 70, 80, 90, 100,
    #         100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
    #         1000, 2000, 3000, 4000, 5000, 6000,

    #         # size
    #         6886,

    #         # over size
    #         8000, 9000, 10000, 11000, 12000, 13000, 14000
    #     ],
    #     samples_count=40,
    #     lock=lock
    # )

    experiment_main(
        file_key="simple",
        file_path="/vt/md/maxes/maxes/data/other/simple.xes",
        traces_counts=[
            # below size
            1, 2, 3, 4, 5,
            6, 8, 10,
            12, 14, 16, 18, 20,
            30, 40, 50, 60, 70, 80, 90, 100,
            100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
            1000, 1500, 2000, 2500, 3000,

            # size
            3512,

            # over size
            4000, 4500, 5000, 5500, 6000, 6500, 7000
        ],
        samples_count=20,
        lock=lock
    )





    # experiment_main(
    #     file_key="activities_edited_hh104_weekends",
    #     file_path="Activities of daily living of several individuals_1_all/data/edited_hh104_weekends.xes/edited_hh104_weekends.xes",
    #     traces_counts=[
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18
    #     ],
    #     samples_count=10,
    #     export_path="output/experiment-46_activities_edited_hh104_weekends.csv"
    # )

    # experiment_main(
    #     file_key="activities_edited_hh110_labour",
    #     file_path="Activities of daily living of several individuals_1_all/data/edited_hh110_labour.xes/edited_hh110_labour.xes",
    #     traces_counts=[
    #         1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
    #         12, 14, 16, 18, 20,
    #         21
    #     ],
    #     samples_count=10,
    #     export_path="output/experiment-46_activities_edited_hh110_labour.csv"
    # )

    # experiment_main(
    #     file_key="activities_edited_hh110_weekends",
    #     file_path="Activities of daily living of several individuals_1_all/data/edited_hh110_weekends.xes/edited_hh110_weekends.xes",
    #     traces_counts=[
    #         1,  2,  3,  4,  5,  6
    #     ],
    #     samples_count=10,
    #     export_path="output/experiment-46_activities_edited_hh110_weekends.csv"
    # )
