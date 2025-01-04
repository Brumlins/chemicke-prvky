import csv
import os

# Konstanty pro soubory
CSV_FILENAME = 'vstupy/elements.csv'
HTML_FILENAME = 'generated/periodic_table.html'


def load_elements_from_csv(filename):
    """
    Načte data prvků z CSV souboru a vrátí seznam slovníků.
    """
    elements = []
    try:
        with open(filename, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    elements.append({
                        'symbol': row['Symbol'],
                        'name': row['Element'],
                        'atomic_number': int(row['AtomicNumber']),
                        'group': int(row['Group']),
                        'period': int(row['Period']),
                    })
                except ValueError:
                    print(f"Chyba při zpracování řádku: {row}")
    except FileNotFoundError:
        print(f"Soubor {filename} nebyl nalezen.")
    return elements


def generate_html_table(elements, output_filename):
    """
    Generuje HTML tabulku s prvky.
    """
    try:
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, 'w', encoding='utf-8') as html_file:
            html_file.write("<!DOCTYPE html><html><head><style>")
            html_file.write(".element { border: 1px solid black; padding: 10px; text-align: center; }")
            html_file.write("table { border-collapse: collapse; width: 100%; table-layout: fixed; }")
            html_file.write("tr:nth-child(even) { background-color: #f2f2f2; }")
            
            # Styling pro periodickou tabulku
            html_file.write(".periodic-table td { border: 1px solid #000; }")
            html_file.write(".periodic-table th { background-color: #ddd; }")
            html_file.write("</style></head><body>")
            html_file.write("<h1>Periodická tabulka prvků</h1>")
            html_file.write("<table class='periodic-table'>")
            
            # Vypíše hlavičku tabulky
            html_file.write("<tr>")
            html_file.write("<th>Symbol</th><th>Název</th><th>Atomové číslo</th>")
            html_file.write("<th colspan='4'>Skupina</th>")
            html_file.write("<th>Perioda</th>")
            html_file.write("</tr>")

            # Generování řádků tabulky
            for element in elements:
                html_file.write("<tr>")
                html_file.write(f"<td class='element'>{element['symbol']}</td>")
                html_file.write(f"<td class='element'>{element['name']}</td>")
                html_file.write(f"<td class='element'>{element['atomic_number']}</td>")
                html_file.write(f"<td class='element' colspan='4'>{element['group']}</td>")
                html_file.write(f"<td class='element'>{element['period']}</td>")
                html_file.write("</tr>")

            html_file.write("</table>")
            html_file.write("</body></html>")

        print(f"HTML tabulka byla vygenerována a uložena jako {output_filename}.")
    except Exception as e:
        print(f"Chyba při generování HTML souboru: {e}")


def main():
    """
    Hlavní funkce programu.
    """
    elements = load_elements_from_csv(CSV_FILENAME)
    if elements:
        generate_html_table(elements, HTML_FILENAME)
    else:
        print("Nepodařilo se načíst žádné prvky.")


if __name__ == '__main__':
    main()
