import os
import random
import subprocess
import json
from pathlib import Path

file_path = Path(__file__).with_name('letter_pairs.txt')
progress_path = Path(__file__).with_name('progress.json')


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


database = read_data()  # data = { "ab": "...", "ac": "...", ... }
to_reviews = []

# batch size
batch_size = 50
input_batch_size = input(
    "Input the batch size for reviewing (default: " + str(batch_size) + "): ")
if input_batch_size.isnumeric():
    batch_size = int(input_batch_size)
print("Using batch size of " + str(batch_size) + "...")

# extract batches
batches = extract_batches(database, batch_size)
current_batch_number = 1
batch = batches[current_batch_number - 1]
print("Begin training batch " + str(current_batch_number) +
      "/" + str(len(batches)) + "...")

while True:
    # choose and print question
    pair = batch[-1]
    data = database[pair]
    number_top = len(database.keys()) - sum(len(x) for x in batches) + 1
    option = input(str(number_top) + " - " + pair + " ? ")
    print(data)
    print()

    # check special options
    if option in ['+', 'edit']:
        print("Editing...")
        process = subprocess.Popen(
            ['start', '', file_path], shell=True)  # On Windows
        continue
    elif option in ['r', 'reload']:
        print("Reloading...")
        database = read_data()
        continue
    elif option in ['s', 'save']:
        print("Saving progress...")
        progress = {
            "batchNumber": current_batch_number,
            "batchSize": batch_size,
            "toReviews": to_reviews,
            "batches": batches
        }
        with open(progress_path, 'w', encoding='utf-8') as progress_file:
            json.dump(progress, progress_file)
            print("Progress saved.")
            continue
    elif option in ['l', 'load']:
        print("Loading progress...")
        if os.path.exists(progress_path):
            progress = {}
            with open(progress_path, 'r', encoding='utf-8') as progress_file:
                progress = json.loads(progress_file.read())
                current_batch_number = progress["batchNumber"]
                batch_size = progress["batchSize"]
                to_reviews.clear()
                to_reviews.extend(progress["toReviews"])
                batches.clear()
                batches.extend(progress["batches"])
                batch = batches[current_batch_number - 1]
                print("Progress loaded successfully.")
        else:
            print("Could not load progress!")
        continue
    elif option in ['q', 'quit']:
        break

    # check review option
    if '\\' in option:
        to_reviews.append(pair)

    # remove pair
    batch.remove(pair)

    # check no more pairs
    if len(batch) == 0:
        if len(to_reviews) > 0:
            input("Let's review those " + str(len(to_reviews)) +
                  " letter pairs that you've missed...\n")
            batch.extend(to_reviews)
            random.shuffle(batch)
            to_reviews = []
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
              str(current_batch_number) + "! " + applause * 6 + "\n")
        if current_batch_number < len(batches):
            current_batch_number += 1
            batch = batches[current_batch_number - 1]
            print("Begin training batch " + str(current_batch_number) +
                  "/" + str(len(batches)) + "...")
            continue
        input("Congratulation! You've learned all the letter pairs!\n")
        break
