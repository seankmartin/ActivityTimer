# Activity Timer

Sometimes I find it hard to manage my time in the day between the different work I need to do. This is designed to help that.

## Installation

```
git clone https://github.com/seankmartin/ActivityTimer
cd ActivityTimer
python -m pip install -r requirements.txt
fbs run
```

Or produce an executable from `fbs freeze`.
A windows download is also available at https://github.com/seankmartin/ActivityTimer/releases/download/0.1/ActivityTimerSetup.exe.

## Features

- Time activities each day and provide an objective and summary.
- Produce a clean excel file for human viewing and a csv for machine use from the times recorded.
- Demonstrates the use of the fbs build system, Pyqt5 timers and file dialogs, auto-saving every 2 minutes.

## User interface

The user interface is very simple, it looks like this:

![Screenshot of sample app on Windows](screenshots/quote-app.png)

## Roadmap

Things I'd like to add, ordered by likelihood of completion.

1. Custom activities. Currently, changing the name of the activities would be little effort, but customising the number would be.
2. Add a minimise button to the UI and support rescaling the UI.
3. Fix a bug with the top time bar not updating sometimes. This causes no problems in the backend, so it is not a priority fix. The time bar for each individual item still updates properly.

## Licensing

This project is licensed under the MIT license.
