from funkce import (
    nacti_prvky_z_csv,
    zobraz_menu,
    vyber_moznost,
    vyhledej_prvek,
    zobraz_vlastnosti_prvku,
    spocitej_prumernou_hmotnost,
    export_do_markdown,
    export_do_xml,
)
from generace_html import generate_html_table

# Cesty k datovým souborům
CSV_SOUBOR = 'vstupy/elements.csv'
GENEROVANY_HTML = 'vystupy/periodic_table.html'

# Načtení prvků z CSV
prvky = nacti_prvky_z_csv(CSV_SOUBOR)

while True:
    zobraz_menu()
    volba = vyber_moznost()

    if volba == '1':
        kriterium = input("Zadejte kritérium (symbol, nazev, atomove_cislo, skupina, perioda, stav): ").strip()
        hodnota = input("Zadejte hodnotu: ").strip()
        nalezene_prvky = vyhledej_prvek(prvky, kriterium, hodnota)
        if nalezene_prvky:
            for prvek in nalezene_prvky:
                zobraz_vlastnosti_prvku(prvek)
        else:
            print("Žádný prvek nebyl nalezen.")

    elif volba == '2':
        skupina = input("Zadejte skupinu (nepovinné): ").strip() or None
        perioda = input("Zadejte periodu (nepovinné): ").strip() or None
        prumerna_hmotnost = spocitej_prumernou_hmotnost(prvky, skupina, perioda)
        print(f"Průměrná relativní atomová hmotnost: {prumerna_hmotnost}")

    elif volba == '3':
        export_do_markdown(prvky)
        print("Data byla exportována do Markdown souboru.")

    elif volba == '4':
        export_do_xml(prvky)
        print("Data byla exportována do XML souboru.")

    elif volba == '5':
        generate_html_table(prvky)
        print(f"HTML tabulka byla vygenerována a uložena jako {GENEROVANY_HTML}.")

    elif volba == '6':
        print("Program ukončen.")
        break

    else:
        print("Neplatná volba, zkuste to znovu.")
