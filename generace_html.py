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
                        'group': int(row['Group']) if row['Group'] else None,
                        'period': int(row['Period']),
                        'category': row['Category'] if 'Category' in row else "Unknown"
                    })
                except ValueError:
                    print(f"Chyba při zpracování řádku: {row}")
    except FileNotFoundError:
        print(f"Soubor {filename} nebyl nalezen.")
    return elements

def generate_html_table(elements, output_filename):
    """
    Generuje HTML tabulku s prvky ve formátu periodické tabulky.
    """
    # Mapování kategorií na barvy
    category_colors = {
        "alkali metal": "#ff6666",
        "alkaline earth metal": "#ffdead",
        "transition metal": "#ffcc80",
        "post-transition metal": "#cccccc",
        "metalloid": "#cccc99",
        "nonmetal": "#bdecb6",
        "halogen": "#ffb3b3",
        "noble gas": "#add8e6",
        "lanthanoid": "#ffbfff",
        "actinoid": "#ff99ff",
        "Unknown": "#ffffff"
    }

    # Rozložení tabulky - pozice prvků
    layout = [
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["1", "H", "", "", "", "", "", "", "", "", "", "", "", "", "", "","","","" ,"He"],
        ["2", "Li", "Be", "", "", "", "", "", "", "", "", "", "", "", "B", "C", "N", "O", "F", "Ne"],
        ["3", "Na", "Mg", "", "", "", "", "", "", "", "", "", "", "", "Al", "Si", "P", "S", "Cl", "Ar"],
        ["4", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "", "Ga", "Ge", "As", "Se", "Br", "Kr"],
        ["5", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "", "In", "Sn", "Sb", "Te", "I", "Xe"],
        ["6", "Cs", "Ba", "", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "", "Tl", "Pb", "Bi", "Po", "At", "Rn"],
        ["7", "Fr", "Ra", "", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Lanthanoids", "", "", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"],
        ["Actinoids", "", "", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"]
    ]

    elements_dict = {e['symbol']: e for e in elements}

    try:
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, 'w', encoding='utf-8') as html_file:
            html_file.write("<!DOCTYPE html><html><head><style>")
            html_file.write(".periodic-table { border-collapse: collapse; margin: 20px auto; }")
            html_file.write(".periodic-table td { width: 50px; height: 50px; text-align: center; border: 1px solid #ccc; }")
            html_file.write(".periodic-table td.empty { background-color: #fff; border: none; }")
            html_file.write(".periodic-table .element { font-size: 12px; padding: 5px; }")
            html_file.write(".periodic-table .header { font-weight: bold; background-color: #ddd; }")
            for category, color in category_colors.items():
                html_file.write(f".periodic-table .{category.replace(' ', '-')} {{ background-color: {color}; }}")
            html_file.write("</style></head><body>")

            html_file.write("<h1>Periodická tabulka prvků</h1>")
            html_file.write("<table class='periodic-table'>")

            for row in layout:
                html_file.write("<tr>")
                for cell in row:
                    if not cell or cell == "":
                        html_file.write("<td class='empty'></td>")
                    elif cell in elements_dict:
                        element = elements_dict[cell]
                        category_class = element['category'].replace(" ", "-")
                        html_file.write(f"<td class='element {category_class}'>")
                        html_file.write(f"<strong>{element['symbol']}</strong><br>{element['atomic_number']}<br>{element['name']}")
                        html_file.write("</td>")
                    else:
                        html_file.write(f"<td class='element header'>{cell}</td>")
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
