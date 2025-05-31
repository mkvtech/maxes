import multiprocessing
import tqdm
import pandas as pd
import numpy as np

import maxes.data.load_files
import maxes.notebooks.utils
from maxes.utils import measured_time
from maxes.xes_loader2 import XesLoader
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3 as XesGenerator

from maxes.metrics.mean_difference import (
    compute_best_match_categorical,
    compute_best_match_numerical,
)


def convert_timestamp_to_seconds_since_first(
    df: pd.DataFrame, columns=["time:timestamp"]
):
    new_df = df.copy(deep=True)
    for column in columns:
        new_df[column] = (new_df[column] - new_df[column].min()).dt.total_seconds()
    return new_df


def experiment_process(args):
    file_path = args["file_path"]
    random_state = args["random_state"]
    traces_count = args["traces_count"]
    identification_columns = args["identification_columns"]
    categorical_difference_columns = args["categorical_difference_columns"]
    numerical_difference_columns = args["numerical_difference_columns"]

    with measured_time() as full_timer:
        rng = np.random.default_rng(random_state)

        loader = XesLoader()

        with measured_time() as timer:
            original_log = loader.load(file_path)
        loading_time = timer()

        generator = XesGenerator(rng=rng, generate_traces_count=traces_count)

        with measured_time() as timer:
            generator.fit(original_log)
        training_time = timer()

        with measured_time() as timer:
            generated_log = generator.generate()
        generation_time = timer()

        # compute_best_match_categorical
        with measured_time() as timer:
            score_categorical = compute_best_match_categorical(
                original_log.df,
                generated_log.df,
                difference_columns=categorical_difference_columns,
                identification_columns=identification_columns,
            )
        computing_categorical_score_time = timer()

        # compute_best_match_numerical
        processed_original_df = convert_timestamp_to_seconds_since_first(
            original_log.df
        )
        processed_generated_df = convert_timestamp_to_seconds_since_first(
            generated_log.df
        )

        with measured_time() as timer:
            score_numerical = compute_best_match_numerical(
                processed_original_df,
                processed_generated_df,
                difference_columns=numerical_difference_columns,
                identification_columns=identification_columns,
            )
        computing_numerical_time = timer()

    full_time = full_timer()

    return {
        "file_path": file_path,
        "random_state": random_state,
        "traces_count": traces_count,
        "score_categorical": score_categorical,
        "score_numerical": score_numerical,
        "loading_time": loading_time,
        "training_time": training_time,
        "generation_time": generation_time,
        "computing_categorical_score_time": computing_categorical_score_time,
        "computing_numerical_time": computing_numerical_time,
        "full_time": full_time,
    }


if __name__ == "__main__":

    # Per-input configuration

    # other/simple.xes

    # file_path = maxes.notebooks.utils.get_data_path("other/simple.xes")
    # identification_columns = ["concept:name", "lifecycle:transition"]
    # categorical_difference_columns = [
    #     "call centre",
    #     "location",
    #     "outcome",
    #     "org:resource",
    # ]
    # numerical_difference_columns = ["time:timestamp"]
    # export_path = (
    #     "/vt/md/maxes/maxes/output/experiments/score/simple.csv"
    # )
    # n_experiments = 100
    # traces_count = 100
    # n_processes = None

    # photo_copier

    # file_path = maxes.data.load_files.get_path__photo_copier()
    # identification_columns = ["concept:name", "lifecycle:transition"]
    # categorical_difference_columns = ["org:resource"]
    # numerical_difference_columns = ["time:timestamp"]
    # export_path = (
    #     "/vt/md/maxes/maxes/output/experiments/score/photo_copier.csv"
    # )
    # n_experiments = 100
    # traces_count = 10
    # n_processes = None

    # bpic2020

    # file_path = maxes.data.load_files.get_path__bpic2020__request_for_payment()
    # identification_columns = ["concept:name"]
    # categorical_difference_columns = ["org:resource", "id", "org:role"]
    # numerical_difference_columns = ["time:timestamp"]
    # export_path = (
    #     "/vt/md/maxes/maxes/output/experiments/score/bpic2020.csv"
    # )
    # n_experiments = 100
    # traces_count = 100
    # n_processes = 2

    # activitylog_uci_detailed_labour

    # file_path = (
    #     maxes.data.load_files.get_path__daily_living_activities__activitylog_uci_detailed_labour()
    # )
    # identification_columns = ["concept:name", "lifecycle:transition"]
    # categorical_difference_columns = ["Column_4"]
    # numerical_difference_columns = ["time:timestamp"]
    # export_path = "/vt/md/maxes/maxes/output/experiments/score/activitylog_uci_detailed_labour.csv"
    # n_experiments = 100
    # traces_count = None
    # n_processes = None

    # ccc19

    # file_path = maxes.data.load_files.get_path__ccc19__data()
    # identification_columns = ["concept:name", "lifecycle:transition"]
    # categorical_difference_columns = [
    #     "EVENTID",
    #     "ACTIVITY",
    #     "STAGE",
    #     "VIDEOSTART",
    #     "VIDEOEND",
    # ]
    # numerical_difference_columns = ["time:timestamp"]
    # export_path = "/vt/md/maxes/maxes/output/experiments/score/ccc19.csv"
    # n_experiments = 100
    # traces_count = None
    # n_processes = None

    # env_permit_application_process

    file_path = maxes.data.load_files.get_path__env_permit_application_process__data()
    identification_columns = ["concept:name", "lifecycle:transition"]
    categorical_difference_columns = ["org:group", "concept:instance", "org:resource"]
    numerical_difference_columns = ["time:timestamp"]
    export_path = "/vt/md/maxes/maxes/output/experiments/score/env_permit_application_process.csv"
    n_experiments = 100
    traces_count = None
    n_processes = None

    # Experiment

    process_pool = multiprocessing.Pool(n_processes)

    params = []
    for i in range(n_experiments):
        params.append(
            {
                "file_path": file_path,
                "random_state": i,
                "traces_count": traces_count,
                "identification_columns": identification_columns,
                "categorical_difference_columns": categorical_difference_columns,
                "numerical_difference_columns": numerical_difference_columns,
            }
        )

    results = []
    for result in tqdm.tqdm(
        process_pool.imap_unordered(experiment_process, params), total=len(params)
    ):
        results.append(result)

    pd.DataFrame(results).to_csv(export_path)
