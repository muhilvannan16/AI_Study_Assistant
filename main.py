import json
# Used for saving and loading data.
DATA_FILE = "notes.json"
# Loads the data in console.
def load_notes():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Saves data as a file.
def save_notes(notes):
    with open(DATA_FILE, "w") as file:
        json.dump(notes, file, indent=4)

# Used to add note.
def add_note():
    subject = input("Subject: ").title()
    note = input("Note: ")

    if subject not in notes:
        notes[subject] = []
    notes[subject].append(note)

    save_notes(notes)
    print("Note added!")
    print("Notes saved!")

# Used to view the notes from the notes.json file
def view_notes():
    if notes == {}:
        print("No notes found.")
    else:
        for subject, subject_notes in notes.items():
            print(f"{subject}")
            for subject_notes in notes[subject]:
                print(f"  - {subject_notes}")
            print("-----------------")

# Shows the menu with options to choose from.    
def menu():
    while True:
        print("\n---- AI Study Assistant-----")
        print("1. Add note")
        print("2. View notes")
        print("3. Exit")

        choice = input("Choose your option(1-3): ")

        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            print("Thanks for studying with me!")
            break
        else:
            print("Invalid option! Try again")
        print("-----")
notes = load_notes()
menu()
