import csv
import xml.etree.ElementTree as ET

def nacti_prvky_z_csv(soubor):
    """
    Nacte data z csv souboru a ulozi je do seznamu slovniku.
    Kazdy slovnik obsahuje klice: 'symbol', 'nazev', 'atomove_cislo', 'skupina', 'perioda', 'hmotnost', 'stav'.
    """
    prvky = []
    with open(soubor, 'r', encoding='utf-8') as csv_soubor:
        ctenar = csv.DictReader(csv_soubor)
        for radek in ctenar:
            try:
                prvky.append({
                    'symbol': radek['Symbol'],
                    'nazev': radek['Element'],
                    'atomove_cislo': int(radek['AtomicNumber']),
                    'skupina': radek['Group'],
                    'perioda': int(radek['Period']),
                    'hmotnost': float(radek['AtomicMass']),
                    'stav': radek['Phase']
                })
            except KeyError as chyba:
                print(f"Chybi klic v csv souboru: {chyba}")
    return prvky

def zobraz_menu():
    """
    Vypise moznosti menu.
    """
    print("Chemicka databaze")
    print("1. Vyhledat prvek")
    print("2. Spocitat prumernou hmotnost")
    print("3. Export do markdown")
    print("4. Export do xml")
    print("5. Ukoncit")

def vyber_moznost():
    """
    Ziska vyber uzivatele.
    """
    return input("Zadejte moznost: ")

def vyhledej_prvek(prvky, kriterium, hodnota):
    """
    Vyhleda prvky dle zadaneho kriteriu a hodnoty.
    """
    return [prvek for prvek in prvky if str(prvek[kriterium]).lower() == hodnota.lower()]

def zobraz_vlastnosti_prvku(prvek):
    """
    Zobrazi detaily daneho prvku.
    """
    for klic, hodnota in prvek.items():
        print(f"{klic}: {hodnota}")

def spocitej_prumernou_hmotnost(prvky, skupina=None, perioda=None):
    """
    Spocita prumernou hmotnost prvku podle filtru.
    """
    vyfiltrovane = prvky
    if skupina:
        vyfiltrovane = [p for p in vyfiltrovane if p['skupina'] == skupina]
    if perioda:
        vyfiltrovane = [p for p in vyfiltrovane if p['perioda'] == perioda]
    if not vyfiltrovane:
        return 0
    return sum(p['hmotnost'] for p in vyfiltrovane) / len(vyfiltrovane)

def export_do_markdown(prvky, soubor="generated/prvky.md"):
    """
    Exportuje prvky do markdown souboru.
    """
    with open(soubor, 'w', encoding='utf-8') as md_soubor:
        for prvek in prvky:
            md_soubor.write(f"## {prvek['nazev']} ({prvek['symbol']})\n")
            md_soubor.write(f"- **Atomove cislo:** {prvek['atomove_cislo']}\n")
            md_soubor.write(f"- **Skupina:** {prvek['skupina']}\n")
            md_soubor.write(f"- **Perioda:** {prvek['perioda']}\n")
            md_soubor.write(f"- **Hmotnost:** {prvek['hmotnost']}\n")
            md_soubor.write(f"- **Stav:** {prvek['stav']}\n\n")

def export_do_xml(prvky, soubor='generated/prvky.xml'):
    """
    Exportuje prvky do xml souboru.
    """
    koren = ET.Element("prvky")
    for prvek in prvky:
        element = ET.SubElement(koren, "prvek")
        for klic, hodnota in prvek.items():
            podrobnost = ET.SubElement(element, klic)
            podrobnost.text = str(hodnota)
    strom = ET.ElementTree(koren)
    strom.write(soubor, encoding='utf-8', xml_declaration=True)
    print(f"Data ulozena do souboru: {soubor}")
