import os
import re
import pandas as pd

def parse_ltspice_logs():
    # Busca todos os arquivos .log na pasta atual
    log_files = [f for f in os.listdir('.') if f.endswith('.log')]
    
    if not log_files:
        print("No .log file found.")
        return

    for log_file_name in log_files:
        print(pid := f"Processing: {log_file_name}...") # Mensagem útil caso queira ver o progresso
        
        # 1. Leitura segura do arquivo com tratamento de encoding
        try:
            with open(log_file_name, "rt", encoding="utf-8", errors="ignore") as f:
                log_content = f.read()
        except Exception as e:
            print(f"Error reading {log_file_name}: {e}")
            continue

        # 2. Extração via Regex
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
                    continue  # Ignora valores que não puderem ser convertidos para float

        # Pula se nenhum dado válido foi encontrado
        if not meas_dict:
            print(f"Warning: No valid meas found in {log_file_name}.")
            continue

        # 3. Criação segura do DataFrame (protege contra tamanhos de listas desiguais)
        try:
            meas_results_df = pd.DataFrame({k: pd.Series(v) for k, v in meas_dict.items()})
        except Exception as e:
            print(f"Error while mounting {log_file_name} DataFrame: {e}")
            continue

        # 4. Estatísticas e formatação
        pd.set_option('display.max_columns', None)
        overview = meas_results_df.describe(percentiles=[], include='all')

        # Remove o "50%" apenas se ele realmente existir no índice
        if "50%" in overview.index:
            overview = overview.drop("50%")
        
        # 5. Escrita segura do arquivo de saída
        output_file_name = log_file_name.replace(".log", "_meas_overview.txt")
        
        try:
            with open(output_file_name, "w", encoding="utf-8") as output_file:
                output_file.write(str(overview))
            print(f"Success generating: {output_file_name}")
        except Exception as e:
            print(f"Error saving output file {output_file_name}: {e}")

if __name__ == "__main__":
    parse_ltspice_logs()