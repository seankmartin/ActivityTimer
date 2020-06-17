import os
import sys
import datetime

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer
import pkg_resources.py2_warn
import openpyxl

from code_time import CodeTime, strfdelta


class DesignerUI(object):
    def __init__(self, design_name):
        self.appctxt = ApplicationContext()
        design_path = self.appctxt.get_resource(design_name)
        Form, Window = uic.loadUiType(design_path)
        self.window = Window()
        self.ui = Form()
        self.ui.setupUi(self.window)
        self.file_dialog = QFileDialog()

    def start(self):
        self.window.show()
        self.exit_code = self.appctxt.app.exec_()

    def getWidgets(self):
        return self.appctxt.app.allWidgets()

    def getWidgetNames(self):
        return [w.objectName() for w in self.getWidgets()]


class CodeTimeUI(DesignerUI):
    def __init__(self, design_name):
        super().__init__(design_name)
        self.init_vars()
        self.linkNames()
        self.setup()
        self.update_times()
        self.autosave_timer.start(self.save_frequency)

    def init_vars(self):
        self.selected_file = None
        self.should_update = False
        self.update_frequency_secs = 1.00
        # Convert to msec for qt timer
        self.update_frequency = int(self.update_frequency_secs * 1000)
        save_freq_mins = 20
        self.save_frequency = int(1000 * 60 * save_freq_mins)

    def linkNames(self):
        self.file_select_button = self.ui.OpenButton
        self.save_button = self.ui.SaveButton
        self.quit_button = self.ui.QuitButton
        self.stop_button = self.ui.StopButton

        self.code_button = self.ui.CodeButton
        self.contact_button = self.ui.ContactButton
        self.misc_button = self.ui.MiscButton
        self.read_button = self.ui.ReadButton
        self.write_button = self.ui.WriteButton

        self.code_text = self.ui.CodeTimeLine
        self.contact_text = self.ui.ContactTimeLine
        self.misc_text = self.ui.MiscTimeLine
        self.read_text = self.ui.ReadingTimeLine
        self.write_text = self.ui.WritingTimeLine

        self.time_dict = {
            "Gaming": self.code_text,
            "Piano": self.read_text,
            "Sleep": self.write_text,
            "Exercise": self.contact_text,
            "Dev": self.misc_text,
        }

        self.info_text = self.ui.InfoText
        self.file_select_text = self.ui.FileSelect
        self.date_text = self.ui.DateLine
        self.selected_text = self.ui.SelectedLine
        self.time_text = self.ui.TimeLine

        self.objective_edit = self.ui.ObjectiveEdit
        self.summary_edit = self.ui.SummaryEdit

    def setup(self):
        home = os.path.expanduser("~")
        default_loc = os.path.join(home, ".code_time_skm", "default_life.txt")
        os.makedirs(os.path.dirname(default_loc), exist_ok=True)
        self.code_time = CodeTime(default_loc=default_loc)
        self.selected_file = self.code_time.filename

        if self.code_time.filename is not None:
            self.file_select_text.setText("Saving to " + self.code_time.filename)
        else:
            self.file_select_text.setText("Please select a file...")

        self.file_select_button.clicked.connect(self.selectFile)
        self.save_button.clicked.connect(self.save)
        self.stop_button.clicked.connect(self.stop)
        self.quit_button.clicked.connect(self.save_quit)

        self.code_button.clicked.connect(self.coding_hit)
        self.contact_button.clicked.connect(self.contact_hit)
        self.misc_button.clicked.connect(self.misc_hit)
        self.read_button.clicked.connect(self.read_hit)
        self.write_button.clicked.connect(self.write_hit)

        self.date_text.setText("Today is " + self.code_time.today)
        self.objective_edit.setPlainText(self.code_time.meta_dict["Misc"])
        self.summary_edit.setPlainText(self.code_time.meta_dict["Summary"])
        self.selected_text.setText("Select a timer to start timing")

        if self.selected_file is None:
            self.info_text.setText("No file selected, please select one")
        else:
            self.info_text.setText("Selected {}".format(self.code_time.filename))

        self.timer = QTimer(self.window)
        self.timer.timeout.connect(self.on_update_timer)
        self.autosave_timer = QTimer(self.window)
        self.autosave_timer.timeout.connect(self.autosave)

    def selectFile(self):
        self.selected_file, _filter = self.file_dialog.getSaveFileName(
            self.window, "Save Output Times", os.path.expanduser("~"), "CSV (*.csv)"
        )
        self.file_select_text.setText("Saving to " + self.selected_file)
        self.info_text.setText("Will save to {}".format(self.selected_file))
        try:
            self.code_time.set_file(self.selected_file)
            self.code_time.load_file()
        except Exception:
            self.info_text.setText("Selected file could not be parsed")
            return

    def coding_hit(self):
        self.time_button_hit("Gaming")

    def read_hit(self):
        self.time_button_hit("Piano")

    def write_hit(self):
        self.time_button_hit("Sleep")

    def contact_hit(self):
        self.time_button_hit("Exercise")

    def misc_hit(self):
        self.time_button_hit("Dev")

    def time_button_hit(self, button_type):
        if self.code_time.selected == button_type:
            self.stop()
        else:
            self.code_time.set_selected(button_type)
            self.selected_text.setText("Timing " + button_type)
            self.timer.start(self.update_frequency)

    def stop(self):
        self.timer.stop()
        self.selected_text.setText("Timer paused")
        self.code_time.set_selected(None)

    def autosave(self):
        if self.code_time.filename is not None:
            self.code_time.save_to_file()
            self.info_text.setText(
                "Successfully autosaved to {} at {}".format(
                    self.code_time.filename,
                    datetime.datetime.now().strftime("%H:%M:%S"),
                )
            )

    def save(self):
        self.code_time.set_objective(self.objective_edit.toPlainText())
        self.code_time.set_summary(self.summary_edit.toPlainText())
        self.code_time.save_to_file()
        text = "Successfully saved to {} at {}".format(
            self.code_time.filename, datetime.datetime.now().strftime("%H:%M:%S")
        )
        try:
            self.code_time.to_nice_format()
        except PermissionError:
            out_name_xls = (
                os.path.splitext(self.code_time.filename)[0] + "_fancy" + ".xlsx"
            )
            text = "ERROR: Please close Excel sheet open at {}".format(out_name_xls)
        self.info_text.setText(text)

    def save_quit(self):
        self.save()
        self.appctxt.app.quit()

    def update_times(self):
        for key, val in self.code_time.time_dict.items():
            dt = datetime.timedelta(seconds=val)
            self.time_dict[key].setText(
                strfdelta(dt, "{hours} hours, {minutes} minutes, {seconds} seconds")
            )
        self.time_text.setText("Total today " + self.code_time.get_total_time())

    def on_update_timer(self):
        self.code_time.update(self.update_frequency_secs)
        self.update_times()


if __name__ == "__main__":
    here = os.path.dirname(os.path.realpath(__file__))
    ui = CodeTimeUI("codetime.ui")
    ui.start()
    sys.exit(ui.exit_code)
