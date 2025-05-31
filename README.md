# About

Experiments with XES files. University project.

# Installation

Project implemented with Python 3.12. Please see `./requirements.txt` for required packages.

1. Install dependencies

```sh
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install -e .
mkdir -r output/logs/notebooks
```

This also installs package in current folder (from this: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder)

2. Put input files in `data` directory

This repository does not contain sample XES files that were used in experiments, as some of them are too large (>1gb).

There is code to download sample XES files from https://data.4tu.nl. See `src/maxes/data/manifest.py` for details. These files were used in experiments.

3. Update `config.local.yml`

Please specifiy project root directory. Here you can also override data directory, in case it is not in its default position.

# Usage

To run GUI:

```sh
python ./src/maxes/app/main.py
```

All other experiments are in `notebooks` directory, for example `notebooks/56_presentation.ipynb`
