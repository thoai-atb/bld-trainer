import csv, json
from pathlib import Path
from colorist import Color

uf_commns_path = Path(__file__).with_name('uf_comms.csv') # source: dylan's 3-style learning sheet
uf_types_path = Path(__file__).with_name('uf_types.csv') # source: dylan's 3-style learning sheet
uf_correction_path = Path(__file__).with_name('uf_corrections.json') # user-generated
ufr_commns_path = Path(__file__).with_name('ufr_comms.csv') # source: dylan's 3-style learning sheet
ufr_types_path = Path(__file__).with_name('ufr_types.csv') # source: dylan's 3-style learning sheet
ufr_correction_path = Path(__file__).with_name('ufr_corrections.json') # user-generated

def load_csv(file_path):
    database = {}
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        columns = []
        for row in csv_reader:
            if columns == []:
                columns = row
                continue
            row_name = row[0][0].lower()
            for idx in range(1, len(row)):
                column_name = columns[idx][0].lower()
                data = row[idx]
                if data:
                    database[column_name + row_name] = data
    return database

def load_correction(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.loads(file.read())
    except:
        return {}

def save_correction(file_path, database):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(database, file)

def train(title, comms, types, color1, color2, correction_path):
    correction_db = load_correction(correction_path)
    while True:
        prompt = input(f"\nInput letter pair for {title} commutator: ")
        if not prompt.strip(): continue
        # Quit
        if prompt in ["q", "quit"]:
            break
        # Add correction
        if prompt.startswith("fix"):
            elements = prompt.split(None, 2)
            if elements[0] != "fix":
                print("Sorry, command has wrong format! Usage: fix <letter-pair> <correction>")
                continue
            letter_pair = elements[1]
            if not (letter_pair in comms and letter_pair in types):
                print(f"Sorry, did not find {color1}{letter_pair}{Color.OFF} in database")
                continue
            correction = elements[2]
            if not correction:
                print("Sorry, correction is empty! Usage: fix <letter-pair> <correction>")
                continue
            correction_db[letter_pair] = correction
            save_correction(correction_path, correction_db)
            print(f"The letter pair {color1}{letter_pair}{Color.OFF} was corrected with: {color2}{correction}{Color.OFF}")
            continue
        # Unfix correction
        if prompt.startswith("unfix"):
            elements = prompt.split()
            if elements[0] != "unfix":
                print("Sorry, command has wrong format! Usage: fix <letter-pair> <correction>")
                continue
            letter_pair = elements[1]
            if not (letter_pair in correction_db):
                print(f"Sorry, did not find {color1}{letter_pair}{Color.OFF} in correction database")
                continue
            correction_db.pop(letter_pair)
            save_correction(correction_path, correction_db)
            print(f"The correction for {color1}{letter_pair}{Color.OFF} was removed")
            continue
        # Show original
        if prompt.startswith("show"):
            elements = prompt.split()
            if elements[0] != "show":
                print("Sorry, command has wrong format! Usage: show <letter-pair>")
                continue
            letter_pair = elements[1]
            if not (letter_pair in comms and letter_pair in types):
                print(f"Sorry, did not find {color1}{letter_pair}{Color.OFF} in database")
                continue
            print(f"{color1}{types[letter_pair]}:{color2} {comms[letter_pair]} (original){Color.OFF}")
            continue
        # Show normal - replace with correct if exists
        if prompt in comms and prompt in types:
            comm = comms[prompt]
            if prompt in correction_db:
                comm = f"{correction_db[prompt]} (corrected)"
            print(f"{color1}{types[prompt]}:{color2} {comm}{Color.OFF}")
        else:
            print(f"Sorry, did not find juice{prompt}juice in database")

while True:
    option = input("Select training option:\n(1) Corners\n(2) Edges\n-> ")
    if option in ["1", "c", ""]:
        comms = load_csv(ufr_commns_path)
        types = load_csv(ufr_types_path)
        color1 = Color.CYAN
        color2 = Color.YELLOW
        train("UFR", comms, types, color1, color2, ufr_correction_path)
    elif option in ["2", "e"]:
        comms = load_csv(uf_commns_path)
        types = load_csv(uf_types_path)
        color1 = Color.GREEN
        color2 = Color.YELLOW
        train("UF", comms, types, color1, color2, uf_correction_path)
    elif option in ["q", "quit"]:
        break
    print()