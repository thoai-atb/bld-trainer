import csv
from pathlib import Path
from colorist import Color

uf_commns_path = Path(__file__).with_name('uf_comms.csv')
uf_types_path = Path(__file__).with_name('uf_types.csv')
ufr_commns_path = Path(__file__).with_name('ufr_comms.csv')
ufr_types_path = Path(__file__).with_name('ufr_types.csv')

def load_data(file_path):
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

def train(title, comms, types, color1, color2):
    while True:
        prompt = input(f"\nInput letter pair for {title} commutator: ")
        if prompt in ["q", "quit"]:
            break
        if prompt in comms and prompt in types:
            print(f"{color1}{types[prompt]}:{color2} {comms[prompt]}{Color.OFF}")
        else:
            print("Sorry, did not find that in database")

while True:
    option = input("Select training option:\n(1) Corners\n(2) Edges\n-> ")
    if option == "1":
        comms = load_data(ufr_commns_path)
        types = load_data(ufr_types_path)
        color1 = Color.CYAN
        color2 = Color.YELLOW
        train("UFR", comms, types, color1, color2)
    elif option == "2":
        comms = load_data(uf_commns_path)
        types = load_data(uf_types_path)
        color1 = Color.GREEN
        color2 = Color.YELLOW
        train("UF", comms, types, color1, color2)
    elif option in ["q", "quit"]:
        break
    print()