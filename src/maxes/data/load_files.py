import typing
import pm4py

import maxes.notebooks.utils
from maxes.xes_loader2 import XesLoader, XesLog

# This file is generated automatically

def get_pathes():
    return {
        "photo_copier__event_log": "/vt/md/maxes/maxes/data/photo_copier/event-log.xes",
        "photo_copier": "/vt/md/maxes/maxes/data/photo_copier/event-log.xes",
        "synthetic_with_performance_characteristics__event_log": "/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log.xes",
        "synthetic_with_performance_characteristics__event_log_lifecycle_moves": "/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log_lifecycle_moves.xes",
        "pdc2023__pdc2023_000000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000000.xes",
        "pdc2023__pdc2023_000001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000001.xes",
        "pdc2023__pdc2023_000010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000010.xes",
        "pdc2023__pdc2023_000011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000011.xes",
        "pdc2023__pdc2023_000100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000100.xes",
        "pdc2023__pdc2023_000101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000101.xes",
        "pdc2023__pdc2023_000110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000110.xes",
        "pdc2023__pdc2023_000111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000111.xes",
        "pdc2023__pdc2023_001000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001000.xes",
        "pdc2023__pdc2023_001001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001001.xes",
        "pdc2023__pdc2023_001010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001010.xes",
        "pdc2023__pdc2023_001011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001011.xes",
        "pdc2023__pdc2023_001100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001100.xes",
        "pdc2023__pdc2023_001101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001101.xes",
        "pdc2023__pdc2023_001110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001110.xes",
        "pdc2023__pdc2023_001111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001111.xes",
        "pdc2023__pdc2023_010000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010000.xes",
        "pdc2023__pdc2023_010001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010001.xes",
        "pdc2023__pdc2023_010010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010010.xes",
        "pdc2023__pdc2023_010011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010011.xes",
        "pdc2023__pdc2023_010100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010100.xes",
        "pdc2023__pdc2023_010101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010101.xes",
        "pdc2023__pdc2023_010110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010110.xes",
        "pdc2023__pdc2023_010111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010111.xes",
        "pdc2023__pdc2023_011000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011000.xes",
        "pdc2023__pdc2023_011001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011001.xes",
        "pdc2023__pdc2023_011010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011010.xes",
        "pdc2023__pdc2023_011011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011011.xes",
        "pdc2023__pdc2023_011100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011100.xes",
        "pdc2023__pdc2023_011101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011101.xes",
        "pdc2023__pdc2023_011110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011110.xes",
        "pdc2023__pdc2023_011111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011111.xes",
        "pdc2023__pdc2023_020000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020000.xes",
        "pdc2023__pdc2023_020001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020001.xes",
        "pdc2023__pdc2023_020010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020010.xes",
        "pdc2023__pdc2023_020011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020011.xes",
        "pdc2023__pdc2023_020100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020100.xes",
        "pdc2023__pdc2023_020101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020101.xes",
        "pdc2023__pdc2023_020110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020110.xes",
        "pdc2023__pdc2023_020111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020111.xes",
        "pdc2023__pdc2023_021000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021000.xes",
        "pdc2023__pdc2023_021001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021001.xes",
        "pdc2023__pdc2023_021010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021010.xes",
        "pdc2023__pdc2023_021011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021011.xes",
        "pdc2023__pdc2023_021100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021100.xes",
        "pdc2023__pdc2023_021101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021101.xes",
        "pdc2023__pdc2023_021110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021110.xes",
        "pdc2023__pdc2023_021111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021111.xes",
        "pdc2023__pdc2023_100000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100000.xes",
        "pdc2023__pdc2023_100001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100001.xes",
        "pdc2023__pdc2023_100010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100010.xes",
        "pdc2023__pdc2023_100011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100011.xes",
        "pdc2023__pdc2023_100100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100100.xes",
        "pdc2023__pdc2023_100101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100101.xes",
        "pdc2023__pdc2023_100110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100110.xes",
        "pdc2023__pdc2023_100111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100111.xes",
        "pdc2023__pdc2023_101000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101000.xes",
        "pdc2023__pdc2023_101001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101001.xes",
        "pdc2023__pdc2023_101010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101010.xes",
        "pdc2023__pdc2023_101011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101011.xes",
        "pdc2023__pdc2023_101100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101100.xes",
        "pdc2023__pdc2023_101101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101101.xes",
        "pdc2023__pdc2023_101110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101110.xes",
        "pdc2023__pdc2023_101111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101111.xes",
        "pdc2023__pdc2023_110000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110000.xes",
        "pdc2023__pdc2023_110001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110001.xes",
        "pdc2023__pdc2023_110010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110010.xes",
        "pdc2023__pdc2023_110011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110011.xes",
        "pdc2023__pdc2023_110100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110100.xes",
        "pdc2023__pdc2023_110101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110101.xes",
        "pdc2023__pdc2023_110110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110110.xes",
        "pdc2023__pdc2023_110111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110111.xes",
        "pdc2023__pdc2023_111000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111000.xes",
        "pdc2023__pdc2023_111001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111001.xes",
        "pdc2023__pdc2023_111010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111010.xes",
        "pdc2023__pdc2023_111011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111011.xes",
        "pdc2023__pdc2023_111100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111100.xes",
        "pdc2023__pdc2023_111101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111101.xes",
        "pdc2023__pdc2023_111110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111110.xes",
        "pdc2023__pdc2023_111111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111111.xes",
        "pdc2023__pdc2023_120000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120000.xes",
        "pdc2023__pdc2023_120001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120001.xes",
        "pdc2023__pdc2023_120010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120010.xes",
        "pdc2023__pdc2023_120011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120011.xes",
        "pdc2023__pdc2023_120100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120100.xes",
        "pdc2023__pdc2023_120101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120101.xes",
        "pdc2023__pdc2023_120110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120110.xes",
        "pdc2023__pdc2023_120111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120111.xes",
        "pdc2023__pdc2023_121000": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121000.xes",
        "pdc2023__pdc2023_121001": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121001.xes",
        "pdc2023__pdc2023_121010": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121010.xes",
        "pdc2023__pdc2023_121011": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121011.xes",
        "pdc2023__pdc2023_121100": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121100.xes",
        "pdc2023__pdc2023_121101": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121101.xes",
        "pdc2023__pdc2023_121110": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121110.xes",
        "pdc2023__pdc2023_121111": "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121111.xes",
        "env_permit_application_process__data": "/vt/md/maxes/maxes/data/env_permit_application_process/event_log.xes",
        "job_shop_scheduling__log_411": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/411.xes",
        "job_shop_scheduling__log_412": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/412.xes",
        "job_shop_scheduling__log_413": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/413.xes",
        "job_shop_scheduling__log_421": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/421.xes",
        "job_shop_scheduling__log_422": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/422.xes",
        "job_shop_scheduling__log_423": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/423.xes",
        "job_shop_scheduling__log_431": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/431.xes",
        "job_shop_scheduling__log_432": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/432.xes",
        "job_shop_scheduling__log_433": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/433.xes",
        "job_shop_scheduling__log_511": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/511.xes",
        "job_shop_scheduling__log_512": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/512.xes",
        "job_shop_scheduling__log_513": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/513.xes",
        "job_shop_scheduling__log_521": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/521.xes",
        "job_shop_scheduling__log_522": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/522.xes",
        "job_shop_scheduling__log_523": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/523.xes",
        "job_shop_scheduling__log_531": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/531.xes",
        "job_shop_scheduling__log_532": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/532.xes",
        "job_shop_scheduling__log_533": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/533.xes",
        "job_shop_scheduling__log_611": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/611.xes",
        "job_shop_scheduling__log_612": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/612.xes",
        "job_shop_scheduling__log_613": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/613.xes",
        "job_shop_scheduling__log_621": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/621.xes",
        "job_shop_scheduling__log_622": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/622.xes",
        "job_shop_scheduling__log_623": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/623.xes",
        "job_shop_scheduling__log_631": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/631.xes",
        "job_shop_scheduling__log_632": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/632.xes",
        "job_shop_scheduling__log_633": "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/633.xes",
        "lawsuits_brazil__event_log": "/vt/md/maxes/maxes/data/lawsuits_brazil/TJSP-BL-event-log.csv",
        "bpic2020__request_for_payment": "/vt/md/maxes/maxes/data/bpic2020/request_for_payment.xes",
        "bpic2020__domestic_declarations": "/vt/md/maxes/maxes/data/bpic2020/domestic_declarations.xes",
        "bpic2020__international_declarations": "/vt/md/maxes/maxes/data/bpic2020/international_declarations.xes",
        "bpic2020__permit_log": "/vt/md/maxes/maxes/data/bpic2020/permit_log.xes",
        "bpic2020__prepaid_travel_cost": "/vt/md/maxes/maxes/data/bpic2020/prepaid_travel_cost.xes",
        "ccc19__data": "/vt/md/maxes/maxes/data/ccc19/data/CCC19 - Log XES.xes",
        "software_data_analytics__alarm_system": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/AlarmSystem Case Study/5ScenarioRun.xes",
        "software_data_analytics__book_store_2": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog2case.xes",
        "software_data_analytics__book_store_20": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog20Cases.xes",
        "software_data_analytics__sports_news_commentary": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/Commentary example/10traces.xes",
        "software_data_analytics__design_patterns__observer__pattern1": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/+pattern1---Observer/1TraceSimple800.xes",
        "software_data_analytics__design_patterns__state__remote_control_software": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/remote control software--state/1trace.xes",
        "software_data_analytics__design_patterns__observer__sensing_alarm_system": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/Sensing Alarm system---Observer/3cases.xes",
        "software_data_analytics__design_patterns__observer__short_message_subscribe": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/short message subscribe---observer/5cases.xes",
        "software_data_analytics__design_patterns__state__pattern1": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/state/1trace.xes",
        "software_data_analytics__design_patterns__strategy__test_software": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/testStateStrategy software-state/1trace.xes",
        "software_data_analytics__jgraphx": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JGraphx 3.5.1/CleanJGraphx1EventLog.xes",
        "software_data_analytics__jhotdraw": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JHotDraw 5.1/CleanSoftwareEventLogJhotdraw.xes",
        "software_data_analytics__junit": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Junit 3.7/JUnit3.7Transforemd1Trace.xes",
        "software_data_analytics__lexi": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/1Trace.xes",
        "software_data_analytics__lexi_transformed": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/CleanedTransformed4Runs--Lexi.xes",
        "software_data_analytics__mailing_server__observer_pattern": "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Running Example---MailingServer_ObserverPattern/3cases.xes",
        "bpic2018__event_log": "/vt/md/maxes/maxes/data/bpic2018/event_log.xes",
        "bpic2018": "/vt/md/maxes/maxes/data/bpic2018/event_log.xes",
        "daily_living_activities__activitylog_uci_detailed_labour": "/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_labour.xes",
        "daily_living_activities__activitylog_uci_detailed_weekends": "/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_weekends.xes",
        "daily_living_activities__edited_hh102_labour": "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_labour.xes",
        "daily_living_activities__edited_hh102_weekends": "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_weekends.xes",
        "daily_living_activities__edited_hh104_labour": "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_labour.xes",
        "daily_living_activities__edited_hh104_weekends": "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_weekends.xes",
        "daily_living_activities__edited_hh110_labour": "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_labour.xes",
        "daily_living_activities__edited_hh110_weekends": "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_weekends.xes",
        "apache_commons_crypto__single_trace": "/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-single-trace.xes",
        "apache_commons_crypto__splitted": "/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-splitted.xes",
        "hospital_billing__event_log": "/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes",
        "hospital_billing": "/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes",
        "junit__event_log": "/vt/md/maxes/maxes/data/junit/JUnit 4.12 Software Event Log.xes",
        "nasa__single": "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-single-trace.xes",
        "nasa__splitted": "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-splitted.xes",
        "nasa__complete_single": "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-single-trace.xes",
        "nasa__complete_splitted": "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-splitted.xes",
        "hospital__event_log": "/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz",
        "hospital": "/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz",
        "road_traffic_fine_management__event_log": "/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz",
        "road_traffic_fine_management": "/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz",
        "statechart_workbench__event_log": "/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes",
        "statechart_workbench": "/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes",
        "bpic2012__event_log": "/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes",
        "bpic2012": "/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes",
        "bpic2013__closed_problems": "/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_closed_problems.xes",
        "bpic2013__incidents": "/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_incidents.xes",
        "bpic2013__open_problems": "/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_open_problems.xes",
        "bpic2015__municipality1": "/vt/md/maxes/maxes/data/bpic2015/BPIC15_1.xes",
        "bpic2015__municipality2": "/vt/md/maxes/maxes/data/bpic2015/BPIC15_2.xes",
        "bpic2015__municipality3": "/vt/md/maxes/maxes/data/bpic2015/BPIC15_3.xes",
        "bpic2015__municipality4": "/vt/md/maxes/maxes/data/bpic2015/BPIC15_4.xes",
        "bpic2015__municipality5": "/vt/md/maxes/maxes/data/bpic2015/BPIC15_5.xes",
        "bpic2017__event_log": "/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes",
        "bpic2017": "/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes",
        }

def get_path__photo_copier__event_log() -> str: return "/vt/md/maxes/maxes/data/photo_copier/event-log.xes"
def get_path__photo_copier() -> str: return "/vt/md/maxes/maxes/data/photo_copier/event-log.xes"
def get_path__synthetic_with_performance_characteristics__event_log() -> str: return "/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log.xes"
def get_path__synthetic_with_performance_characteristics__event_log_lifecycle_moves() -> str: return "/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log_lifecycle_moves.xes"
def get_path__pdc2023__pdc2023_000000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000000.xes"
def get_path__pdc2023__pdc2023_000001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000001.xes"
def get_path__pdc2023__pdc2023_000010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000010.xes"
def get_path__pdc2023__pdc2023_000011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000011.xes"
def get_path__pdc2023__pdc2023_000100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000100.xes"
def get_path__pdc2023__pdc2023_000101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000101.xes"
def get_path__pdc2023__pdc2023_000110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000110.xes"
def get_path__pdc2023__pdc2023_000111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000111.xes"
def get_path__pdc2023__pdc2023_001000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001000.xes"
def get_path__pdc2023__pdc2023_001001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001001.xes"
def get_path__pdc2023__pdc2023_001010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001010.xes"
def get_path__pdc2023__pdc2023_001011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001011.xes"
def get_path__pdc2023__pdc2023_001100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001100.xes"
def get_path__pdc2023__pdc2023_001101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001101.xes"
def get_path__pdc2023__pdc2023_001110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001110.xes"
def get_path__pdc2023__pdc2023_001111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001111.xes"
def get_path__pdc2023__pdc2023_010000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010000.xes"
def get_path__pdc2023__pdc2023_010001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010001.xes"
def get_path__pdc2023__pdc2023_010010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010010.xes"
def get_path__pdc2023__pdc2023_010011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010011.xes"
def get_path__pdc2023__pdc2023_010100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010100.xes"
def get_path__pdc2023__pdc2023_010101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010101.xes"
def get_path__pdc2023__pdc2023_010110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010110.xes"
def get_path__pdc2023__pdc2023_010111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010111.xes"
def get_path__pdc2023__pdc2023_011000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011000.xes"
def get_path__pdc2023__pdc2023_011001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011001.xes"
def get_path__pdc2023__pdc2023_011010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011010.xes"
def get_path__pdc2023__pdc2023_011011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011011.xes"
def get_path__pdc2023__pdc2023_011100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011100.xes"
def get_path__pdc2023__pdc2023_011101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011101.xes"
def get_path__pdc2023__pdc2023_011110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011110.xes"
def get_path__pdc2023__pdc2023_011111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011111.xes"
def get_path__pdc2023__pdc2023_020000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020000.xes"
def get_path__pdc2023__pdc2023_020001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020001.xes"
def get_path__pdc2023__pdc2023_020010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020010.xes"
def get_path__pdc2023__pdc2023_020011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020011.xes"
def get_path__pdc2023__pdc2023_020100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020100.xes"
def get_path__pdc2023__pdc2023_020101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020101.xes"
def get_path__pdc2023__pdc2023_020110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020110.xes"
def get_path__pdc2023__pdc2023_020111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020111.xes"
def get_path__pdc2023__pdc2023_021000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021000.xes"
def get_path__pdc2023__pdc2023_021001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021001.xes"
def get_path__pdc2023__pdc2023_021010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021010.xes"
def get_path__pdc2023__pdc2023_021011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021011.xes"
def get_path__pdc2023__pdc2023_021100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021100.xes"
def get_path__pdc2023__pdc2023_021101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021101.xes"
def get_path__pdc2023__pdc2023_021110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021110.xes"
def get_path__pdc2023__pdc2023_021111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021111.xes"
def get_path__pdc2023__pdc2023_100000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100000.xes"
def get_path__pdc2023__pdc2023_100001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100001.xes"
def get_path__pdc2023__pdc2023_100010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100010.xes"
def get_path__pdc2023__pdc2023_100011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100011.xes"
def get_path__pdc2023__pdc2023_100100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100100.xes"
def get_path__pdc2023__pdc2023_100101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100101.xes"
def get_path__pdc2023__pdc2023_100110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100110.xes"
def get_path__pdc2023__pdc2023_100111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100111.xes"
def get_path__pdc2023__pdc2023_101000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101000.xes"
def get_path__pdc2023__pdc2023_101001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101001.xes"
def get_path__pdc2023__pdc2023_101010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101010.xes"
def get_path__pdc2023__pdc2023_101011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101011.xes"
def get_path__pdc2023__pdc2023_101100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101100.xes"
def get_path__pdc2023__pdc2023_101101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101101.xes"
def get_path__pdc2023__pdc2023_101110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101110.xes"
def get_path__pdc2023__pdc2023_101111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101111.xes"
def get_path__pdc2023__pdc2023_110000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110000.xes"
def get_path__pdc2023__pdc2023_110001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110001.xes"
def get_path__pdc2023__pdc2023_110010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110010.xes"
def get_path__pdc2023__pdc2023_110011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110011.xes"
def get_path__pdc2023__pdc2023_110100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110100.xes"
def get_path__pdc2023__pdc2023_110101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110101.xes"
def get_path__pdc2023__pdc2023_110110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110110.xes"
def get_path__pdc2023__pdc2023_110111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110111.xes"
def get_path__pdc2023__pdc2023_111000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111000.xes"
def get_path__pdc2023__pdc2023_111001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111001.xes"
def get_path__pdc2023__pdc2023_111010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111010.xes"
def get_path__pdc2023__pdc2023_111011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111011.xes"
def get_path__pdc2023__pdc2023_111100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111100.xes"
def get_path__pdc2023__pdc2023_111101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111101.xes"
def get_path__pdc2023__pdc2023_111110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111110.xes"
def get_path__pdc2023__pdc2023_111111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111111.xes"
def get_path__pdc2023__pdc2023_120000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120000.xes"
def get_path__pdc2023__pdc2023_120001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120001.xes"
def get_path__pdc2023__pdc2023_120010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120010.xes"
def get_path__pdc2023__pdc2023_120011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120011.xes"
def get_path__pdc2023__pdc2023_120100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120100.xes"
def get_path__pdc2023__pdc2023_120101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120101.xes"
def get_path__pdc2023__pdc2023_120110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120110.xes"
def get_path__pdc2023__pdc2023_120111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120111.xes"
def get_path__pdc2023__pdc2023_121000() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121000.xes"
def get_path__pdc2023__pdc2023_121001() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121001.xes"
def get_path__pdc2023__pdc2023_121010() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121010.xes"
def get_path__pdc2023__pdc2023_121011() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121011.xes"
def get_path__pdc2023__pdc2023_121100() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121100.xes"
def get_path__pdc2023__pdc2023_121101() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121101.xes"
def get_path__pdc2023__pdc2023_121110() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121110.xes"
def get_path__pdc2023__pdc2023_121111() -> str: return "/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121111.xes"
def get_path__env_permit_application_process__data() -> str: return "/vt/md/maxes/maxes/data/env_permit_application_process/event_log.xes"
def get_path__job_shop_scheduling__log_411() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/411.xes"
def get_path__job_shop_scheduling__log_412() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/412.xes"
def get_path__job_shop_scheduling__log_413() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/413.xes"
def get_path__job_shop_scheduling__log_421() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/421.xes"
def get_path__job_shop_scheduling__log_422() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/422.xes"
def get_path__job_shop_scheduling__log_423() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/423.xes"
def get_path__job_shop_scheduling__log_431() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/431.xes"
def get_path__job_shop_scheduling__log_432() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/432.xes"
def get_path__job_shop_scheduling__log_433() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/433.xes"
def get_path__job_shop_scheduling__log_511() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/511.xes"
def get_path__job_shop_scheduling__log_512() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/512.xes"
def get_path__job_shop_scheduling__log_513() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/513.xes"
def get_path__job_shop_scheduling__log_521() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/521.xes"
def get_path__job_shop_scheduling__log_522() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/522.xes"
def get_path__job_shop_scheduling__log_523() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/523.xes"
def get_path__job_shop_scheduling__log_531() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/531.xes"
def get_path__job_shop_scheduling__log_532() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/532.xes"
def get_path__job_shop_scheduling__log_533() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/533.xes"
def get_path__job_shop_scheduling__log_611() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/611.xes"
def get_path__job_shop_scheduling__log_612() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/612.xes"
def get_path__job_shop_scheduling__log_613() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/613.xes"
def get_path__job_shop_scheduling__log_621() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/621.xes"
def get_path__job_shop_scheduling__log_622() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/622.xes"
def get_path__job_shop_scheduling__log_623() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/623.xes"
def get_path__job_shop_scheduling__log_631() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/631.xes"
def get_path__job_shop_scheduling__log_632() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/632.xes"
def get_path__job_shop_scheduling__log_633() -> str: return "/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/633.xes"
def get_path__lawsuits_brazil__event_log() -> str: return "/vt/md/maxes/maxes/data/lawsuits_brazil/TJSP-BL-event-log.csv"
def get_path__bpic2020__request_for_payment() -> str: return "/vt/md/maxes/maxes/data/bpic2020/request_for_payment.xes"
def get_path__bpic2020__domestic_declarations() -> str: return "/vt/md/maxes/maxes/data/bpic2020/domestic_declarations.xes"
def get_path__bpic2020__international_declarations() -> str: return "/vt/md/maxes/maxes/data/bpic2020/international_declarations.xes"
def get_path__bpic2020__permit_log() -> str: return "/vt/md/maxes/maxes/data/bpic2020/permit_log.xes"
def get_path__bpic2020__prepaid_travel_cost() -> str: return "/vt/md/maxes/maxes/data/bpic2020/prepaid_travel_cost.xes"
def get_path__ccc19__data() -> str: return "/vt/md/maxes/maxes/data/ccc19/data/CCC19 - Log XES.xes"
def get_path__software_data_analytics__alarm_system() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/AlarmSystem Case Study/5ScenarioRun.xes"
def get_path__software_data_analytics__book_store_2() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog2case.xes"
def get_path__software_data_analytics__book_store_20() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog20Cases.xes"
def get_path__software_data_analytics__sports_news_commentary() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/Commentary example/10traces.xes"
def get_path__software_data_analytics__design_patterns__observer__pattern1() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/+pattern1---Observer/1TraceSimple800.xes"
def get_path__software_data_analytics__design_patterns__state__remote_control_software() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/remote control software--state/1trace.xes"
def get_path__software_data_analytics__design_patterns__observer__sensing_alarm_system() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/Sensing Alarm system---Observer/3cases.xes"
def get_path__software_data_analytics__design_patterns__observer__short_message_subscribe() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/short message subscribe---observer/5cases.xes"
def get_path__software_data_analytics__design_patterns__state__pattern1() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/state/1trace.xes"
def get_path__software_data_analytics__design_patterns__strategy__test_software() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/testStateStrategy software-state/1trace.xes"
def get_path__software_data_analytics__jgraphx() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JGraphx 3.5.1/CleanJGraphx1EventLog.xes"
def get_path__software_data_analytics__jhotdraw() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JHotDraw 5.1/CleanSoftwareEventLogJhotdraw.xes"
def get_path__software_data_analytics__junit() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Junit 3.7/JUnit3.7Transforemd1Trace.xes"
def get_path__software_data_analytics__lexi() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/1Trace.xes"
def get_path__software_data_analytics__lexi_transformed() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/CleanedTransformed4Runs--Lexi.xes"
def get_path__software_data_analytics__mailing_server__observer_pattern() -> str: return "/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Running Example---MailingServer_ObserverPattern/3cases.xes"
def get_path__bpic2018__event_log() -> str: return "/vt/md/maxes/maxes/data/bpic2018/event_log.xes"
def get_path__bpic2018() -> str: return "/vt/md/maxes/maxes/data/bpic2018/event_log.xes"
def get_path__daily_living_activities__activitylog_uci_detailed_labour() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_labour.xes"
def get_path__daily_living_activities__activitylog_uci_detailed_weekends() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_weekends.xes"
def get_path__daily_living_activities__edited_hh102_labour() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_labour.xes"
def get_path__daily_living_activities__edited_hh102_weekends() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_weekends.xes"
def get_path__daily_living_activities__edited_hh104_labour() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_labour.xes"
def get_path__daily_living_activities__edited_hh104_weekends() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_weekends.xes"
def get_path__daily_living_activities__edited_hh110_labour() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_labour.xes"
def get_path__daily_living_activities__edited_hh110_weekends() -> str: return "/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_weekends.xes"
def get_path__apache_commons_crypto__single_trace() -> str: return "/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-single-trace.xes"
def get_path__apache_commons_crypto__splitted() -> str: return "/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-splitted.xes"
def get_path__hospital_billing__event_log() -> str: return "/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes"
def get_path__hospital_billing() -> str: return "/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes"
def get_path__junit__event_log() -> str: return "/vt/md/maxes/maxes/data/junit/JUnit 4.12 Software Event Log.xes"
def get_path__nasa__single() -> str: return "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-single-trace.xes"
def get_path__nasa__splitted() -> str: return "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-splitted.xes"
def get_path__nasa__complete_single() -> str: return "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-single-trace.xes"
def get_path__nasa__complete_splitted() -> str: return "/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-splitted.xes"
def get_path__hospital__event_log() -> str: return "/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz"
def get_path__hospital() -> str: return "/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz"
def get_path__road_traffic_fine_management__event_log() -> str: return "/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz"
def get_path__road_traffic_fine_management() -> str: return "/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz"
def get_path__statechart_workbench__event_log() -> str: return "/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes"
def get_path__statechart_workbench() -> str: return "/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes"
def get_path__bpic2012__event_log() -> str: return "/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes"
def get_path__bpic2012() -> str: return "/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes"
def get_path__bpic2013__closed_problems() -> str: return "/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_closed_problems.xes"
def get_path__bpic2013__incidents() -> str: return "/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_incidents.xes"
def get_path__bpic2013__open_problems() -> str: return "/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_open_problems.xes"
def get_path__bpic2015__municipality1() -> str: return "/vt/md/maxes/maxes/data/bpic2015/BPIC15_1.xes"
def get_path__bpic2015__municipality2() -> str: return "/vt/md/maxes/maxes/data/bpic2015/BPIC15_2.xes"
def get_path__bpic2015__municipality3() -> str: return "/vt/md/maxes/maxes/data/bpic2015/BPIC15_3.xes"
def get_path__bpic2015__municipality4() -> str: return "/vt/md/maxes/maxes/data/bpic2015/BPIC15_4.xes"
def get_path__bpic2015__municipality5() -> str: return "/vt/md/maxes/maxes/data/bpic2015/BPIC15_5.xes"
def get_path__bpic2017__event_log() -> str: return "/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes"
def get_path__bpic2017() -> str: return "/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes"

def load_xes__photo_copier__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/photo_copier/event-log.xes")
def load_xes__photo_copier() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/photo_copier/event-log.xes")
def load_xes__synthetic_with_performance_characteristics__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log.xes")
def load_xes__synthetic_with_performance_characteristics__event_log_lifecycle_moves() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log_lifecycle_moves.xes")
def load_xes__pdc2023__pdc2023_000000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000000.xes")
def load_xes__pdc2023__pdc2023_000001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000001.xes")
def load_xes__pdc2023__pdc2023_000010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000010.xes")
def load_xes__pdc2023__pdc2023_000011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000011.xes")
def load_xes__pdc2023__pdc2023_000100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000100.xes")
def load_xes__pdc2023__pdc2023_000101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000101.xes")
def load_xes__pdc2023__pdc2023_000110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000110.xes")
def load_xes__pdc2023__pdc2023_000111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000111.xes")
def load_xes__pdc2023__pdc2023_001000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001000.xes")
def load_xes__pdc2023__pdc2023_001001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001001.xes")
def load_xes__pdc2023__pdc2023_001010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001010.xes")
def load_xes__pdc2023__pdc2023_001011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001011.xes")
def load_xes__pdc2023__pdc2023_001100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001100.xes")
def load_xes__pdc2023__pdc2023_001101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001101.xes")
def load_xes__pdc2023__pdc2023_001110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001110.xes")
def load_xes__pdc2023__pdc2023_001111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001111.xes")
def load_xes__pdc2023__pdc2023_010000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010000.xes")
def load_xes__pdc2023__pdc2023_010001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010001.xes")
def load_xes__pdc2023__pdc2023_010010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010010.xes")
def load_xes__pdc2023__pdc2023_010011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010011.xes")
def load_xes__pdc2023__pdc2023_010100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010100.xes")
def load_xes__pdc2023__pdc2023_010101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010101.xes")
def load_xes__pdc2023__pdc2023_010110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010110.xes")
def load_xes__pdc2023__pdc2023_010111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010111.xes")
def load_xes__pdc2023__pdc2023_011000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011000.xes")
def load_xes__pdc2023__pdc2023_011001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011001.xes")
def load_xes__pdc2023__pdc2023_011010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011010.xes")
def load_xes__pdc2023__pdc2023_011011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011011.xes")
def load_xes__pdc2023__pdc2023_011100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011100.xes")
def load_xes__pdc2023__pdc2023_011101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011101.xes")
def load_xes__pdc2023__pdc2023_011110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011110.xes")
def load_xes__pdc2023__pdc2023_011111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011111.xes")
def load_xes__pdc2023__pdc2023_020000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020000.xes")
def load_xes__pdc2023__pdc2023_020001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020001.xes")
def load_xes__pdc2023__pdc2023_020010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020010.xes")
def load_xes__pdc2023__pdc2023_020011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020011.xes")
def load_xes__pdc2023__pdc2023_020100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020100.xes")
def load_xes__pdc2023__pdc2023_020101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020101.xes")
def load_xes__pdc2023__pdc2023_020110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020110.xes")
def load_xes__pdc2023__pdc2023_020111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020111.xes")
def load_xes__pdc2023__pdc2023_021000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021000.xes")
def load_xes__pdc2023__pdc2023_021001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021001.xes")
def load_xes__pdc2023__pdc2023_021010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021010.xes")
def load_xes__pdc2023__pdc2023_021011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021011.xes")
def load_xes__pdc2023__pdc2023_021100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021100.xes")
def load_xes__pdc2023__pdc2023_021101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021101.xes")
def load_xes__pdc2023__pdc2023_021110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021110.xes")
def load_xes__pdc2023__pdc2023_021111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021111.xes")
def load_xes__pdc2023__pdc2023_100000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100000.xes")
def load_xes__pdc2023__pdc2023_100001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100001.xes")
def load_xes__pdc2023__pdc2023_100010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100010.xes")
def load_xes__pdc2023__pdc2023_100011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100011.xes")
def load_xes__pdc2023__pdc2023_100100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100100.xes")
def load_xes__pdc2023__pdc2023_100101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100101.xes")
def load_xes__pdc2023__pdc2023_100110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100110.xes")
def load_xes__pdc2023__pdc2023_100111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100111.xes")
def load_xes__pdc2023__pdc2023_101000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101000.xes")
def load_xes__pdc2023__pdc2023_101001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101001.xes")
def load_xes__pdc2023__pdc2023_101010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101010.xes")
def load_xes__pdc2023__pdc2023_101011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101011.xes")
def load_xes__pdc2023__pdc2023_101100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101100.xes")
def load_xes__pdc2023__pdc2023_101101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101101.xes")
def load_xes__pdc2023__pdc2023_101110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101110.xes")
def load_xes__pdc2023__pdc2023_101111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101111.xes")
def load_xes__pdc2023__pdc2023_110000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110000.xes")
def load_xes__pdc2023__pdc2023_110001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110001.xes")
def load_xes__pdc2023__pdc2023_110010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110010.xes")
def load_xes__pdc2023__pdc2023_110011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110011.xes")
def load_xes__pdc2023__pdc2023_110100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110100.xes")
def load_xes__pdc2023__pdc2023_110101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110101.xes")
def load_xes__pdc2023__pdc2023_110110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110110.xes")
def load_xes__pdc2023__pdc2023_110111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110111.xes")
def load_xes__pdc2023__pdc2023_111000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111000.xes")
def load_xes__pdc2023__pdc2023_111001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111001.xes")
def load_xes__pdc2023__pdc2023_111010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111010.xes")
def load_xes__pdc2023__pdc2023_111011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111011.xes")
def load_xes__pdc2023__pdc2023_111100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111100.xes")
def load_xes__pdc2023__pdc2023_111101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111101.xes")
def load_xes__pdc2023__pdc2023_111110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111110.xes")
def load_xes__pdc2023__pdc2023_111111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111111.xes")
def load_xes__pdc2023__pdc2023_120000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120000.xes")
def load_xes__pdc2023__pdc2023_120001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120001.xes")
def load_xes__pdc2023__pdc2023_120010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120010.xes")
def load_xes__pdc2023__pdc2023_120011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120011.xes")
def load_xes__pdc2023__pdc2023_120100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120100.xes")
def load_xes__pdc2023__pdc2023_120101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120101.xes")
def load_xes__pdc2023__pdc2023_120110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120110.xes")
def load_xes__pdc2023__pdc2023_120111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120111.xes")
def load_xes__pdc2023__pdc2023_121000() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121000.xes")
def load_xes__pdc2023__pdc2023_121001() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121001.xes")
def load_xes__pdc2023__pdc2023_121010() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121010.xes")
def load_xes__pdc2023__pdc2023_121011() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121011.xes")
def load_xes__pdc2023__pdc2023_121100() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121100.xes")
def load_xes__pdc2023__pdc2023_121101() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121101.xes")
def load_xes__pdc2023__pdc2023_121110() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121110.xes")
def load_xes__pdc2023__pdc2023_121111() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121111.xes")
def load_xes__env_permit_application_process__data() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/env_permit_application_process/event_log.xes")
def load_xes__job_shop_scheduling__log_411() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/411.xes")
def load_xes__job_shop_scheduling__log_412() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/412.xes")
def load_xes__job_shop_scheduling__log_413() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/413.xes")
def load_xes__job_shop_scheduling__log_421() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/421.xes")
def load_xes__job_shop_scheduling__log_422() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/422.xes")
def load_xes__job_shop_scheduling__log_423() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/423.xes")
def load_xes__job_shop_scheduling__log_431() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/431.xes")
def load_xes__job_shop_scheduling__log_432() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/432.xes")
def load_xes__job_shop_scheduling__log_433() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/433.xes")
def load_xes__job_shop_scheduling__log_511() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/511.xes")
def load_xes__job_shop_scheduling__log_512() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/512.xes")
def load_xes__job_shop_scheduling__log_513() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/513.xes")
def load_xes__job_shop_scheduling__log_521() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/521.xes")
def load_xes__job_shop_scheduling__log_522() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/522.xes")
def load_xes__job_shop_scheduling__log_523() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/523.xes")
def load_xes__job_shop_scheduling__log_531() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/531.xes")
def load_xes__job_shop_scheduling__log_532() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/532.xes")
def load_xes__job_shop_scheduling__log_533() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/533.xes")
def load_xes__job_shop_scheduling__log_611() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/611.xes")
def load_xes__job_shop_scheduling__log_612() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/612.xes")
def load_xes__job_shop_scheduling__log_613() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/613.xes")
def load_xes__job_shop_scheduling__log_621() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/621.xes")
def load_xes__job_shop_scheduling__log_622() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/622.xes")
def load_xes__job_shop_scheduling__log_623() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/623.xes")
def load_xes__job_shop_scheduling__log_631() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/631.xes")
def load_xes__job_shop_scheduling__log_632() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/632.xes")
def load_xes__job_shop_scheduling__log_633() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/633.xes")
def load_xes__lawsuits_brazil__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/lawsuits_brazil/TJSP-BL-event-log.csv")
def load_xes__bpic2020__request_for_payment() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2020/request_for_payment.xes")
def load_xes__bpic2020__domestic_declarations() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2020/domestic_declarations.xes")
def load_xes__bpic2020__international_declarations() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2020/international_declarations.xes")
def load_xes__bpic2020__permit_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2020/permit_log.xes")
def load_xes__bpic2020__prepaid_travel_cost() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2020/prepaid_travel_cost.xes")
def load_xes__ccc19__data() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/ccc19/data/CCC19 - Log XES.xes")
def load_xes__software_data_analytics__alarm_system() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/AlarmSystem Case Study/5ScenarioRun.xes")
def load_xes__software_data_analytics__book_store_2() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog2case.xes")
def load_xes__software_data_analytics__book_store_20() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog20Cases.xes")
def load_xes__software_data_analytics__sports_news_commentary() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/Commentary example/10traces.xes")
def load_xes__software_data_analytics__design_patterns__observer__pattern1() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/+pattern1---Observer/1TraceSimple800.xes")
def load_xes__software_data_analytics__design_patterns__state__remote_control_software() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/remote control software--state/1trace.xes")
def load_xes__software_data_analytics__design_patterns__observer__sensing_alarm_system() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/Sensing Alarm system---Observer/3cases.xes")
def load_xes__software_data_analytics__design_patterns__observer__short_message_subscribe() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/short message subscribe---observer/5cases.xes")
def load_xes__software_data_analytics__design_patterns__state__pattern1() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/state/1trace.xes")
def load_xes__software_data_analytics__design_patterns__strategy__test_software() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/testStateStrategy software-state/1trace.xes")
def load_xes__software_data_analytics__jgraphx() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JGraphx 3.5.1/CleanJGraphx1EventLog.xes")
def load_xes__software_data_analytics__jhotdraw() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JHotDraw 5.1/CleanSoftwareEventLogJhotdraw.xes")
def load_xes__software_data_analytics__junit() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Junit 3.7/JUnit3.7Transforemd1Trace.xes")
def load_xes__software_data_analytics__lexi() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/1Trace.xes")
def load_xes__software_data_analytics__lexi_transformed() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/CleanedTransformed4Runs--Lexi.xes")
def load_xes__software_data_analytics__mailing_server__observer_pattern() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Running Example---MailingServer_ObserverPattern/3cases.xes")
def load_xes__bpic2018__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2018/event_log.xes")
def load_xes__bpic2018() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2018/event_log.xes")
def load_xes__daily_living_activities__activitylog_uci_detailed_labour() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_labour.xes")
def load_xes__daily_living_activities__activitylog_uci_detailed_weekends() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_weekends.xes")
def load_xes__daily_living_activities__edited_hh102_labour() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_labour.xes")
def load_xes__daily_living_activities__edited_hh102_weekends() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_weekends.xes")
def load_xes__daily_living_activities__edited_hh104_labour() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_labour.xes")
def load_xes__daily_living_activities__edited_hh104_weekends() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_weekends.xes")
def load_xes__daily_living_activities__edited_hh110_labour() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_labour.xes")
def load_xes__daily_living_activities__edited_hh110_weekends() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_weekends.xes")
def load_xes__apache_commons_crypto__single_trace() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-single-trace.xes")
def load_xes__apache_commons_crypto__splitted() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-splitted.xes")
def load_xes__hospital_billing__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes")
def load_xes__hospital_billing() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes")
def load_xes__junit__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/junit/JUnit 4.12 Software Event Log.xes")
def load_xes__nasa__single() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-single-trace.xes")
def load_xes__nasa__splitted() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-splitted.xes")
def load_xes__nasa__complete_single() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-single-trace.xes")
def load_xes__nasa__complete_splitted() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-splitted.xes")
def load_xes__hospital__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz")
def load_xes__hospital() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz")
def load_xes__road_traffic_fine_management__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz")
def load_xes__road_traffic_fine_management() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz")
def load_xes__statechart_workbench__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes")
def load_xes__statechart_workbench() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes")
def load_xes__bpic2012__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes")
def load_xes__bpic2012() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes")
def load_xes__bpic2013__closed_problems() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_closed_problems.xes")
def load_xes__bpic2013__incidents() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_incidents.xes")
def load_xes__bpic2013__open_problems() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_open_problems.xes")
def load_xes__bpic2015__municipality1() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2015/BPIC15_1.xes")
def load_xes__bpic2015__municipality2() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2015/BPIC15_2.xes")
def load_xes__bpic2015__municipality3() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2015/BPIC15_3.xes")
def load_xes__bpic2015__municipality4() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2015/BPIC15_4.xes")
def load_xes__bpic2015__municipality5() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2015/BPIC15_5.xes")
def load_xes__bpic2017__event_log() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes")
def load_xes__bpic2017() -> str: return XesLoader().load("/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes")

def load_csv__photo_copier__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/photo_copier/event-log.xes")
def load_csv__photo_copier() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/photo_copier/event-log.xes")
def load_csv__synthetic_with_performance_characteristics__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log.xes")
def load_csv__synthetic_with_performance_characteristics__event_log_lifecycle_moves() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/synthetic_with_performance_characteristics/event_log_lifecycle_moves.xes")
def load_csv__pdc2023__pdc2023_000000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000000.xes")
def load_csv__pdc2023__pdc2023_000001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000001.xes")
def load_csv__pdc2023__pdc2023_000010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000010.xes")
def load_csv__pdc2023__pdc2023_000011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000011.xes")
def load_csv__pdc2023__pdc2023_000100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000100.xes")
def load_csv__pdc2023__pdc2023_000101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000101.xes")
def load_csv__pdc2023__pdc2023_000110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000110.xes")
def load_csv__pdc2023__pdc2023_000111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_000111.xes")
def load_csv__pdc2023__pdc2023_001000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001000.xes")
def load_csv__pdc2023__pdc2023_001001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001001.xes")
def load_csv__pdc2023__pdc2023_001010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001010.xes")
def load_csv__pdc2023__pdc2023_001011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001011.xes")
def load_csv__pdc2023__pdc2023_001100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001100.xes")
def load_csv__pdc2023__pdc2023_001101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001101.xes")
def load_csv__pdc2023__pdc2023_001110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001110.xes")
def load_csv__pdc2023__pdc2023_001111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_001111.xes")
def load_csv__pdc2023__pdc2023_010000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010000.xes")
def load_csv__pdc2023__pdc2023_010001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010001.xes")
def load_csv__pdc2023__pdc2023_010010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010010.xes")
def load_csv__pdc2023__pdc2023_010011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010011.xes")
def load_csv__pdc2023__pdc2023_010100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010100.xes")
def load_csv__pdc2023__pdc2023_010101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010101.xes")
def load_csv__pdc2023__pdc2023_010110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010110.xes")
def load_csv__pdc2023__pdc2023_010111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_010111.xes")
def load_csv__pdc2023__pdc2023_011000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011000.xes")
def load_csv__pdc2023__pdc2023_011001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011001.xes")
def load_csv__pdc2023__pdc2023_011010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011010.xes")
def load_csv__pdc2023__pdc2023_011011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011011.xes")
def load_csv__pdc2023__pdc2023_011100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011100.xes")
def load_csv__pdc2023__pdc2023_011101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011101.xes")
def load_csv__pdc2023__pdc2023_011110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011110.xes")
def load_csv__pdc2023__pdc2023_011111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_011111.xes")
def load_csv__pdc2023__pdc2023_020000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020000.xes")
def load_csv__pdc2023__pdc2023_020001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020001.xes")
def load_csv__pdc2023__pdc2023_020010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020010.xes")
def load_csv__pdc2023__pdc2023_020011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020011.xes")
def load_csv__pdc2023__pdc2023_020100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020100.xes")
def load_csv__pdc2023__pdc2023_020101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020101.xes")
def load_csv__pdc2023__pdc2023_020110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020110.xes")
def load_csv__pdc2023__pdc2023_020111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_020111.xes")
def load_csv__pdc2023__pdc2023_021000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021000.xes")
def load_csv__pdc2023__pdc2023_021001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021001.xes")
def load_csv__pdc2023__pdc2023_021010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021010.xes")
def load_csv__pdc2023__pdc2023_021011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021011.xes")
def load_csv__pdc2023__pdc2023_021100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021100.xes")
def load_csv__pdc2023__pdc2023_021101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021101.xes")
def load_csv__pdc2023__pdc2023_021110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021110.xes")
def load_csv__pdc2023__pdc2023_021111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_021111.xes")
def load_csv__pdc2023__pdc2023_100000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100000.xes")
def load_csv__pdc2023__pdc2023_100001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100001.xes")
def load_csv__pdc2023__pdc2023_100010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100010.xes")
def load_csv__pdc2023__pdc2023_100011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100011.xes")
def load_csv__pdc2023__pdc2023_100100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100100.xes")
def load_csv__pdc2023__pdc2023_100101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100101.xes")
def load_csv__pdc2023__pdc2023_100110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100110.xes")
def load_csv__pdc2023__pdc2023_100111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_100111.xes")
def load_csv__pdc2023__pdc2023_101000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101000.xes")
def load_csv__pdc2023__pdc2023_101001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101001.xes")
def load_csv__pdc2023__pdc2023_101010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101010.xes")
def load_csv__pdc2023__pdc2023_101011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101011.xes")
def load_csv__pdc2023__pdc2023_101100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101100.xes")
def load_csv__pdc2023__pdc2023_101101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101101.xes")
def load_csv__pdc2023__pdc2023_101110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101110.xes")
def load_csv__pdc2023__pdc2023_101111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_101111.xes")
def load_csv__pdc2023__pdc2023_110000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110000.xes")
def load_csv__pdc2023__pdc2023_110001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110001.xes")
def load_csv__pdc2023__pdc2023_110010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110010.xes")
def load_csv__pdc2023__pdc2023_110011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110011.xes")
def load_csv__pdc2023__pdc2023_110100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110100.xes")
def load_csv__pdc2023__pdc2023_110101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110101.xes")
def load_csv__pdc2023__pdc2023_110110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110110.xes")
def load_csv__pdc2023__pdc2023_110111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_110111.xes")
def load_csv__pdc2023__pdc2023_111000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111000.xes")
def load_csv__pdc2023__pdc2023_111001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111001.xes")
def load_csv__pdc2023__pdc2023_111010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111010.xes")
def load_csv__pdc2023__pdc2023_111011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111011.xes")
def load_csv__pdc2023__pdc2023_111100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111100.xes")
def load_csv__pdc2023__pdc2023_111101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111101.xes")
def load_csv__pdc2023__pdc2023_111110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111110.xes")
def load_csv__pdc2023__pdc2023_111111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_111111.xes")
def load_csv__pdc2023__pdc2023_120000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120000.xes")
def load_csv__pdc2023__pdc2023_120001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120001.xes")
def load_csv__pdc2023__pdc2023_120010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120010.xes")
def load_csv__pdc2023__pdc2023_120011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120011.xes")
def load_csv__pdc2023__pdc2023_120100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120100.xes")
def load_csv__pdc2023__pdc2023_120101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120101.xes")
def load_csv__pdc2023__pdc2023_120110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120110.xes")
def load_csv__pdc2023__pdc2023_120111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_120111.xes")
def load_csv__pdc2023__pdc2023_121000() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121000.xes")
def load_csv__pdc2023__pdc2023_121001() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121001.xes")
def load_csv__pdc2023__pdc2023_121010() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121010.xes")
def load_csv__pdc2023__pdc2023_121011() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121011.xes")
def load_csv__pdc2023__pdc2023_121100() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121100.xes")
def load_csv__pdc2023__pdc2023_121101() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121101.xes")
def load_csv__pdc2023__pdc2023_121110() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121110.xes")
def load_csv__pdc2023__pdc2023_121111() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/pdc2023/base_logs/pdc2023_121111.xes")
def load_csv__env_permit_application_process__data() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/env_permit_application_process/event_log.xes")
def load_csv__job_shop_scheduling__log_411() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/411.xes")
def load_csv__job_shop_scheduling__log_412() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/412.xes")
def load_csv__job_shop_scheduling__log_413() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/413.xes")
def load_csv__job_shop_scheduling__log_421() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/421.xes")
def load_csv__job_shop_scheduling__log_422() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/422.xes")
def load_csv__job_shop_scheduling__log_423() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/423.xes")
def load_csv__job_shop_scheduling__log_431() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/431.xes")
def load_csv__job_shop_scheduling__log_432() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/432.xes")
def load_csv__job_shop_scheduling__log_433() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/433.xes")
def load_csv__job_shop_scheduling__log_511() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/511.xes")
def load_csv__job_shop_scheduling__log_512() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/512.xes")
def load_csv__job_shop_scheduling__log_513() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/513.xes")
def load_csv__job_shop_scheduling__log_521() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/521.xes")
def load_csv__job_shop_scheduling__log_522() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/522.xes")
def load_csv__job_shop_scheduling__log_523() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/523.xes")
def load_csv__job_shop_scheduling__log_531() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/531.xes")
def load_csv__job_shop_scheduling__log_532() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/532.xes")
def load_csv__job_shop_scheduling__log_533() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/533.xes")
def load_csv__job_shop_scheduling__log_611() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/611.xes")
def load_csv__job_shop_scheduling__log_612() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/612.xes")
def load_csv__job_shop_scheduling__log_613() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/613.xes")
def load_csv__job_shop_scheduling__log_621() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/621.xes")
def load_csv__job_shop_scheduling__log_622() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/622.xes")
def load_csv__job_shop_scheduling__log_623() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/623.xes")
def load_csv__job_shop_scheduling__log_631() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/631.xes")
def load_csv__job_shop_scheduling__log_632() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/632.xes")
def load_csv__job_shop_scheduling__log_633() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/job_shop_scheduling/filtered_files/FilteredFiles/633.xes")
def load_csv__lawsuits_brazil__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/lawsuits_brazil/TJSP-BL-event-log.csv")
def load_csv__bpic2020__request_for_payment() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2020/request_for_payment.xes")
def load_csv__bpic2020__domestic_declarations() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2020/domestic_declarations.xes")
def load_csv__bpic2020__international_declarations() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2020/international_declarations.xes")
def load_csv__bpic2020__permit_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2020/permit_log.xes")
def load_csv__bpic2020__prepaid_travel_cost() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2020/prepaid_travel_cost.xes")
def load_csv__ccc19__data() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/ccc19/data/CCC19 - Log XES.xes")
def load_csv__software_data_analytics__alarm_system() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/AlarmSystem Case Study/5ScenarioRun.xes")
def load_csv__software_data_analytics__book_store_2() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog2case.xes")
def load_csv__software_data_analytics__book_store_20() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog20Cases.xes")
def load_csv__software_data_analytics__sports_news_commentary() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/3 Case studies/Commentary example/10traces.xes")
def load_csv__software_data_analytics__design_patterns__observer__pattern1() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/+pattern1---Observer/1TraceSimple800.xes")
def load_csv__software_data_analytics__design_patterns__state__remote_control_software() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/remote control software--state/1trace.xes")
def load_csv__software_data_analytics__design_patterns__observer__sensing_alarm_system() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/Sensing Alarm system---Observer/3cases.xes")
def load_csv__software_data_analytics__design_patterns__observer__short_message_subscribe() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/short message subscribe---observer/5cases.xes")
def load_csv__software_data_analytics__design_patterns__state__pattern1() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/state/1trace.xes")
def load_csv__software_data_analytics__design_patterns__strategy__test_software() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Design pattern detection/source+data/testStateStrategy software-state/1trace.xes")
def load_csv__software_data_analytics__jgraphx() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JGraphx 3.5.1/CleanJGraphx1EventLog.xes")
def load_csv__software_data_analytics__jhotdraw() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/JHotDraw 5.1/CleanSoftwareEventLogJhotdraw.xes")
def load_csv__software_data_analytics__junit() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Junit 3.7/JUnit3.7Transforemd1Trace.xes")
def load_csv__software_data_analytics__lexi() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/1Trace.xes")
def load_csv__software_data_analytics__lexi_transformed() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Lexi 0.1.1/CleanedTransformed4Runs--Lexi.xes")
def load_csv__software_data_analytics__mailing_server__observer_pattern() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/software_data_analytics/data/PhD Thesis Execution Data/Running Example---MailingServer_ObserverPattern/3cases.xes")
def load_csv__bpic2018__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2018/event_log.xes")
def load_csv__bpic2018() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2018/event_log.xes")
def load_csv__daily_living_activities__activitylog_uci_detailed_labour() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_labour.xes")
def load_csv__daily_living_activities__activitylog_uci_detailed_weekends() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/activitylog_uci_detailed_weekends.xes")
def load_csv__daily_living_activities__edited_hh102_labour() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_labour.xes")
def load_csv__daily_living_activities__edited_hh102_weekends() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh102_weekends.xes")
def load_csv__daily_living_activities__edited_hh104_labour() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_labour.xes")
def load_csv__daily_living_activities__edited_hh104_weekends() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh104_weekends.xes")
def load_csv__daily_living_activities__edited_hh110_labour() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_labour.xes")
def load_csv__daily_living_activities__edited_hh110_weekends() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/daily_living_activities/data/edited_hh110_weekends.xes")
def load_csv__apache_commons_crypto__single_trace() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-single-trace.xes")
def load_csv__apache_commons_crypto__splitted() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/apache_commons_crypto/data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-splitted.xes")
def load_csv__hospital_billing__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes")
def load_csv__hospital_billing() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/hospital_billing/eveng_log.xes")
def load_csv__junit__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/junit/JUnit 4.12 Software Event Log.xes")
def load_csv__nasa__single() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-single-trace.xes")
def load_csv__nasa__splitted() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-1-10-splitted.xes")
def load_csv__nasa__complete_single() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-single-trace.xes")
def load_csv__nasa__complete_splitted() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/nasa/data/nasa-cev-complete-splitted.xes")
def load_csv__hospital__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz")
def load_csv__hospital() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/hospital/Hospital_log.xes.gz")
def load_csv__road_traffic_fine_management__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz")
def load_csv__road_traffic_fine_management() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/road_traffic_fine_management/Road_Traffic_Fine_Management_Process.xes.gz")
def load_csv__statechart_workbench__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes")
def load_csv__statechart_workbench() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/statechart_workbench/data/Statechart Workbench and Alignments Software Event Log.xes")
def load_csv__bpic2012__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes")
def load_csv__bpic2012() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2012/BPI_Challenge_2012.xes")
def load_csv__bpic2013__closed_problems() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_closed_problems.xes")
def load_csv__bpic2013__incidents() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_incidents.xes")
def load_csv__bpic2013__open_problems() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2013/BPI_Challenge_2013_open_problems.xes")
def load_csv__bpic2015__municipality1() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2015/BPIC15_1.xes")
def load_csv__bpic2015__municipality2() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2015/BPIC15_2.xes")
def load_csv__bpic2015__municipality3() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2015/BPIC15_3.xes")
def load_csv__bpic2015__municipality4() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2015/BPIC15_4.xes")
def load_csv__bpic2015__municipality5() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2015/BPIC15_5.xes")
def load_csv__bpic2017__event_log() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes")
def load_csv__bpic2017() -> str: return pm4py.read_csv("/vt/md/maxes/maxes/data/bpic2017/BPI Challenge 2017.xes")
