import re
import pandas as pd

LTSpiceLOG = open(".\\LTSpice_Example\\LTSPICE_Example.log", "rt")

log_content = LTSpiceLOG.read()

LTSpiceLOG.close()

pattern = re.compile(r"^Measurement:\s(.+)|^\s+\d+\s(\d+\.?\d+)", re.MULTILINE)

meas_results = pattern.findall(log_content)

meas_dict = {}

for signal, value in meas_results:
    if signal:
        signal_name = signal
        meas_dict[signal_name] = []
    elif value:
        meas_dict[signal_name].append(float(value))

print(meas_dict)