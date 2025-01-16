import re
import pandas as pd

LTSpiceLOG = open(".\\LTSpice_Example\\LTSPICE_Example.log", "rt")

log_content = LTSpiceLOG.read()

LTSpiceLOG.close()

pattern = re.compile(r"^Measurement:\s(.+)|^\s+\d+\s(\d+\.?\d+)", re.MULTILINE)

meas_results = pattern.findall(log_content)


