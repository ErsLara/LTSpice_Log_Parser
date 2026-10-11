# LTSpice Log Parser

A lightweight utility to parse LTSpice simulation log files and extract `.MEAS` results into a clean overview text file.

## Features

- Automatically detects and parses LTSpice `.log` files.
- Extracts all `.MEAS` (measurement) results.
- Generates a structured statistical overview for quick analysis.

## How to Use

1. Download the latest executable: [`LTSpice_LOG_Parser.exe`](https://github.com/ErsLara/LTSpice_Log_Parser/releases/latest/download/LTSpice_LOG_Parser.exe).
2. Place the executable directly into your LTSpice simulation model folder.
3. Run your simulation in LTSpice.
4. Once the simulation finishes, run the LTSpice_LOG_Parser.exe. It will automatically process the `.log` file and generate a `<model_name>_meas_overview.txt` file containing the statistical summary of the measurements.

> **Note on Windows SmartScreen:** Because this executable is self-compiled and not digitally signed with a commercial certificate, Windows may show a "Windows protected your PC" warning when you first run it. Click on **"More info"** and then **"Run anyway"** to proceed. It is 100% safe and open-source.
