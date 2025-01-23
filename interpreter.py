# -*- coding: utf-8 -*-
import time
from tqdm import tqdm

# Mapa paneli
panel_mapping = {
    0x100: "PANEL OPERATORSKI 1 HB",
    0x108: "PANEL OPERATORSKI 2 HB",
    0x110: "PANEL OPERATORSKI 3 HB",
    0x118: "PANEL OPERATORSKI 4 HB",
    0x120: "PANEL OPERATORSKI 5 HB",
    0x128: "PANEL OPERATORSKI 6 HB",
    0x130: "PANEL OPERATORSKI 7 HB",
    0x138: "PANEL OPERATORSKI 8 HB",
}

# Funkcja do przetwarzania jednej linii logu
def process_line(line):
    try:
        # Rozdzielenie linii na czêœci
        parts = line.strip().split()
        timestamp, can_info = parts[0].strip('()'), parts[1]
        message = parts[2]

        # Konwersja znacznika czasu na datê i czas
        dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(timestamp)))

        # Wyodrêbnienie adresu i danych CAN
        address, data = message.split('#')
        address = int(address, 16)

        # Obs³uga regu³ dla adresów w zakresie 0x100-0x130
        panel_message = panel_mapping.get(address, "")
        if not panel_message:
            return ""  # Zwróæ pusty string, jeœli adres nie jest w zakresie

        # Obs³uga regu³ dla danych po #
        if data == "00":
            button_message = "PRZYCISK NIE WCISNIETY"
        elif data == "01":
            button_message = "PRZYCISK WCISNIETY"
        else:
            button_message = "DANE NIEZNANE"

        # Wynik przetwarzania
        result = f"{dt} {can_info} {message}"
        if panel_message:
            result += f"  {panel_message}"
        if button_message:
            result += f"  {button_message}"

        return result

    except Exception as e:
        return f"Blad przetwarzania linii: {line.strip()} ({e})"

# Odczyt pliku linia po linii i przetwarzanie
def process_log_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            processed = process_line(line)
            if processed:  # SprawdŸ, czy wynik nie jest pusty
                outfile.write(processed + '\n')

if __name__ == "__main__":
    # Œcie¿ka do pliku logu
    log_file_path = 'canfile.log'
    output_file_path = 'interpretacja_logu.log'
    process_log_file(log_file_path, output_file_path)
    # Odczyt pliku logu i przetwarzanie z paskiem postêpu
    with open(log_file_path, 'r') as infile:
        total_lines = sum(1 for line in infile)
    
    with open(log_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in tqdm(infile, total=total_lines, desc="Przetwarzanie logu"):
            processed = process_line(line)
            if processed:  # SprawdŸ, czy wynik nie jest pusty
                outfile.write(processed + '\n')
