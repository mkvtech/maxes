import gzip
import logging
import urllib.request
import shutil
import os
import pathlib
import jinja2

import maxes.notebooks.utils
from maxes.data.manifest import manifest as imported_manifest
from maxes.utils import download_with_progress_bar


def get_file_path(data_key: str, file_key: str | None = None) -> str:
    data_entry = next(
        (
            data_entry
            for data_entry in imported_manifest
            if data_entry["key"] == data_key
        )
    )

    if file_key is None:
        file_key = data_entry["default_file_key"]

    file_entry = next(
        (
            file_entry
            for file_entry in data_entry["result_files"]
            if file_entry["key"] == file_key
        )
    )

    file_in_data_entry_path = file_entry["path"]
    file_in_data_directory_path = os.path.join(data_key, file_in_data_entry_path)
    full_path = maxes.notebooks.utils.get_data_path(file_in_data_directory_path)

    return full_path


def process_manifest(
    manifest=imported_manifest, show_progress_bar=False, skip_downloaded=True
):
    for manifest_item in manifest:
        process_manifest_item(
            manifest_item,
            show_progress_bar=show_progress_bar,
            skip_downloaded=skip_downloaded,
        )


def process_manifest_item(item: dict, show_progress_bar=False, skip_downloaded=True):
    item_key = item["key"]

    item_directory_path = os.path.join(maxes.notebooks.utils.get_data_path(), item_key)
    pathlib.Path(item_directory_path).mkdir(exist_ok=True)

    # Download files
    if item.get("files") is not None:
        for file_entry in item["files"]:
            download(
                file_entry,
                item_directory_path,
                show_progress_bar=show_progress_bar,
                skip_downloaded=skip_downloaded,
            )

    # Unpack downloaded files
    if item.get("process") is not None:
        for process_step in item["process"]:
            process(process_step, item_directory_path)


def download(
    file_entry, data_entry_directory_path, show_progress_bar=False, skip_downloaded=True
):
    file_download_path = os.path.join(
        data_entry_directory_path, file_entry["destination"]
    )
    url = file_entry["url"]

    if skip_downloaded and os.path.isfile(file_download_path):
        logging.info(f'skip downloading file from "{url}" to "{file_download_path}"')
        return

    logging.info(
        f'start: downloading from "{url}" to "{file_download_path}"',
        extra={"url": url, "file_download_path": file_download_path},
    )

    if show_progress_bar:
        download_with_progress_bar(url, file_download_path)
    else:
        urllib.request.urlretrieve(url, file_download_path)

    logging.info(
        f'complete: downloading from "{url}" to "{file_download_path}"',
        extra={"url": url, "file_download_path": file_download_path},
    )


def process(process_step, data_entry_directory_path):
    step = process_step["step"]

    source_path = os.path.join(data_entry_directory_path, process_step["source"])
    destination_path = os.path.join(
        data_entry_directory_path, process_step["destination"]
    )

    logging.info(
        f'start: processing "{step}" from "{source_path}" to "{destination_path}"',
        extra={
            "step": step,
            "source_path": source_path,
            "destination_path": destination_path,
        },
    )

    if step == "gzip":
        uncompress_gzip(source_path, destination_path)
    elif step == "zip":
        shutil.unpack_archive(source_path, destination_path)
    else:
        raise NotImplementedError(f"Unknown process step: {step}")

    logging.info(
        f'complete: processing "{step}" from "{source_path}" to "{destination_path}"',
        extra={
            "step": step,
            "source_path": source_path,
            "destination_path": destination_path,
        },
    )


def uncompress_gzip(source_path, destination_path):
    with gzip.open(source_path, "rb") as f_in:
        with open(destination_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


dir_path = os.path.dirname(os.path.realpath(__file__))


def generate_data_files_file():
    load_files = {}
    for data_entry in imported_manifest:
        if data_entry.get("result_files") is None:
            continue

        data_key = data_entry["key"]
        print(data_key)

        for result_file_entry in data_entry["result_files"]:
            result_file_key = result_file_entry["key"]
            full_key = f"{data_key}__{result_file_key}"
            relative_path = os.path.join(data_key, result_file_entry["path"])
            full_path = maxes.notebooks.utils.get_data_path(relative_path)
            load_files[full_key] = full_path

        if data_entry.get("default_file_key") is not None:
            result_file_entry = next(
                (
                    i
                    for i in data_entry["result_files"]
                    if i["key"] == data_entry["default_file_key"]
                )
            )
            relative_path = os.path.join(data_key, result_file_entry["path"])
            full_path = maxes.notebooks.utils.get_data_path(relative_path)
            load_files[data_key] = full_path

    # Load template
    template = None
    template_path = os.path.join(dir_path, "load_files.py.j2")
    with open(template_path, "r") as file:
        template_text = file.read()
        template = jinja2.Template(template_text, trim_blocks=True)

    # Render
    python_text = template.render(load_files=load_files)

    # Write to file
    python_file_path = os.path.join(dir_path, "load_files.py")
    with open(python_file_path, "w") as file:
        file.write(python_text)


def get_file_key(data_key, result_file_key):
    return f"{data_key}__{result_file_key}"
