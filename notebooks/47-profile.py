import maxes.notebooks.utils

file_path = maxes.notebooks.utils.get_data_path('other/simple.xes')

import logging
logging.basicConfig(
    filename='log.txt',
    filemode="a",
    format="%(asctime)s %(message)s",
    level=logging.DEBUG)

from maxes.xes_loader2 import XesLoader
from maxes.generators.xes_generator.xes_generator3 import XesGenerator3

for i in range(1):
    log = XesLoader().load(file_path)

    xes_generator = XesGenerator3(traces_count=1000)
    xes_generator.fit(log)

    generated_log = xes_generator.generate()
    generated_log.update_df()
    print(len(generated_log.df))
