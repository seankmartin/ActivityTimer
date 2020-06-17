# Activity Timer
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sometimes I find it hard to manage my time in the day between the different work I need to do. This is designed to help that.

## Installation

```
git clone https://github.com/seankmartin/ActivityTimer
cd ActivityTimer
python -m pip install -r requirements.txt
fbs run
```

Or produce an executable from `fbs freeze`.
A windows download is also available at https://github.com/seankmartin/ActivityTimer/releases/download/0.11/ActivityTimerSetup.exe.

## Features

- Time activities each day and provide an objective and summary.
- Produce a clean excel file for human viewing and a csv for machine use from the times recorded.
- Demonstrates the use of the fbs build system, Pyqt5 timers and file dialogs, auto-saving every 20 minutes.

## User interface

The user interface is very simple, it looks like this:

![Screenshot of sample app on Windows](screenshots/quote-app.png)

## Command line interface

The command line interface currently only supports editing timing entries as opposed to doing actual timing.
Run with the help flag to get more information.

```
python main.py -h
```

For example, to add an extra hour and a half of time to the coding category yesterday and backup before modification, run

```
python main.py -k Coding -u 90 -d 1 -b
```

## Roadmap

Things I'd like to add, ordered by likelihood of completion.

1. Custom activities. Currently, changing the name of the activities would be little effort, but customising the number would be.
2. Add a minimise button to the UI and support rescaling the UI.

## Licensing

This project is licensed under the MIT license.
