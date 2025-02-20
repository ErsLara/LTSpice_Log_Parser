import re
import pandas as pd

log_file_name = r".\LTSpice_Example\LTSPICE_Example.log"

LTSpiceLOG = open(log_file_name, "rt")

log_content = LTSpiceLOG.read()

LTSpiceLOG.close()

pattern = re.compile(r"^Measurement:\s(.+)|^\s+\d+\s(-?\d+\.*\d*)", re.MULTILINE)

meas_results = pattern.findall(log_content)

meas_dict = {}

for signal, value in meas_results:
    if signal:
        signal_name = signal
        meas_dict[signal_name] = []
    elif value:
        meas_dict[signal_name].append(float(value))

meas_results_df = pd.DataFrame(meas_dict)

pd.set_option('display.max_columns', None)
overview = meas_results_df.describe(percentiles=[], include='all')
overview = overview.drop("50%")

output_file_name = log_file_name.replace(".log", "_meas_overview.txt")

output_file = open(output_file_name, "w")
output_file.write(str(overview))
output_file.close()
