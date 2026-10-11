import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def parse_ltspice_logs():
    # Search for all .log files in the current directory
    log_files = [f for f in os.listdir('.') if f.endswith('.log')]
    
    if not log_files:
        print("No .log files found in the directory.")
        return

    for log_file_name in log_files:
        print(f"Processing: {log_file_name}...")
        
        # 1. Safe file reading with encoding handling
        try:
            with open(log_file_name, "rt", encoding="utf-8", errors="ignore") as f:
                log_content = f.read()
        except Exception as e:
            print(f"Error reading {log_file_name}: {e}")
            continue

        # 2. Regex extraction
        pattern = re.compile(r"^Measurement:\s(.+)|^\s+\d+\s(-?\d*\.*\d*e?-?\d+)", re.MULTILINE)
        meas_results = pattern.findall(log_content)
        
        meas_dict = {}
        signal_name = None
        
        for signal, value in meas_results:
            if signal:
                signal_name = signal.strip()
                if signal_name not in meas_dict:
                    meas_dict[signal_name] = []
            elif value and signal_name:
                try:
                    meas_dict[signal_name].append(float(value))
                except ValueError:
                    continue  # Ignore values that cannot be converted to float

        # Skip if no valid data was found
        if not meas_dict:
            print(f"Warning: No valid measurements found in {log_file_name}.")
            continue

        # 3. Safe DataFrame creation
        try:
            meas_results_df = pd.DataFrame({k: pd.Series(v) for k, v in meas_dict.items()})
        except Exception as e:
            print(f"Error building DataFrame for {log_file_name}: {e}")
            continue

        # 4. Statistics and overview text generation
        pd.set_option('display.max_columns', None)
        overview = meas_results_df.describe(percentiles=[], include='all')

        # Remove "50%" only if it actually exists in the index
        if "50%" in overview.index:
            overview = overview.drop("50%")
        
        output_file_name = log_file_name.replace(".log", "_meas_overview.txt")
        
        try:
            with open(output_file_name, "w", encoding="utf-8") as output_file:
                output_file.write(str(overview))
            print(f"Overview successfully generated: {output_file_name}")
        except Exception as e:
            print(f"Error saving output file {output_file_name}: {e}")

        # 5. Generate a histogram plot for each signal found
        for col in meas_results_df.columns:
            # Clean signal name to be safe for filenames (e.g., remove invalid path characters)
            safe_signal_name = re.sub(r'[\\/*?:"<>|]', "_", col)
            histogram_filename = f"{safe_signal_name}_histogram.png"
            
            try:
                plt.figure(figsize=(8, 5))
                sns.histplot(meas_results_df[col].dropna(), kde=True, color='skyblue', edgecolor='black')
                
                plt.title(f"Histogram of {col}", fontsize=12, fontweight='bold')
                plt.xlabel(col, fontsize=10)
                plt.ylabel("Frequency", fontsize=10)
                plt.grid(True, linestyle='--', alpha=0.6)
                
                plt.tight_layout()
                plt.savefig(histogram_filename, dpi=300)
                plt.close()
                print(f"Histogram generated: {histogram_filename}")
            except Exception as e:
                print(f"Error generating histogram for signal '{col}': {e}")

if __name__ == "__main__":
    parse_ltspice_logs()