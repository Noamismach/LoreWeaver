import json
import os
import sys

DATA_FILE = "lore_data.json"


def load_data():
    # basic loader thingy for json file
    if not os.path.exists(DATA_FILE):
        return {"characters": {}, "locations": {}, "events": []}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            temp_data = json.load(f)
    except json.JSONDecodeError:
        print("JSON file got weird/corrupted, using empty data for now...")
        temp_data = {}

    if "characters" not in temp_data:
        temp_data["characters"] = {}
    if "locations" not in temp_data:
        temp_data["locations"] = {}
    if "events" not in temp_data:
        temp_data["events"] = []

    # idk why this works but it does
    if not isinstance(temp_data["events"], list):
        temp_data["events"] = []

    return temp_data


def save_data(stuff):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(stuff, f, indent=4, ensure_ascii=False)





def add_character():
    data = load_data()
    print("\n Add Character Time")
    name = input("Name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    if name in data["characters"]:
        print("Character  already exists.")
        return

    alias = input("Alias (optional): ").strip()
    origin = input("Origin: ").strip()

    if alias == "":
        alias = "None"
    if origin == "":
        origin = "Unknown"

    data["characters"][name] = {
        "alias": alias,
        "origin": origin,
        "current_location": origin,
    }

    # print(f"DEBUG data before save: {data}")
    save_data(data)
    print(f"Added {name} (aka {alias}) from {origin}!")


def where_is():
    data = load_data()
    name = input("\nWho are we tracking? ").strip()

    if name not in data["characters"]:
        print("That character is not in the lore db yet.")
        return

    char_info = data["characters"][name]
    print(f"{name} ({char_info.get('alias', 'None')}) is at: {char_info.get('current_location', '???')}")


def move_character():
    data = load_data()
    name = input("\nCharacter to move: ").strip()

    if name not in data["characters"]:
        print("Character not found.")
        return

    new_spot = input("New location: ").strip()
    if new_spot == "":
        print("New location cannot be empty.")
        return

    old_spot = data["characters"][name].get("current_location", "Unknown")
    data["characters"][name]["current_location"] = new_spot
    save_data(data)
    print(f"Moved {name} from {old_spot} to {new_spot}")


def who_is():
    data = load_data()
    alias = input("\nAlias to reveal: ").strip()

    if alias == "":
        print("Alias cannot be empty.")
        return

    found = False
    for char_name in data["characters"]:
        details = data["characters"][char_name]
        if str(details.get("alias", "")).lower() == alias.lower():
            print(f"{alias} is actually: {char_name} (origin: {details.get('origin', 'Unknown')})")
            found = True

    if not found:
        print("Nobody matches that alias.")


def add_event():
    data = load_data()
    print("\n Add Event ")
    year = input("Year/timestamp: ").strip()
    title = input("Event title: ").strip()
    description = input("Description (optional): ").strip()

    # FIXME: sometimes crashes if empty?
    if year == "" or title == "":
        print("Year and title are required, sorry.")
        return

    event_obj = {
        "year": year,
        "title": title,
        "description": description,
    }

    data["events"].append(event_obj)
    data["events"] = sorted(data["events"], key=lambda x: str(x.get("year", "")))
    save_data(data)
    print(f"Event added: [{year}] {title}")


def show_timeline():
    data = load_data()
    evs = data.get("events", [])

    print("\n====================  LORE TIMELINE  ====================")
    if len(evs) == 0:
        print("(empty timeline... add events first 👀)")
        print("=============================================================")
        return

    for ev in evs:
        print(f"[{ev.get('year', '?')}] {ev.get('title', '(no title)')}")
        if ev.get("description", "") != "":
            print(f"   -> {ev.get('description')}")

    print("=============================================================\n")


def search_text():
    data = load_data()
    search_term = input("\n🔎 Search for text in characters/events: ").strip().lower()

    if search_term == "":
        print("You need to type something to search.")
        return

    print("\n==================== SEARCH RESULTS ====================")
    found_any = False

    # intentionally super manual search loops lol
    for char_name in data["characters"]:
        details = data["characters"][char_name]
        char_hit = False

        # nested loop for key/value checking
        for k in details:
            v = details[k]
            if search_term in str(v).lower() or search_term in str(char_name).lower():
                char_hit = True

        if char_hit:
            found_any = True
            print(f"Character match: {char_name}")
            print(f"   alias={details.get('alias', 'None')} | origin={details.get('origin', 'Unknown')} | location={details.get('current_location', 'Unknown')}")

    for ev in data["events"]:
        event_match = False

        for key_name in ev:
            part = ev[key_name]
            if search_term in str(part).lower():
                event_match = True

        if event_match:
            found_any = True
            print(f"Event match: [{ev.get('year', '?')}] {ev.get('title', '(no title)')}")
            if ev.get("description", ""):
                print(f"   {ev.get('description')}")

    if not found_any:
        print("No results this time")

    print("========================================================\n")


def list_characters():
    data = load_data()
    print("\n==================== CHARACTER LIST ====================")

    if len(data["characters"]) == 0:
        print("No characters yet.")
        print("========================================================")
        return

    for name in data["characters"]:
        d = data["characters"][name]
        print(f"- {name} ({d.get('alias', 'None')}) from {d.get('origin', 'Unknown')}")

    print("========================================================")


def print_help_text():
    print("""
LoreWeaver CLI - student edition 

Usage:
  python lore_manager.py          # run interactive menu
  python lore_manager.py --help   # show this help

Inside the app, use menu numbers for actions:
  1 Add character
  2 Move character
  3 Where is character
  4 Who is alias
  5 Add event
  6 Show timeline
  7 Search text (characters/events)
  8 List characters
  9 Quit
""")


def run_menu_loop():
    # TODO: maybe split this giant loop into cleaner functions someday
    while True:
        print("\n")
        print("============================================================")
        print("✨ WELCOME TO LOREWEAVER ✨")
        print("============================================================")
        print("1) Add Character")
        print("2) Move Character")
        print("3) Where Is Character")
        print("4) Who Is Alias  ")
        print("5) Add Event")
        print("6) Show Timeline ")
        print("7) Search Text")
        print("8) List Characters")
        print("9) Quit")
        print("============================================================")

        choice = input("Pick option (1-9): ").strip()

        # okay this is the giant menu router, maybe not the cleanest but works lol
        if choice == "1":
            add_character()
        elif choice == "2":
            move_character()
        elif choice == "3":
            where_is()
        elif choice == "4":
            who_is()
        elif choice == "5":
            add_event()
        elif choice == "6":
            show_timeline()
        elif choice == "7":
            search_text()
        elif choice == "8":
            list_characters()
        elif choice == "9":
            print("\nBye bye, thanks for weaving lore with me\n")
            break
        else:
            print("\n invalid option, try again pls\n")

        # old version, delete later
        # if choice == "1":
        #     print("adding!")


def main():
    if len(sys.argv) > 1:
        first_arg = sys.argv[1].strip().lower()
        if first_arg in ["--help", "-h", "help"]:
            print_help_text()
            return
        else:
            print("Unknown argument, starting menu mode anyway...")

    run_menu_loop()


if __name__ == "__main__":
    main()
