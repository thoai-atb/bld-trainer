import os
import random
import subprocess
import json
from pathlib import Path

file_path = Path(__file__).with_name('letter_pairs.txt')
progress_path = Path(__file__).with_name('progress.json')

# global variables
g_to_reviews = []
g_batch_size = 50
g_batches = []
g_batch_number = 0
g_batch = []
g_database = {}

def read_data():
    pairs_map = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        # You can also read the file line by line
        for line in file:
            line = line.strip()
            if line == "":
                continue
            tokens = line.split(':', 1)
            pairs_map[tokens[0]] = tokens[1].strip()
    print("Loaded " + str(len(pairs_map.keys())) + " letter pairs...")
    return pairs_map

def extract_batches(data, size):
    keys = list(data.keys())
    batches = []
    while len(keys) > 0:
        batch = []
        for _ in range(size):
            if len(keys) == 0:
                break
            pair = random.choice(keys)
            keys.remove(pair)
            batch.append(pair)
        batches.append(batch)
    return batches

def load_progress():
    global g_batch_number, g_batch_size, g_to_reviews, g_batches, g_batch
    print("Loading progress...")
    if os.path.exists(progress_path):
        progress = {}
        with open(progress_path, 'r', encoding='utf-8') as progress_file:
            progress = json.loads(progress_file.read())
            g_batch_number = progress["batchNumber"]
            g_batch_size = progress["batchSize"]
            g_to_reviews.clear()
            g_to_reviews.extend(progress["toReviews"])
            g_batches.clear()
            g_batches.extend(progress["batches"])
            g_batch = g_batches[g_batch_number - 1]
            print("Progress loaded successfully.")
            print(f"Training batch {g_batch_number}/{len(g_batches)}...")
            return True
    else:
        print("Could not load progress...")
    return False

def new_progress():
    global g_batch_number, g_batch_size, g_to_reviews, g_batches, g_batch
    # batch size
    input_batch_size = input(
        "Input the batch size for reviewing (default: " + str(g_batch_size) + "): ")
    if input_batch_size.isnumeric():
        g_batch_size = int(input_batch_size)
    print("Using batch size of " + str(g_batch_size) + "...")
    # extract batches
    g_batches = extract_batches(g_database, g_batch_size)
    g_batch_number = 1
    g_batch = g_batches[g_batch_number - 1]
    print(f"Begin training batch {g_batch_number}/{len(g_batches)}...")

g_database = read_data()  # data = { "ab": "...", "ac": "...", ... }
if not load_progress():
    new_progress()

while True:
    # choose and print question
    pair = g_batch[-1]
    data = g_database[pair]
    number_top = len(g_database.keys()) - sum(len(x) for x in g_batches) + 1
    option = input(f"\n{number_top} - {pair} ? ")

    # check special options
    if option in ['+', 'edit']:
        print("Editing...")
        process = subprocess.Popen(
            ['start', '', file_path], shell=True)  # On Windows
        input("Press enter when you have finished editing...")
        g_database = read_data()
        continue
    elif option in ['r', 'reload']:
        print("Reloading...")
        g_database = read_data()
        continue
    elif option in ['s', 'save']:
        print("Saving progress...")
        progress = {
            "batchNumber": g_batch_number,
            "batchSize": g_batch_size,
            "toReviews": g_to_reviews,
            "batches": g_batches
        }
        with open(progress_path, 'w', encoding='utf-8') as progress_file:
            json.dump(progress, progress_file)
            print("Progress saved.")
            continue
    elif option in ['l', 'load']:
        load_progress()
        continue
    elif option in ['n', 'new']:
        new_progress()
        continue
    elif option in ['q', 'quit']:
        break

    # check review option
    if '\\' in option:
        g_to_reviews.append(pair)
    print(data)
    g_batch.remove(pair)

    # check no more pairs
    if len(g_batch) == 0:
        if len(g_to_reviews) > 0:
            input("Let's review those " + str(len(g_to_reviews)) +
                  " letter pairs that you've missed...\n")
            g_batch.extend(g_to_reviews)
            random.shuffle(g_batch)
            g_to_reviews = []
            continue
        emoji_list = ['😀', '😍', '😎', '🤑', '🤢', '😇', '👻', '🤖', '😺', '🐵', '🦒', '🐭',
                      '🐷', '🐸', '🦄', '🐲', '🐪', '🦎', '🐬', '🐳', '🐠', '🦆', '🦢', '🐤',
                      '🪰', '🐞', '👀', '🧠', '🫵', '✌️', '🤘', '🤙', '👌', '👍', '🤟', '👏',
                      '🙌', '🙏', '🎈', '🧨', '✨', '🎃', '🎄', '🎊', '🧧', '🎀', '🎁', '🎗️',
                      '🕶️', '👙', '🩱', '👛', '👑', '🩴', '🪖', '💎', '🥎', '🎳', '🥇', '🏅',
                      '🪄', '🧩', '🔔', '🎵', '📯', '🎷', '🎺', '🔑', '🪓', '🧱', '🪵', '🧬',
                      '💊', '🪝', '🏹', '🪃', '🧮', '💡', '🔖', '💴', '✏️', '🖍️', '📌', '✂️',
                      '⏰', '🍕', '🥨', '🥩', '🫕', '🍭', '🍬', '🍫', '🧋', '🍉', '🍒', '🍆',
                      '🍓', '🌶️', '🍄', '🥑', '🌹', '🌺', '🌻', '🌼', '🌷', '🥀', '☘️', '🌴',
                      '🌵', '🌾', '🌿', '🍂', '🍃', '🚲', '🪂', '🚀', '🚨', '🚩', '🏁', '🏠',
                      '🗾', '🎌', '🛎️', '🪠', '🧼', '🪥', '🌥️', '🌨️', '🌜', '⭐', '☂️', '⚡',
                      '❄️', '☃️', '🔥', '💧']
        applause = random.choice(emoji_list)
        input("Good work! You've learned all the letter pairs from batch number " +
              str(g_batch_number) + "! " + applause * 6 + "\n")
        if g_batch_number < len(g_batches):
            g_batch_number += 1
            g_batch = g_batches[g_batch_number - 1]
            print(f"Begin training batch {g_batch_number}/{len(g_batches)}...")
            continue
        input("Congratulation! You've learned all the letter pairs!\n")
        break
