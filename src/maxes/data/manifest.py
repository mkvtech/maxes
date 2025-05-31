manifest = [
    {
        "key": "photo_copier",
        "title": "Artificial Digital Photo Copier Event Log",
        "page_url": "https://data.4tu.nl/datasets/c8ae67a9-13de-445b-8086-2655afc0c1db",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/c8ae67a9-13de-445b-8086-2655afc0c1db/87aa13ed-6ebc-46b5-8b1e-b13fd0d23f69",
                "destination": "event-log.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "event-log.xes.gz",
                "destination": "event-log.xes",
            }
        ],
        "result_files": [{"key": "event_log", "path": "event-log.xes"}],
    },
    {
        "key": "synthetic_with_performance_characteristics",
        "title": "Synthetic event log with specific process performance characteristics",
        "page_url": "",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/670bf51b-cb96-4c80-9c20-caff31b2f568/3fe0c66f-2d18-4f48-81ab-6efba707973f",
                "destination": "event_log.xes",
            },
            {
                "key": "event_log_lifecycle_moves",
                "url": "https://data.4tu.nl/file/670bf51b-cb96-4c80-9c20-caff31b2f568/bbcb2ba0-4e61-4120-a0ff-d72f8a7a9cd3",
                "destination": "event_log_lifecycle_moves.xes",
            },
        ],
        "result_files": [
            {"key": "event_log", "path": "event_log.xes"},
            {
                "key": "event_log_lifecycle_moves",
                "path": "event_log_lifecycle_moves.xes",
            },
        ],
    },
    {
        "key": "pdc2023",
        "title": "Process Discovery Contest 2023",
        "page_url": "https://data.4tu.nl/datasets/afd6f608-469e-48f9-977d-875b45840d39/1",
        "files": [
            {
                "key": "base_logs",
                "url": "https://data.4tu.nl/file/afd6f608-469e-48f9-977d-875b45840d39/17cf3540-27b9-4525-a5e8-626de4faa627",
                "destination": "base_logs.zip",
            },
            {
                "key": "ground_truth_logs",
                "url": "https://data.4tu.nl/file/afd6f608-469e-48f9-977d-875b45840d39/0e3065bd-5e8d-48f7-8548-b490d3ef80bb",
                "destination": "ground_truth_logs.zip",
            },
            {
                "key": "models",
                "url": "https://data.4tu.nl/file/afd6f608-469e-48f9-977d-875b45840d39/e8eaeb15-b503-443c-8666-43f3c5261eb2",
                "destination": "models.zip",
            },
            {
                "key": "test_logs",
                "url": "https://data.4tu.nl/file/afd6f608-469e-48f9-977d-875b45840d39/de946a9a-727e-4eed-b0e5-0ca2393d54aa",
                "destination": "test_logs.zip",
            },
            {
                "key": "training_logs",
                "url": "https://data.4tu.nl/file/afd6f608-469e-48f9-977d-875b45840d39/acbc2e6d-6182-4a3a-84b5-282a28022228",
                "destination": "training_logs.zip",
            },
        ],
        "process": [
            {"step": "zip", "source": "base_logs.zip", "destination": "base_logs"},
            {
                "step": "zip",
                "source": "ground_truth_logs.zip",
                "destination": "ground_truth_logs",
            },
            {"step": "zip", "source": "models.zip", "destination": "models"},
            {"step": "zip", "source": "test_logs.zip", "destination": "test_logs"},
            {
                "step": "zip",
                "source": "training_logs.zip",
                "destination": "training_logs",
            },
        ],
        "result_files": [
            {"key": "pdc2023_000000", "path": "base_logs/pdc2023_000000.xes"},
            {"key": "pdc2023_000001", "path": "base_logs/pdc2023_000001.xes"},
            {"key": "pdc2023_000010", "path": "base_logs/pdc2023_000010.xes"},
            {"key": "pdc2023_000011", "path": "base_logs/pdc2023_000011.xes"},
            {"key": "pdc2023_000100", "path": "base_logs/pdc2023_000100.xes"},
            {"key": "pdc2023_000101", "path": "base_logs/pdc2023_000101.xes"},
            {"key": "pdc2023_000110", "path": "base_logs/pdc2023_000110.xes"},
            {"key": "pdc2023_000111", "path": "base_logs/pdc2023_000111.xes"},
            {"key": "pdc2023_001000", "path": "base_logs/pdc2023_001000.xes"},
            {"key": "pdc2023_001001", "path": "base_logs/pdc2023_001001.xes"},
            {"key": "pdc2023_001010", "path": "base_logs/pdc2023_001010.xes"},
            {"key": "pdc2023_001011", "path": "base_logs/pdc2023_001011.xes"},
            {"key": "pdc2023_001100", "path": "base_logs/pdc2023_001100.xes"},
            {"key": "pdc2023_001101", "path": "base_logs/pdc2023_001101.xes"},
            {"key": "pdc2023_001110", "path": "base_logs/pdc2023_001110.xes"},
            {"key": "pdc2023_001111", "path": "base_logs/pdc2023_001111.xes"},
            {"key": "pdc2023_010000", "path": "base_logs/pdc2023_010000.xes"},
            {"key": "pdc2023_010001", "path": "base_logs/pdc2023_010001.xes"},
            {"key": "pdc2023_010010", "path": "base_logs/pdc2023_010010.xes"},
            {"key": "pdc2023_010011", "path": "base_logs/pdc2023_010011.xes"},
            {"key": "pdc2023_010100", "path": "base_logs/pdc2023_010100.xes"},
            {"key": "pdc2023_010101", "path": "base_logs/pdc2023_010101.xes"},
            {"key": "pdc2023_010110", "path": "base_logs/pdc2023_010110.xes"},
            {"key": "pdc2023_010111", "path": "base_logs/pdc2023_010111.xes"},
            {"key": "pdc2023_011000", "path": "base_logs/pdc2023_011000.xes"},
            {"key": "pdc2023_011001", "path": "base_logs/pdc2023_011001.xes"},
            {"key": "pdc2023_011010", "path": "base_logs/pdc2023_011010.xes"},
            {"key": "pdc2023_011011", "path": "base_logs/pdc2023_011011.xes"},
            {"key": "pdc2023_011100", "path": "base_logs/pdc2023_011100.xes"},
            {"key": "pdc2023_011101", "path": "base_logs/pdc2023_011101.xes"},
            {"key": "pdc2023_011110", "path": "base_logs/pdc2023_011110.xes"},
            {"key": "pdc2023_011111", "path": "base_logs/pdc2023_011111.xes"},
            {"key": "pdc2023_020000", "path": "base_logs/pdc2023_020000.xes"},
            {"key": "pdc2023_020001", "path": "base_logs/pdc2023_020001.xes"},
            {"key": "pdc2023_020010", "path": "base_logs/pdc2023_020010.xes"},
            {"key": "pdc2023_020011", "path": "base_logs/pdc2023_020011.xes"},
            {"key": "pdc2023_020100", "path": "base_logs/pdc2023_020100.xes"},
            {"key": "pdc2023_020101", "path": "base_logs/pdc2023_020101.xes"},
            {"key": "pdc2023_020110", "path": "base_logs/pdc2023_020110.xes"},
            {"key": "pdc2023_020111", "path": "base_logs/pdc2023_020111.xes"},
            {"key": "pdc2023_021000", "path": "base_logs/pdc2023_021000.xes"},
            {"key": "pdc2023_021001", "path": "base_logs/pdc2023_021001.xes"},
            {"key": "pdc2023_021010", "path": "base_logs/pdc2023_021010.xes"},
            {"key": "pdc2023_021011", "path": "base_logs/pdc2023_021011.xes"},
            {"key": "pdc2023_021100", "path": "base_logs/pdc2023_021100.xes"},
            {"key": "pdc2023_021101", "path": "base_logs/pdc2023_021101.xes"},
            {"key": "pdc2023_021110", "path": "base_logs/pdc2023_021110.xes"},
            {"key": "pdc2023_021111", "path": "base_logs/pdc2023_021111.xes"},
            {"key": "pdc2023_100000", "path": "base_logs/pdc2023_100000.xes"},
            {"key": "pdc2023_100001", "path": "base_logs/pdc2023_100001.xes"},
            {"key": "pdc2023_100010", "path": "base_logs/pdc2023_100010.xes"},
            {"key": "pdc2023_100011", "path": "base_logs/pdc2023_100011.xes"},
            {"key": "pdc2023_100100", "path": "base_logs/pdc2023_100100.xes"},
            {"key": "pdc2023_100101", "path": "base_logs/pdc2023_100101.xes"},
            {"key": "pdc2023_100110", "path": "base_logs/pdc2023_100110.xes"},
            {"key": "pdc2023_100111", "path": "base_logs/pdc2023_100111.xes"},
            {"key": "pdc2023_101000", "path": "base_logs/pdc2023_101000.xes"},
            {"key": "pdc2023_101001", "path": "base_logs/pdc2023_101001.xes"},
            {"key": "pdc2023_101010", "path": "base_logs/pdc2023_101010.xes"},
            {"key": "pdc2023_101011", "path": "base_logs/pdc2023_101011.xes"},
            {"key": "pdc2023_101100", "path": "base_logs/pdc2023_101100.xes"},
            {"key": "pdc2023_101101", "path": "base_logs/pdc2023_101101.xes"},
            {"key": "pdc2023_101110", "path": "base_logs/pdc2023_101110.xes"},
            {"key": "pdc2023_101111", "path": "base_logs/pdc2023_101111.xes"},
            {"key": "pdc2023_110000", "path": "base_logs/pdc2023_110000.xes"},
            {"key": "pdc2023_110001", "path": "base_logs/pdc2023_110001.xes"},
            {"key": "pdc2023_110010", "path": "base_logs/pdc2023_110010.xes"},
            {"key": "pdc2023_110011", "path": "base_logs/pdc2023_110011.xes"},
            {"key": "pdc2023_110100", "path": "base_logs/pdc2023_110100.xes"},
            {"key": "pdc2023_110101", "path": "base_logs/pdc2023_110101.xes"},
            {"key": "pdc2023_110110", "path": "base_logs/pdc2023_110110.xes"},
            {"key": "pdc2023_110111", "path": "base_logs/pdc2023_110111.xes"},
            {"key": "pdc2023_111000", "path": "base_logs/pdc2023_111000.xes"},
            {"key": "pdc2023_111001", "path": "base_logs/pdc2023_111001.xes"},
            {"key": "pdc2023_111010", "path": "base_logs/pdc2023_111010.xes"},
            {"key": "pdc2023_111011", "path": "base_logs/pdc2023_111011.xes"},
            {"key": "pdc2023_111100", "path": "base_logs/pdc2023_111100.xes"},
            {"key": "pdc2023_111101", "path": "base_logs/pdc2023_111101.xes"},
            {"key": "pdc2023_111110", "path": "base_logs/pdc2023_111110.xes"},
            {"key": "pdc2023_111111", "path": "base_logs/pdc2023_111111.xes"},
            {"key": "pdc2023_120000", "path": "base_logs/pdc2023_120000.xes"},
            {"key": "pdc2023_120001", "path": "base_logs/pdc2023_120001.xes"},
            {"key": "pdc2023_120010", "path": "base_logs/pdc2023_120010.xes"},
            {"key": "pdc2023_120011", "path": "base_logs/pdc2023_120011.xes"},
            {"key": "pdc2023_120100", "path": "base_logs/pdc2023_120100.xes"},
            {"key": "pdc2023_120101", "path": "base_logs/pdc2023_120101.xes"},
            {"key": "pdc2023_120110", "path": "base_logs/pdc2023_120110.xes"},
            {"key": "pdc2023_120111", "path": "base_logs/pdc2023_120111.xes"},
            {"key": "pdc2023_121000", "path": "base_logs/pdc2023_121000.xes"},
            {"key": "pdc2023_121001", "path": "base_logs/pdc2023_121001.xes"},
            {"key": "pdc2023_121010", "path": "base_logs/pdc2023_121010.xes"},
            {"key": "pdc2023_121011", "path": "base_logs/pdc2023_121011.xes"},
            {"key": "pdc2023_121100", "path": "base_logs/pdc2023_121100.xes"},
            {"key": "pdc2023_121101", "path": "base_logs/pdc2023_121101.xes"},
            {"key": "pdc2023_121110", "path": "base_logs/pdc2023_121110.xes"},
            {"key": "pdc2023_121111", "path": "base_logs/pdc2023_121111.xes"},
        ],
    },
    {
        "key": "env_permit_application_process",
        "title": "Receipt phase of an environmental permit application process (WABO), CoSeLoG project",
        "page_url": "https://data.4tu.nl/datasets/2db2e3c1-9499-4699-9098-1a28c15a5913/2",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/2db2e3c1-9499-4699-9098-1a28c15a5913/21758246-61e7-4019-bf7d-fb6a9b38df14",
                "destination": "event_log.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "event_log.xes.gz",
                "destination": "event_log.xes",
            }
        ],
        "result_files": [{"key": "data", "path": "event_log.xes"}],
    },
    {
        "key": "job_shop_scheduling",
        "title": "An agent-based process mining architecture for emergent behavior analysis",
        "page_url": "https://data.4tu.nl/datasets/29fee175-d665-4412-b3c8-d7e553ea1b73/2",
        "files": [
            {
                "key": "filtered_files",
                "url": "https://data.4tu.nl/file/29fee175-d665-4412-b3c8-d7e553ea1b73/c97251ff-7da3-4936-8933-72fb223b5473",
                "destination": "filtered_files.zip",
            }
        ],
        "process": [
            {
                "step": "zip",
                "source": "filtered_files.zip",
                "destination": "filtered_files",
            }
        ],
        "result_files": [
            {"key": "log_411", "path": "filtered_files/FilteredFiles/411.xes"},
            {"key": "log_412", "path": "filtered_files/FilteredFiles/412.xes"},
            {"key": "log_413", "path": "filtered_files/FilteredFiles/413.xes"},
            {"key": "log_421", "path": "filtered_files/FilteredFiles/421.xes"},
            {"key": "log_422", "path": "filtered_files/FilteredFiles/422.xes"},
            {"key": "log_423", "path": "filtered_files/FilteredFiles/423.xes"},
            {"key": "log_431", "path": "filtered_files/FilteredFiles/431.xes"},
            {"key": "log_432", "path": "filtered_files/FilteredFiles/432.xes"},
            {"key": "log_433", "path": "filtered_files/FilteredFiles/433.xes"},
            {"key": "log_511", "path": "filtered_files/FilteredFiles/511.xes"},
            {"key": "log_512", "path": "filtered_files/FilteredFiles/512.xes"},
            {"key": "log_513", "path": "filtered_files/FilteredFiles/513.xes"},
            {"key": "log_521", "path": "filtered_files/FilteredFiles/521.xes"},
            {"key": "log_522", "path": "filtered_files/FilteredFiles/522.xes"},
            {"key": "log_523", "path": "filtered_files/FilteredFiles/523.xes"},
            {"key": "log_531", "path": "filtered_files/FilteredFiles/531.xes"},
            {"key": "log_532", "path": "filtered_files/FilteredFiles/532.xes"},
            {"key": "log_533", "path": "filtered_files/FilteredFiles/533.xes"},
            {"key": "log_611", "path": "filtered_files/FilteredFiles/611.xes"},
            {"key": "log_612", "path": "filtered_files/FilteredFiles/612.xes"},
            {"key": "log_613", "path": "filtered_files/FilteredFiles/613.xes"},
            {"key": "log_621", "path": "filtered_files/FilteredFiles/621.xes"},
            {"key": "log_622", "path": "filtered_files/FilteredFiles/622.xes"},
            {"key": "log_623", "path": "filtered_files/FilteredFiles/623.xes"},
            {"key": "log_631", "path": "filtered_files/FilteredFiles/631.xes"},
            {"key": "log_632", "path": "filtered_files/FilteredFiles/632.xes"},
            {"key": "log_633", "path": "filtered_files/FilteredFiles/633.xes"},
        ],
    },
    {
        "key": "lawsuits_brazil",
        "title": "",
        "description": "Event log containing business 4,795 lawsuits distributed between January 1, 2018 and July 21, 2020 from the Court of Justice of the State of Sao Paulo, Brazil.",
        "page_url": "https://data.4tu.nl/datasets/d5076a17-6d14-4c23-9ff9-23c43659cb83/1",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/d5076a17-6d14-4c23-9ff9-23c43659cb83/38c90eeb-7a1d-4789-a4fe-308410ea7302",
                "destination": "TJSP-BL-event-log.csv",
            }
        ],
        "result_files": [{"key": "event_log", "path": "TJSP-BL-event-log.csv"}],
    },
    {
        "key": "bpic2020",
        "title": "BPI Challenge 2020",
        "page_url": "https://data.4tu.nl/collections/6bcb71ec-6e2e-4837-a899-624367f1c36b",
        "files": [
            {
                "key": "request_for_payment",
                "url": "https://data.4tu.nl/file/a6f651a7-5ce0-4bc6-8be1-a7747effa1cc/7b1f2e56-e4a8-43ee-9a09-6e64f45a1a98",
                "destination": "request_for_payment.xes.gz",
            },
            {
                "key": "domestic_declarations",
                "url": "https://data.4tu.nl/file/6a0a26d2-82d0-4018-b1cd-89afb0e8627f/6eeb0328-f991-48c7-95f2-35033504036e",
                "destination": "domestic_declarations.xes.gz",
            },
            {
                "key": "international_declarations",
                "url": "https://data.4tu.nl/file/91fd1fa8-4df4-4b1a-9a3f-0116c412378f/d45ee7dc-952c-4885-b950-4579a91ef426",
                "destination": "international_declarations.xes.gz",
            },
            {
                "key": "permit_log",
                "url": "https://data.4tu.nl/file/db35afac-2133-40f3-a565-2dc77a9329a3/12b48cc1-18a8-4089-ae01-7078fc5e8f90",
                "destination": "permit_log.xes.gz",
            },
            {
                "key": "prepaid_travel_cost",
                "url": "https://data.4tu.nl/file/fb84cf2d-166f-4de2-87be-62ee317077e5/612068f6-14d0-4a82-b118-1b51db52e73a",
                "destination": "prepaid_travel_cost.xes.gz",
            },
        ],
        "process": [
            {
                "step": "gzip",
                "source": "request_for_payment.xes.gz",
                "destination": "request_for_payment.xes",
            },
            {
                "step": "gzip",
                "source": "domestic_declarations.xes.gz",
                "destination": "domestic_declarations.xes",
            },
            {
                "step": "gzip",
                "source": "international_declarations.xes.gz",
                "destination": "international_declarations.xes",
            },
            {
                "step": "gzip",
                "source": "permit_log.xes.gz",
                "destination": "permit_log.xes",
            },
            {
                "step": "gzip",
                "source": "prepaid_travel_cost.xes.gz",
                "destination": "prepaid_travel_cost.xes",
            },
        ],
        "result_files": [
            {"key": "request_for_payment", "path": "request_for_payment.xes"},
            {"key": "domestic_declarations", "path": "domestic_declarations.xes"},
            {
                "key": "international_declarations",
                "path": "international_declarations.xes",
            },
            {"key": "permit_log", "path": "permit_log.xes"},
            {"key": "prepaid_travel_cost", "path": "prepaid_travel_cost.xes"},
        ],
    },
    {
        "key": "ccc19",
        "title": "Conformance Checking Challenge 2019 (CCC19)",
        "page_url": "https://data.4tu.nl/datasets/cb2975c2-96c5-4616-97a4-f0f88abef14e/1",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/cb2975c2-96c5-4616-97a4-f0f88abef14e/7866ef2e-a8ad-461b-aaa5-4533c1856a32",
                "destination": "data.zip",
            },
        ],
        "process": [
            {"step": "zip", "source": "data.zip", "destination": "data"},
        ],
        "result_files": [
            {"key": "data", "path": "data/CCC19 - Log XES.xes"},
        ],
    },
    {
        "key": "software_data_analytics",
        "title": 'Experimental data for "Software Data Analytics: Architectural Model Discovery and Design Pattern Detection"',
        "page_url": "https://data.4tu.nl/datasets/a1d2ad46-7e37-476b-9c5f-082db6ee112a/1",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/a1d2ad46-7e37-476b-9c5f-082db6ee112a/58e54a9d-9962-47c9-bbb1-8f492e0a1417",
                "destination": "data.zip",
            },
        ],
        "process": [
            {"step": "zip", "source": "data.zip", "destination": "data"},
            {
                "step": "gzip",
                "source": "data/PhD Thesis Execution Data/JGraphx 3.5.1/CleanJGraphx1EventLog.xes.gz",
                "destination": "data/PhD Thesis Execution Data/JGraphx 3.5.1/CleanJGraphx1EventLog.xes",
            },
            {
                "step": "gzip",
                "source": "data/PhD Thesis Execution Data/JHotDraw 5.1/CleanSoftwareEventLogJhotdraw.xes.gz",
                "destination": "data/PhD Thesis Execution Data/JHotDraw 5.1/CleanSoftwareEventLogJhotdraw.xes",
            },
            {
                "step": "gzip",
                "source": "data/PhD Thesis Execution Data/Junit 3.7/JUnit3.7Transforemd1Trace.xes.gz",
                "destination": "data/PhD Thesis Execution Data/Junit 3.7/JUnit3.7Transforemd1Trace.xes",
            },
            {
                "step": "gzip",
                "source": "data/PhD Thesis Execution Data/Lexi 0.1.1/1Trace.xes.gz",
                "destination": "data/PhD Thesis Execution Data/Lexi 0.1.1/1Trace.xes",
            },
            {
                "step": "gzip",
                "source": "data/PhD Thesis Execution Data/Lexi 0.1.1/CleanedTransformed4Runs--Lexi.xes.gz",
                "destination": "data/PhD Thesis Execution Data/Lexi 0.1.1/CleanedTransformed4Runs--Lexi.xes",
            },
        ],
        "result_files": [
            # 3 case studies
            {
                "key": "alarm_system",
                "path": "data/PhD Thesis Execution Data/3 Case studies/AlarmSystem Case Study/5ScenarioRun.xes",
            },
            #
            {
                "key": "book_store_2",
                "path": "data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog2case.xes",
            },
            {
                "key": "book_store_20",
                "path": "data/PhD Thesis Execution Data/3 Case studies/bookstore case [source+data+component config]/bookstorelog20Cases.xes",
            },
            #
            {
                "key": "sports_news_commentary",
                "path": "data/PhD Thesis Execution Data/3 Case studies/Commentary example/10traces.xes",
            },
            # Design pattern detection
            {
                "key": "design_patterns__observer__pattern1",
                "path": "data/PhD Thesis Execution Data/Design pattern detection/source+data/+pattern1---Observer/1TraceSimple800.xes",
            },
            {
                "key": "design_patterns__state__remote_control_software",
                "path": "data/PhD Thesis Execution Data/Design pattern detection/source+data/remote control software--state/1trace.xes",
            },
            {
                "key": "design_patterns__observer__sensing_alarm_system",
                "path": "data/PhD Thesis Execution Data/Design pattern detection/source+data/Sensing Alarm system---Observer/3cases.xes",
            },
            {
                "key": "design_patterns__observer__short_message_subscribe",
                "path": "data/PhD Thesis Execution Data/Design pattern detection/source+data/short message subscribe---observer/5cases.xes",
            },
            {
                "key": "design_patterns__state__pattern1",
                "path": "data/PhD Thesis Execution Data/Design pattern detection/source+data/state/1trace.xes",
            },
            {
                "key": "design_patterns__strategy__test_software",
                "path": "data/PhD Thesis Execution Data/Design pattern detection/source+data/testStateStrategy software-state/1trace.xes",
            },
            #
            {
                "key": "jgraphx",
                "path": "data/PhD Thesis Execution Data/JGraphx 3.5.1/CleanJGraphx1EventLog.xes",
            },
            {
                "key": "jhotdraw",
                "path": "data/PhD Thesis Execution Data/JHotDraw 5.1/CleanSoftwareEventLogJhotdraw.xes",
            },
            {
                "key": "junit",
                "path": "data/PhD Thesis Execution Data/Junit 3.7/JUnit3.7Transforemd1Trace.xes",
            },
            {
                "key": "lexi",
                "path": "data/PhD Thesis Execution Data/Lexi 0.1.1/1Trace.xes",
            },
            {
                "key": "lexi_transformed",
                "path": "data/PhD Thesis Execution Data/Lexi 0.1.1/CleanedTransformed4Runs--Lexi.xes",
            },
            #
            {
                "key": "mailing_server__observer_pattern",
                "path": "data/PhD Thesis Execution Data/Running Example---MailingServer_ObserverPattern/3cases.xes",
            },
        ],
    },
    {
        "key": "bpic2018",
        "title": "BPI Challenge 2018",
        "page_url": "https://data.4tu.nl/datasets/443451fd-d38a-4464-88b4-0fc641552632/1",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/443451fd-d38a-4464-88b4-0fc641552632/cd4fd2b8-6c95-47ae-aad9-dc1a085db364",
                "destination": "event_log.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "event_log.xes.gz",
                "destination": "event_log.xes",
            },
        ],
        "result_files": [
            {"key": "event_log", "path": "event_log.xes"},
        ],
    },
    {
        "key": "daily_living_activities",
        "title": "Activities of daily living of several individuals",
        "page_url": "https://data.4tu.nl/datasets/14ecd91b-494a-4fdb-ad19-7ba824cdb049/1",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/14ecd91b-494a-4fdb-ad19-7ba824cdb049/ed03561c-e22a-4c87-ab6e-4b6ddaddf0f6",
                "destination": "data.zip",
            }
        ],
        "process": [
            {"step": "zip", "source": "data.zip", "destination": "data"},
            {
                "step": "gzip",
                "source": "data/activitylog_uci_detailed_labour.xes.gz",
                "destination": "data/activitylog_uci_detailed_labour.xes",
            },
            {
                "step": "gzip",
                "source": "data/activitylog_uci_detailed_weekends.xes.gz",
                "destination": "data/activitylog_uci_detailed_weekends.xes",
            },
            {
                "step": "gzip",
                "source": "data/edited_hh102_labour.xes.gz",
                "destination": "data/edited_hh102_labour.xes",
            },
            {
                "step": "gzip",
                "source": "data/edited_hh102_weekends.xes.gz",
                "destination": "data/edited_hh102_weekends.xes",
            },
            {
                "step": "gzip",
                "source": "data/edited_hh104_labour.xes.gz",
                "destination": "data/edited_hh104_labour.xes",
            },
            {
                "step": "gzip",
                "source": "data/edited_hh104_weekends.xes.gz",
                "destination": "data/edited_hh104_weekends.xes",
            },
            {
                "step": "gzip",
                "source": "data/edited_hh110_labour.xes.gz",
                "destination": "data/edited_hh110_labour.xes",
            },
            {
                "step": "gzip",
                "source": "data/edited_hh110_weekends.xes.gz",
                "destination": "data/edited_hh110_weekends.xes",
            },
        ],
        "result_files": [
            {
                "key": "activitylog_uci_detailed_labour",
                "path": "data/activitylog_uci_detailed_labour.xes",
            },
            {
                "key": "activitylog_uci_detailed_weekends",
                "path": "data/activitylog_uci_detailed_weekends.xes",
            },
            {"key": "edited_hh102_labour", "path": "data/edited_hh102_labour.xes"},
            {"key": "edited_hh102_weekends", "path": "data/edited_hh102_weekends.xes"},
            {"key": "edited_hh104_labour", "path": "data/edited_hh104_labour.xes"},
            {"key": "edited_hh104_weekends", "path": "data/edited_hh104_weekends.xes"},
            {"key": "edited_hh110_labour", "path": "data/edited_hh110_labour.xes"},
            {"key": "edited_hh110_weekends", "path": "data/edited_hh110_weekends.xes"},
        ],
    },
    {
        "key": "apache_commons_crypto",
        "title": "Apache Commons Crypto 1.0.0 - Stream CbcNopad Unit Test Software Event Log",
        "page_url": "https://data.4tu.nl/articles/_/12713972/1",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/8a67441a-f961-4f5e-97f6-46115f7e8679/2bf8155f-1cf3-4000-8398-b5f3f892174d",
                "destination": "data.zip",
            }
        ],
        "process": [
            {"step": "zip", "source": "data.zip", "destination": "data"},
            {
                "step": "gzip",
                "source": "data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-single-trace.xes.gz",
                "destination": "data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-single-trace.xes",
            },
            {
                "step": "gzip",
                "source": "data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-splitted.xes.gz",
                "destination": "data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-splitted.xes",
            },
        ],
        "result_files": [
            {
                "key": "single_trace",
                "path": "data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-single-trace.xes",
            },
            {
                "key": "splitted",
                "path": "data/ApacheCommons-Crypto-1.0.0-StreamCbcNopad-splitted.xes",
            },
        ],
    },
    {
        "key": "hospital_billing",
        "title": "Hospital Billing - Event Log",
        "page_url": "https://data.4tu.nl/articles/_/12705113/1",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/6af6d5f0-f44c-49be-aac8-8eaa5fe4f6fd/28b83e72-375e-4da4-8459-a8506e898edf",
                "destination": "event_log.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "event_log.xes.gz",
                "destination": "eveng_log.xes",
            }
        ],
        "result_files": [{"key": "event_log", "path": "eveng_log.xes"}],
    },
    {
        "key": "junit",
        "title": "JUnit 4.12 Software Event Log",
        "page_url": "https://data.4tu.nl/articles/_/12715829/1",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/1af91e91-78cf-4f16-a237-a7bc65efaec2/4e0d99f5-f04a-49e2-84e3-4491203e9c89",
                "destination": "JUnit 4.12 Software Event Log.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "JUnit 4.12 Software Event Log.xes.gz",
                "destination": "JUnit 4.12 Software Event Log.xes",
            }
        ],
        "result_files": [
            {"key": "event_log", "path": "JUnit 4.12 Software Event Log.xes"}
        ],
    },
    {
        "key": "nasa",
        "title": "NASA Crew Exploration Vehicle (CEV) Software Event Log",
        "page_url": "https://data.4tu.nl/articles/_/12696995/1",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/95edb3e5-8f28-49d7-bffa-72f46c625ca9/1ed0e56c-6af4-474e-8f99-cb406cfca080",
                "destination": "data.zip",
            }
        ],
        "process": [
            {"step": "zip", "source": "data.zip", "destination": "data"},
            {
                "step": "gzip",
                "source": "data/nasa-cev-1-10-single-trace.xes.gz",
                "destination": "data/nasa-cev-1-10-single-trace.xes",
            },
            {
                "step": "gzip",
                "source": "data/nasa-cev-1-10-splitted.xes.gz",
                "destination": "data/nasa-cev-1-10-splitted.xes",
            },
            {
                "step": "gzip",
                "source": "data/nasa-cev-complete-single-trace.xes.gz",
                "destination": "data/nasa-cev-complete-single-trace.xes",
            },
            {
                "step": "gzip",
                "source": "data/nasa-cev-complete-splitted.xes.gz",
                "destination": "data/nasa-cev-complete-splitted.xes",
            },
        ],
        "result_files": [
            {
                "key": "single",
                "path": "data/nasa-cev-1-10-single-trace.xes",
            },
            {
                "key": "splitted",
                "path": "data/nasa-cev-1-10-splitted.xes",
            },
            {
                "key": "complete_single",
                "path": "data/nasa-cev-complete-single-trace.xes",
            },
            {
                "key": "complete_splitted",
                "path": "data/nasa-cev-complete-splitted.xes",
            },
        ],
    },
    {
        "key": "hospital",
        "title": "Real-life event logs - Hospital log",
        "page_url": "https://data.4tu.nl/articles/_/12716513/1",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/5ea5bb88-feaa-4e6f-a743-6460a755e05b/6f9640f9-0f1e-44d2-9495-ef9d1bd82218",
                "destination": "Hospital_log.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "Hospital_log.xes.gz",
                "destination": "Hospital_log.xes",
            }
        ],
        "result_files": [{"key": "event_log", "path": "Hospital_log.xes.gz"}],
    },
    {
        "key": "road_traffic_fine_management",
        "title": "Road Traffic Fine Management Process",
        "page_url": "https://data.4tu.nl/articles/_/12683249/1",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/806acd1a-2bf2-4e39-be21-69b8cad10909/b234b06c-4d4f-4055-9f14-6218e3906d82",
                "destination": "Road_Traffic_Fine_Management_Process.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "Road_Traffic_Fine_Management_Process.xes.gz",
                "destination": "Road_Traffic_Fine_Management_Process.xes",
            }
        ],
        "result_files": [
            {"key": "event_log", "path": "Road_Traffic_Fine_Management_Process.xes.gz"}
        ],
    },
    {
        "key": "statechart_workbench",
        "title": "Statechart Workbench and Alignments Software Event Log",
        "page_url": "https://data.4tu.nl/articles/_/12705863/1",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/3ec3daab-c7a4-4e4f-bdc4-02c23d488677/b964dc3a-981c-4259-a82a-3430a5787e32",
                "destination": "data.zip",
            }
        ],
        "process": [
            {"step": "zip", "source": "data.zip", "destination": "data"},
            {
                "step": "gzip",
                "source": "data/Statechart Workbench and Alignments Software Event Log.xes.gz",
                "destination": "data/Statechart Workbench and Alignments Software Event Log.xes",
            },
        ],
        "result_files": [
            {
                "key": "event_log",
                "path": "data/Statechart Workbench and Alignments Software Event Log.xes",
            }
        ],
    },
    {
        "key": "bpic2012",
        "title": "BPI Challenge 2012",
        "page_url": "https://data.4tu.nl/articles/_/12689204/1",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "data",
                "url": "https://data.4tu.nl/file/533f66a4-8911-4ac7-8612-1235d65d1f37/3276db7f-8bee-4f2b-88ee-92dbffb5a893",
                "destination": "BPI_Challenge_2012.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "BPI_Challenge_2012.xes.gz",
                "destination": "BPI_Challenge_2012.xes",
            },
        ],
        "result_files": [
            {
                "key": "event_log",
                "path": "BPI_Challenge_2012.xes",
            }
        ],
    },
    {
        "key": "bpic2013",
        "title": "BPI Challenge 2013",
        "page_url": "https://data.4tu.nl/collections/_/5065448/1",
        "files": [
            {
                "key": "bpic2013_closed_problems",
                "url": "https://data.4tu.nl/file/1987a2a6-9f5b-4b14-8d26-ab7056b17929/8b99119d-9525-452e-bc8f-236ac76fa9c9",
                "destination": "BPI_Challenge_2013_closed_problems.xes.gz",
            },
            {
                "key": "bpic2013_incidents",
                "url": "https://data.4tu.nl/file/0fc5c579-e544-4fab-9143-fab1f5192432/aa51ffbb-25fd-4b5a-b0b8-9aba659b7e8c",
                "destination": "BPI_Challenge_2013_incidents.xes.gz",
            },
            {
                "key": "bpic2013_open_problems",
                "url": "https://data.4tu.nl/file/7aafbf5b-97ae-48ba-bd0a-4d973a68cd35/0647ad1a-fa73-4376-bdb4-1b253576c3a1",
                "destination": "BPI_Challenge_2013_open_problems.xes.gz",
            },
        ],
        "process": [
            {
                "step": "gzip",
                "source": "BPI_Challenge_2013_closed_problems.xes.gz",
                "destination": "BPI_Challenge_2013_closed_problems.xes",
            },
            {
                "step": "gzip",
                "source": "BPI_Challenge_2013_incidents.xes.gz",
                "destination": "BPI_Challenge_2013_incidents.xes",
            },
            {
                "step": "gzip",
                "source": "BPI_Challenge_2013_open_problems.xes.gz",
                "destination": "BPI_Challenge_2013_open_problems.xes",
            },
        ],
        "result_files": [
            {
                "key": "closed_problems",
                "path": "BPI_Challenge_2013_closed_problems.xes",
            },
            {
                "key": "incidents",
                "path": "BPI_Challenge_2013_incidents.xes",
            },
            {
                "key": "open_problems",
                "path": "BPI_Challenge_2013_open_problems.xes",
            },
        ],
    },
    {
        "key": "bpic2015",
        "title": "BPI Challenge 2015",
        "page_url": "https://data.4tu.nl/collections/_/5065424/1",
        "files": [
            {
                "key": "municipality1",
                "url": "https://data.4tu.nl/file/6f35269e-4ce7-4bc4-9abb-b3cea04cad00/2c8d5827-3e08-471d-98e2-6ffdec92f958",
                "destination": "BPIC15_1.xes",
            },
            {
                "key": "municipality2",
                "url": "https://data.4tu.nl/file/372d0cad-3fb1-4627-8ea9-51a09923d331/d653a8ec-4cd1-4029-8b61-6cfde4f4a666",
                "destination": "BPIC15_2.xes",
            },
            {
                "key": "municipality3",
                "url": "https://data.4tu.nl/file/d6741425-5f62-4a59-92c5-08bae64b4611/21b574ab-02ba-4dfb-badc-bb46ce0edc44",
                "destination": "BPIC15_3.xes",
            },
            {
                "key": "municipality4",
                "url": "https://data.4tu.nl/file/34216d8a-f054-46d4-bf03-d9352f90967e/68923819-b085-43be-abe2-e084a0f1381f",
                "destination": "BPIC15_4.xes",
            },
            {
                "key": "municipality5",
                "url": "https://data.4tu.nl/file/32b70553-0765-4808-b155-aa5319802c8a/d39e1365-e4b8-4cb8-83d3-0b01cbf6f8c2",
                "destination": "BPIC15_5.xes",
            },
        ],
        "result_files": [
            {
                "key": "municipality1",
                "path": "BPIC15_1.xes",
            },
            {
                "key": "municipality2",
                "path": "BPIC15_2.xes",
            },
            {
                "key": "municipality3",
                "path": "BPIC15_3.xes",
            },
            {
                "key": "municipality4",
                "path": "BPIC15_4.xes",
            },
            {
                "key": "municipality5",
                "path": "BPIC15_5.xes",
            },
        ],
    },
    {
        "key": "bpic2017",
        "title": "BPI Challenge 2017",
        "page_url": "https://data.4tu.nl/articles/_/12696884/1",
        "default_file_key": "event_log",
        "files": [
            {
                "key": "event_log",
                "url": "https://data.4tu.nl/file/34c3f44b-3101-4ea9-8281-e38905c68b8d/f3aec4f7-d52c-4217-82f4-57d719a8298c",
                "destination": "BPI Challenge 2017.xes.gz",
            }
        ],
        "process": [
            {
                "step": "gzip",
                "source": "BPI Challenge 2017.xes.gz",
                "destination": "BPI Challenge 2017.xes",
            },
        ],
        "result_files": [
            {
                "key": "event_log",
                "path": "BPI Challenge 2017.xes",
            }
        ],
    },
    # {
    #     "key": "template",
    #     "title": "",
    #     "page_url": "",
    #     "files": [
    #         {
    #             "key": "",
    #             "url": "",
    #             "destination": ""
    #         },
    #     ],
    #     "process": [
    #         {
    #             "step": "zip",
    #             "source": "event_log.zip",
    #             "destination": "event_log"
    #         },
    #     ],
    #     "result_files": [
    #         {
    #             "key": "event_log",
    #             "path": "event_log.xes"
    #         },
    #     ]
    # },
]
