import json
import random
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
            
# Used to search for specific notes of user's choice.
def search_notes():
    # Asks user for keyword.
    keyword = input("Enter a keyword to search: ")
    found = False
    # Loop through every subject.
    for subject, subject_notes in notes.items():
        # Loop through every notes of subject.
        for note in subject_notes:
            # Checks if keyword is in note.
            if keyword.lower() in note.lower():
                
                if not found:
                    print("Found!")
                    print()

                print(subject)
                print(f"  - {note}")

                found = True
                
    if not found:
        print("No matching notes found.")
# Used to delete note.
def delete_note():
    subject = input("Subject: ").title()
    note = input("Note: ")

    if subject in notes:
        if note in notes[subject]:
            notes[subject].remove(note)
            print("Note removed.")
        else:
            print("Note not found.")
        if notes[subject] == []:
            del notes[subject]
            print("Subject was removed due to lack of notes in it.")
    else:
        print("Subject not found.")

    save_notes(notes)
# Creates flashcards to study using notes.
def flashcards():
    if notes == {}:
        print("No notes found.")
        return

    subject = input("Study which subject? (or type 'all'): ").title()

    if subject != "All" and subject not in notes:
        print("Subject not found!")
        return

    while True:

        if subject == "All":
            current_subject = random.choice(list(notes.keys()))
        else:
            current_subject = subject

        note = random.choice(notes[current_subject])

        print(f"\n📚 Subject: {current_subject}")
        print("----------------------")
        print("Study this:")
        print(note)

        input("\nPress Enter to continue...")

        again = input("\nAnother flashcard? (y/n): ").lower()

        if again != "y":
            break

        print("----------------------")
# Uses the notes to create a quiz.
def quiz_mode():
    if notes == {}:
        print("No notes found.")
        return
    
    correct = 0
    review = 0
    
    while True:
        subject = random.choice(list(notes.keys()))
        note = random.choice(notes[subject])

        print(f"\nSubject: {subject}")
        print("Study this!")
        print(note)

        answer = input("Do you remeber this ? (y(for yes) / n(for no)): ").lower()

        if answer == "y":
            print("Nice!")
            correct += 1
        else:
            print("Review this later.")
            review += 1
        print()
        again = input("Another flashcard ? (y (for yes) / n (for no)): ").lower()
        if again != "y":
            break
        print("------")

    print("\nQuiz Complete!")
    print(f"Remembered: {correct}")
    print(f"Need Review: {review}")

def edit_note():
    subject = input("Subject: ").title()
    old_note = input("Current note: ")
    new_note = input("New note: ")

    if subject in notes:
        if old_note in notes[subject]:
            index = notes[subject].index(old_note)
            notes[subject][index] = new_note

            save_notes(notes)
            print("Notes updated!")
        else:
            print("Note not found.")
    else:
        print("Subject not found.")

# Shows the menu with options to choose from.    
def menu():
    while True:
        print("\n---- AI Study Assistant-----")
        print("1. Add note")
        print("2. View notes")
        print("3. Search Notes")
        print("4. Delete Note")
        print("5. Flashcards")
        print("6. Quiz mode")
        print("7. Edit note")
        print("8. Exit")

        choice = input("Choose your option(1-8): ")
        print()
        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            search_notes()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            flashcards()
        elif choice == "6":
            quiz_mode()
        elif choice == "7":
            edit_note()
        elif choice == "8":
            print("Thanks for studying with me!")
            break
        else:
            print("Invalid option! Try again")
        print("-----")

notes = load_notes()
menu()
