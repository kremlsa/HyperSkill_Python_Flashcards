# Write your code here
import argparse
import json
import random
from collections import defaultdict


def print_log(entry):
    global logs
    print(entry)
    logs.append(entry)


def input_log():
    global logs
    result = input()
    logs.append(result)
    return result


def add_card():
    global flashcards
    print_log("The term for card:")
    while True:
        key = input_log()
        if key in flashcards.keys():
            print_log('The term "{}" already exists. Try again:'.format(key))
            continue
        break
    print_log("The definition for card:")
    while True:
        value = input_log()
        if value in flashcards.values():
            print_log('The definition "{}" already exists. Try again:'.format(value))
            continue
        break
    flashcards[key] = value
    print_log('The pair ("{}":"{}") has been added.'.format(key, value))


def remove_card():
    global flashcards, statistics
    print_log('Which card?')
    card_name = input_log()
    if card_name in list(flashcards.keys()):
        flashcards.pop(card_name)
        print_log('The card has been removed.')
        if card_name in list(statistics.keys()):
            statistics.pop(card_name)
    else:
        print_log('Can\'t remove "{}": there is no such card.'.format(card_name))


def import_card():
    global flashcards, statistics
    print_log('File name:')
    file_name = input_log()
    try:
        with open(file_name , 'r') as f:
            temp = json.load(f)
            flashcards = temp["flashcards"]
            statistics = temp["statistics"]
            print_log('{} cards have been loaded.'.format(len(flashcards)))
    except FileNotFoundError:
        print_log("File not found.")


def export_card():
    global flashcards, statistics
    print_log('File name:')
    file_name = input_log()
    with open(file_name, 'w') as f:
        temp = {"flashcards": flashcards, "statistics": statistics}
        json.dump(temp, f)
    print_log('{} cards have been saved.'.format(len(flashcards)))


def save_log():
    print_log('File name:')
    file_name = input_log()
    with open(file_name, 'w') as f:
        f.write("\n".join(str(entry) for entry in logs))
    print_log('The log has been saved.')


def ask_card():
    global flashcards , statistics
    print_log("How many times to ask?")
    num_of_asks = int(input_log())
    for i in range(num_of_asks):
        key = random.choice(list(flashcards.keys()))
        print_log('Print the definition of "{}":'.format(key))
        answer = input_log()
        if answer == flashcards[key]:
            print_log('Correct!')
        elif answer in flashcards.values():
            print_log('Wrong. The right answer is "{}", but your definition is correct for "{}".'
                      .format(flashcards[key] , list(flashcards.keys())[list(flashcards.values()).index(answer)]))
            statistics[key] += 1
        else:
            print_log('Wrong. The right answer is "{}".'.format(flashcards[key]))
            statistics[key] += 1


def hardest_card():
    global statistics
    if len(statistics) > 0:
        max_value = max(statistics.values())
        keys = [k for k, v in statistics.items() if v == max_value]
        keys = ['"' + k + '"' for k in keys]
        print_log('The hardest card is {}. You have {} errors answering it.'
              .format(", ".join(keys), max_value))
    else:
        print_log('There are no cards with errors.')


def menu():
    global statistics, flashcards, args
    if args.import_from is not None:
        try:
            with open(args.import_from, 'r') as f:
                temp = json.load(f)
                flashcards = temp["flashcards"]
                statistics = temp["statistics"]
                print_log('{} cards have been loaded.'.format(len(flashcards)))
        except FileNotFoundError:
            print_log("File not found.")
    while True:
        print_log('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        action = input()
        if action == "add":
            add_card()
        if action == "remove":
            remove_card()
        if action == "import":
            import_card()
        if action == "export":
            export_card()
        if action == "ask":
            ask_card()
        if action == "reset stats":
            statistics.clear()
            print_log('Card statistics have been reset.')
        if action == "hardest card":
            hardest_card()
        if action == "log":
            save_log()
        if action == "exit":
            print_log('Bye bye!')
            if args.export_to is not None:
                with open(args.export_to, 'w') as f:
                    temp = {"flashcards": flashcards, "statistics": statistics}
                    json.dump(temp, f)
                print_log('{} cards have been saved.'.format(len(flashcards)))
            break


parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()
flashcards = {}
statistics = defaultdict(int)
logs = []
menu()
