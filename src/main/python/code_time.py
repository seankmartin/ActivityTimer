"""This module holds the code time class."""
import datetime
import time
import os

import pandas as pd


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


class CodeTime(object):

    def __init__(self, keys=None, default_loc=None):
        if keys is None:
            keys = ["Coding", "Reading", "Writing", "Contact", "Misc"]
        self.time_dict = {}
        for k in keys:
            self.time_dict[k] = 0.0
        self.meta_dict = {"Objective": "Objective:", "Summary": "Summary:"}
        self.selected = None
        self.today = datetime.datetime.today().strftime("%d/%m/%Y")
        self.filename = None
        self.default_loc = default_loc
        self.delimeter = "|"

        self.populate()

    def set_file(self, filename):
        self.filename = filename
        if os.path.isfile(self.filename):
            self.load_file()

    def set_selected(self, selected):
        self.selected = selected

    def set_objective(self, objective):
        self.meta_dict["Objective"] = objective

    def set_summary(self, summary):
        self.meta_dict["Summary"] = summary

    def get_time(self):
        out_time = 0.00
        if self.selected is not None:
            out_time = self.time_dict[self.selected]
        dt = datetime.timedelta(seconds=out_time)
        return strfdelta(
            dt, "{hours} hours, {minutes} minutes, {seconds} seconds")

    def get_total_time(self):
        out_time = 0.00
        for time_val in self.time_dict.values():
            out_time += time_val
        dt = datetime.timedelta(seconds=out_time)
        return strfdelta(
            dt, "{hours} hours, {minutes} minutes, {seconds} seconds")

    def populate(self, in_fname=None):
        if self.default_loc is not None:
            if os.path.isfile(self.default_loc):
                with open(self.default_loc, "r") as f:
                    fname = f.read().strip()
                    self.set_file(fname)
        if in_fname is not None:
            self.set_file(in_fname)

    def stop(self):
        self.selected = None

    def update(self, elapsed_time):
        if self.selected is not None:
            self.time_dict[self.selected] += elapsed_time

    def load_file(self):
        with open(self.filename, "r") as f:
            df = pd.read_csv(f, sep=self.delimeter)
            this_row = df[df["Date"] == self.today]
            if len(this_row) == 0:
                return
            this_row_index = this_row.index[0]
            for key in this_row:
                if key == "Date":
                    continue
                elif key in list(self.time_dict.keys()):
                    value = this_row.get(key).at[this_row_index]
                    self.time_dict[key] = value
                else:
                    value = this_row.get(key).at[this_row_index]
                    self.meta_dict[key] = value

    def save_to_file(self):
        if os.path.isfile(self.filename):
            df = pd.read_csv(self.filename, sep=self.delimeter)
            this_row = df.index[df["Date"] == self.today]
            if len(this_row) == 0:
                dict_to_append = self.time_dict
                dict_to_append.update(self.meta_dict)
                dict_to_append["Date"] = self.today
                df = df.append(dict_to_append, ignore_index=True)
            else:
                for key, val in self.time_dict.items():
                    df.at[this_row, key] = val
                for key, val in self.meta_dict.items():
                    df.at[this_row, key] = val
            df.to_csv(self.filename, sep=self.delimeter, index=False)

        else:
            header_string = "Date" + self.delimeter
            header_string += self.delimeter.join(list(self.meta_dict.keys()))
            header_string += self.delimeter
            header_string += self.delimeter.join(list(self.time_dict.keys()))
            main_string = self.today + self.delimeter
            main_string += self.delimeter.join(list(self.meta_dict.values()))
            main_string += self.delimeter
            float_str_l = ["{:.2f}".format(v) for v in self.time_dict.values()]
            main_string += self.delimeter.join(float_str_l)
            with open(self.filename, "w") as f:
                f.write(header_string + "\n")
                f.write(main_string)

        with open(self.default_loc, "w") as f:
            f.write(self.filename)

    def to_nice_format(self):
        import math

        def change_function(x):
            if isinstance(x, float):
                if math.isnan(x):
                    return ""
                out_time = x
                dt = datetime.timedelta(seconds=out_time)
                return strfdelta(dt, "{hours} hours, {minutes} minutes")
            else:
                if "Summary: " in x:
                    x = x[len("Summary: "):]
                elif "Objective: " in x:
                    x = x[len("Objective: "):]
                elif "Summary:" in x:
                    x = x[len("Summary:"):]
                elif "Objective:" in x:
                    x = x[len("Objective:"):]
                return x

        def row_total(row):
            total = 0
            for k in self.time_dict.keys():
                total += row[k]
            return total

        df = pd.read_csv(self.filename, sep=self.delimeter)
        # Add a total row
        df['Total'] = df.apply(row_total, axis=1)
        df.loc['inf'] = df.mean()
        df.at['inf', "Date"] = "Average"

        out_fname = os.path.splitext(self.filename)[0] + "_fancy" + ".xlsx"
        df = df.applymap(change_function)
        df.to_excel(out_fname, index=False, freeze_panes=(1, 1))


if __name__ == "__main__":
    main_fname = r"E:\Google_Drive\PhD\Admin\timing.csv"
    main_default_loc = r"C:\Users\Sean\.code_time_skm\default.txt"
    ct = CodeTime(default_loc=main_default_loc)
    ct.to_nice_format()
    # ct.set_selected("Coding")

    # start_time = time.monotonic()
    # m_elapsed_time = 0.10
    # while (time.monotonic() - start_time) < 1.0:
    #     time.sleep(m_elapsed_time)
    #     ct.update(m_elapsed_time)

    # ct.stop()
    # ct.save_to_file()
