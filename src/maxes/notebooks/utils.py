import datetime
import logging
import importlib
import jinja2
import json
import os
import yaml
import xml.etree.ElementTree as ET

import maxes.serialization.serialize
from maxes.xes_loader2 import XesLoader
from maxes.xes_log import XesLog

dir_path = os.path.dirname(os.path.realpath(__file__))


def _get_config_file_path():
    # TODO: Read from args or env

    # Currently, "config.local.yml" is expected to be two directories up from this file
    this_file_directory_path = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(
        this_file_directory_path, os.pardir, os.pardir, os.pardir, "config.local.yml"
    )
    config_file_path_normalized = os.path.abspath(config_file_path)
    return config_file_path_normalized


config_file_path = _get_config_file_path()
config = {}
with open(config_file_path, "r") as file:
    config = yaml.safe_load(file)

# print("Config:")
# print(config)


def init_notebook(init_logging=True, init_data_files_file=True):
    print(f"Loading config from: {config_file_path}")

    with open(config_file_path, "r") as file:
        global config
        config = yaml.safe_load(file)

    print("Config:")
    print(config)

    if init_logging:
        setup_notebook_logging()

    if init_data_files_file:
        generate_data_files_file()


def setup_notebook_logging():
    """When called, creates notebook log file and re-configures global logging module"""

    # TODO: use __vsc_ipynb_file__ to get notebook file name

    importlib.reload(logging)
    filename_timestamp_part = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    absolute_file_path = get_project_path(
        f"output/logs/notebooks/{filename_timestamp_part}.log"
    )
    logging.basicConfig(
        filename=absolute_file_path,
        filemode="a",
        format="%(asctime)s %(message)s",
        level=logging.DEBUG,
    )
    logging.info("START")


def get_project_path(path=""):
    project_path = config["project_directory_path"]
    return _optionally_join(project_path, path)


def get_data_path(path=""):
    data_path = config["data_directory_path"]
    return _optionally_join(data_path, path)


def get_output_path(path=""):
    output_path = config["output_directory_path"]
    return _optionally_join(output_path, path)


def _optionally_join(first_path, second_path):
    if second_path == None or second_path == "":
        return first_path

    return os.path.join(first_path, second_path)


def generate_data_files_file():
    # Load load_files.json
    load_files = {}
    load_files_file_path = os.path.join(dir_path, "load_files.json")
    with open(load_files_file_path, "r") as file:
        load_files = json.load(file)

    # Load template
    template = None
    template_path = os.path.join(dir_path, "load_file.py.j2")
    with open(template_path, "r") as file:
        template_text = file.read()
        template = jinja2.Template(template_text, trim_blocks=True)

    # Render
    python_text = template.render(load_files=load_files)

    # Write to file
    python_file_path = os.path.join(dir_path, "load_files.py")
    with open(python_file_path, "w") as file:
        file.write(python_text)


def write_xes_to_file(log: XesLog, skeleton_log: XesLog, destination_file_path: str):
    logging.info("Serializing")
    log_ET = maxes.serialization.serialize.Serializer().serialize(
        log, xml_log_skeleton=skeleton_log.loader.xml_log_skeleton
    )

    logging.info("Formatting XML")
    ET.indent(log_ET)

    logging.info("Writing XML")
    ET.register_namespace("", "http://www.xes-standard.org")
    with open(destination_file_path, "w") as file:
        log_ET.write(file, encoding="unicode")

    logging.info("Done")


def load_xes(file_path: str) -> XesLog:
    loader = XesLoader()

    logging.info("Loading")
    log = loader.load(file_path)

    if len(loader.errors):
        raise RuntimeError("Errors while loading XES")

    return log


def generate_xes_for_file(source_file_path: str, destination_file_path: str):
    loader = XesLoader()

    logging.info("Loading")
    log = loader.load(source_file_path)

    if len(loader.errors):
        raise RuntimeError("Errors while loading XES")

    generate_xes_for_log(log, destination_file_path)
