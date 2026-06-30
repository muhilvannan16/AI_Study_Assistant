import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import random
from ai import (
    ask_ai,
    summarize_note,
    generate_flashcards,
    generate_quiz,
    create_study_plan
)

# ----------------------------
# File Handling
# ----------------------------

DATA_FILE = "notes.json"
dark_mode = False

def load_notes():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_notes(notes):
    with open(DATA_FILE, "w") as file:
        json.dump(notes, file, indent=4)

def choose_subject(title):

    if notes == {}:
        messagebox.showinfo(
            "No Subjects",
            "No subjects found."
        )
        return None

    window = tk.Toplevel(root)

    window.title(title)

    window.geometry("300x120")

    subject_var = tk.StringVar()

    subject_var.set(list(notes.keys())[0])

    tk.Label(
        window,
        text="Choose a Subject:"
    ).pack(pady=10)

    tk.OptionMenu(
        window,
        subject_var,
        *notes.keys()
    ).pack()

    result = {"subject": None}

    def confirm():

        result["subject"] = subject_var.get()

        window.destroy()

    tk.Button(
        window,
        text="OK",
        command=confirm
    ).pack(pady=10)

    window.grab_set()

    root.wait_window(window)

    return result["subject"]

notes = load_notes()

# ----------------------------
# Functions
# ----------------------------


def view_notes():
    notes_display.config(state="normal")
    notes_display.delete("1.0", tk.END)

    if notes == {}:
        notes_display.insert(tk.END, "No notes found.")
    else:
        for subject, subject_notes in notes.items():
            

            notes_display.insert(
                tk.END,
                f"{subject}\n"
            )

            notes_display.insert(
                tk.END,
                "-" * 25 + "\n"
            )
            
            status.config(text="Displaying notes.")
            for note in subject_notes:
                notes_display.insert(
                    tk.END,
                    f"• {note}\n"
                )

            notes_display.insert(
                tk.END,
                "\n"
            )

    notes_display.config(state="disabled")


def add_note():

    subject = simpledialog.askstring(
        "Subject",
        "Enter the subject:"
    )

    if not subject:
        return

    note = simpledialog.askstring(
        "Note",
        "Enter the note:"
    )

    if not note:
        return

    subject = subject.title()

    if subject not in notes:
        notes[subject] = []

    notes[subject].append(note)

    save_notes(notes)

    status.config(text="Added a new note.")
    
    messagebox.showinfo(
        "Success",
        "Note added successfully!"
    )

    view_notes()

def search_note():

    keyword = simpledialog.askstring(
        "Search Notes",
        "Enter a keyword:"
    )

    if not keyword:
        return

    keyword = keyword.lower()

    results = ""

    for subject, subject_notes in notes.items():

        for note in subject_notes:

            if keyword in note.lower():
                status.config(text="Search complete.")
                results += f"{subject}\n"
                results += f"• {note}\n\n"

    notes_display.config(state="normal")
    notes_display.delete("1.0", tk.END)

    if results == "":
        notes_display.insert(
            tk.END,
            "No matching notes found."
        )
    else:
        notes_display.insert(
            tk.END,
            results
        )

    notes_display.config(state="disabled")

def delete_note():

    subject = choose_subject("Delete Note")

    if subject is None:
        return

    if not subject:
        return

    subject = subject.title()

    if subject not in notes:

        messagebox.showerror(
            "Error",
            "Subject not found."
        )

        return

    note = simpledialog.askstring(
        "Delete Note",
        "Enter the exact note:"
    )

    if not note:
        return

    if note in notes[subject]:

        notes[subject].remove(note)

        if len(notes[subject]) == 0:

            del notes[subject]

        save_notes(notes)

        status.config(text="Note deleted.")
        
        messagebox.showinfo(
            "Success",
            "Note deleted successfully!"
        )

        view_notes()

    else:

        messagebox.showerror(
            "Error",
            "Note not found."
        )

def edit_note():

    subject = choose_subject("Edit Note")

    if subject is None:
        return

    if not subject:
        return

    subject = subject.title()

    if subject not in notes:

        messagebox.showerror(
            "Error",
            "Subject not found."
        )

        return

    old_note = simpledialog.askstring(
        "Edit Note",
        "Current note:"
    )

    if not old_note:
        return

    if old_note not in notes[subject]:

        messagebox.showerror(
            "Error",
            "Note not found."
        )

        return

    new_note = simpledialog.askstring(
        "Edit Note",
        "New note:"
    )

    if not new_note:
        return

    index = notes[subject].index(old_note)

    notes[subject][index] = new_note

    save_notes(notes)

    status.config(text="Note updated.")
    
    messagebox.showinfo(
        "Success",
        "Note updated successfully!"
    )

    view_notes()

def flashcards():

    if notes == {}:
        messagebox.showinfo(
            "Flashcards",
            "No notes found."
        )
        return

    flash_window = tk.Toplevel(root)
    flash_window.title("Flashcards")
    flash_window.geometry("600x400")
    flash_window.resizable(True, True)

    tk.Label(
        flash_window,
        text="Flashcards",
        font=("Helvetica", 18, "bold")
    ).pack(pady=10)

    subject_var = tk.StringVar()

    subjects = ["All"] + list(notes.keys())

    subject_var.set("All")

    tk.OptionMenu(
        flash_window,
        subject_var,
        *subjects
    ).pack()

    card_text = tk.Label(
        flash_window,
        text="Choose a subject\n\nThen press Next Card",
        font=("Arial",16,"bold"),
        wraplength=500,
        relief=tk.RIDGE,
        bd=3,
        width=35,
        height=8,
        justify="center"
    )

    card_text.pack(
        pady=40
    )

    def next_card():

        selected = subject_var.get()

        if selected == "All":
            current_subject = random.choice(list(notes.keys()))
        else:
            current_subject = selected

        note = random.choice(notes[current_subject])

        card_text.config(
            text=f"📚 {current_subject}\n\n{note}"
        )

    tk.Button(
        flash_window,
        text="Next Card",
        width=20,
        command=next_card
    ).pack()

    tk.Button(
        flash_window,
        text="Close",
        width=20,
        command=flash_window.destroy
    ).pack(pady=10)

def quiz_mode():

    if notes == {}:
        messagebox.showinfo(
            "Quiz Mode",
            "No notes found."
        )
        return

    quiz_window = tk.Toplevel(root)

    quiz_window.title("Quiz Mode")

    quiz_window.geometry("650x450")

    quiz_window.resizable(True, True)

    correct = 0
    review = 0

    current_subject = ""
    current_note = ""

    tk.Label(
        quiz_window,
        text="Quiz Mode",
        font=("Helvetica", 18, "bold")
    ).pack(pady=15)

    card = tk.Label(
        quiz_window,
        text="",
        font=("Arial", 14),
        wraplength=500,
        justify="center"
    )

    card.pack(pady=30)

    stats = tk.Label(
        quiz_window,
        text="Remembered: 0     Need Review: 0",
        font=("Arial", 12)
    )

    stats.pack(pady=10)

    def next_question():

        nonlocal current_subject
        nonlocal current_note

        current_subject = random.choice(list(notes.keys()))

        current_note = random.choice(notes[current_subject])

        card.config(
            text=f"📚 {current_subject}\n\n{current_note}"
        )

    def remembered():

        nonlocal correct

        correct += 1

        stats.config(
            text=f"Remembered: {correct}     Need Review: {review}"
        )

        next_question()

    def need_review():

        nonlocal review

        review += 1

        stats.config(
            text=f"Remembered: {correct}     Need Review: {review}"
        )

        next_question()

    tk.Button(
        quiz_window,
        text="I Remember",
        width=18,
        command=remembered
    ).pack(pady=5)

    tk.Button(
        quiz_window,
        text="Need Review",
        width=18,
        command=need_review
    ).pack(pady=5)

    tk.Button(
        quiz_window,
        text="Finish Quiz",
        width=18,
        command=lambda: finish()
    ).pack(pady=20)

    def finish():

        messagebox.showinfo(
            "Quiz Complete",
            f"Remembered: {correct}\nNeed Review: {review}"
        )

        quiz_window.destroy()

    next_question()
    
def clear_display():

    notes_display.config(state="normal")

    notes_display.delete("1.0", tk.END)

    notes_display.config(state="disabled")

    status.config(text="Display cleared.")
    
def about():

    messagebox.showinfo(
        "About",
        "AI Study Assistant\n\nCreated by Muhil Vannan\nVersion 1.0"
    )

def study_statistics():

    total_subjects = len(notes)

    total_notes = 0

    text = "Study Statistics\n\n"

    for subject, subject_notes in notes.items():

        count = len(subject_notes)

        total_notes += count

        text += f"{subject:<15}{count} notes\n"

    text += "\n"

    text += f"Subjects : {total_subjects}\n"

    text += f"Total Notes : {total_notes}"

    messagebox.showinfo(
        "Statistics",
        text
    )

def export_notes():

    if notes == {}:
        messagebox.showinfo(
            "Export",
            "No notes to export."
        )
        return

    with open("study_notes.txt", "w") as file:

        for subject, subject_notes in notes.items():

            file.write(subject + "\n")

            file.write("-" * 25 + "\n")

            for note in subject_notes:

                file.write("• " + note + "\n")

            file.write("\n")

    messagebox.showinfo(
        "Export Complete",
        "Notes exported to study_notes.txt"
    )

    status.config(text="Notes exported.")

def toggle_dark_mode():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        root.configure(bg="#2E2E2E")

        button_frame.configure(bg="#2E2E2E")

        title.configure(
            bg="#2E2E2E",
            fg="white"
        )

        notes_display.configure(
            bg="#1E1E1E",
            fg="white"
        )

        status.configure(
            bg="#2E2E2E",
            fg="white"
        )

    else:

        root.configure(bg="#f4f4f4")

        button_frame.configure(bg="#f4f4f4")

        title.configure(
            bg="#f4f4f4",
            fg="black"
        )

        notes_display.configure(
            bg="white",
            fg="black"
        )

        status.configure(
            bg="SystemButtonFace",
            fg="black"
        )

def ai_chat():

    ai_window = tk.Toplevel(root)
    ai_window.title("Ask AI")
    ai_window.geometry("700x550")
    ai_window.resizable(True, True)

    tk.Label(
        ai_window,
        text="🤖 AI Study Assistant",
        font=("Arial",18,"bold")
    ).pack(pady=10)

    tk.Label(
        ai_window,
        text="Ask any study question:"
    ).pack()

    question_entry = tk.Entry(
        ai_window,
        width=70,
        font=("Arial",12)
    )
    question_entry.pack(pady=10)

    response_box = tk.Text(
        ai_window,
        width=80,
        height=18,
        wrap="word"
    )
    response_box.pack(padx=10,pady=10)

    def ask():

        question = question_entry.get().strip()

        if question == "":
            messagebox.showwarning(
                "Warning",
                "Please enter a question."
            )
            return

        response_box.delete("1.0", tk.END)

        response_box.insert(
            tk.END,
            "Thinking...\n\n"
        )

        ai_window.update()

        answer = ask_ai(question)

        response_box.delete("1.0", tk.END)

        response_box.insert(
            tk.END,
            answer
        )

    tk.Button(
        ai_window,
        text="Ask AI",
        command=ask,
        width=20
    ).pack(pady=5)

    tk.Button(
        ai_window,
        text="Close",
        command=ai_window.destroy,
        width=20
    ).pack()

def ai_summarizer():

    if notes == {}:
        messagebox.showinfo(
            "No Notes",
            "There are no notes to summarize."
        )
        return

    summary_window = tk.Toplevel(root)

    summary_window.title("AI Note Summarizer")

    summary_window.geometry("750x650")

    summary_window.resizable(True, True)

    # -------------------------------
    # Subject Dropdown
    # -------------------------------

    tk.Label(
        summary_window,
        text="Choose Subject",
        font=("Arial", 12, "bold")
    ).pack(pady=(15,5))

    subject_var = tk.StringVar()

    subjects = list(notes.keys())

    subject_var.set(subjects[0])

    tk.OptionMenu(
        summary_window,
        subject_var,
        *subjects
    ).pack()

    # -------------------------------
    # Note List
    # -------------------------------

    tk.Label(
        summary_window,
        text="Choose a Note",
        font=("Arial",12,"bold")
    ).pack(pady=(20,5))

    note_list = tk.Listbox(
        summary_window,
        width=85,
        height=8,
        font=("Consolas",11)
    )

    note_list.pack(pady=5)

    # -------------------------------
    # Summary Display
    # -------------------------------

    tk.Label(
        summary_window,
        text="AI Summary",
        font=("Arial",12,"bold")
    ).pack(pady=(20,5))

    summary_box = tk.Text(
        summary_window,
        width=85,
        height=12,
        wrap="word",
        font=("Consolas",11)
    )

    summary_box.pack(pady=5)

    # -------------------------------
    # Load Notes
    # -------------------------------

    def load_notes():

        note_list.delete(0, tk.END)

        subject = subject_var.get()

        for note in notes[subject]:

            note_list.insert(
                tk.END,
                note
            )

    load_notes()

    subject_var.trace_add(
        "write",
        lambda *args: load_notes()
    )

    # -------------------------------
    # Summarize Selected Note
    # -------------------------------

    def summarize_selected_note():

        selection = note_list.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a note first."
            )

            return

        note = note_list.get(selection[0])

        summary_box.delete("1.0", tk.END)

        summary_box.insert(
            tk.END,
            "Summarizing...\n\n"
        )

        summary_window.update()

        summary = summarize_note(note)

        summary_box.delete("1.0", tk.END)

        summary_box.insert(
            tk.END,
            summary
        )

    # -------------------------------
    # Summarize Button
    # -------------------------------

    tk.Button(
        summary_window,
        text="✨ Summarize",
        width=20,
        bg="#4CAF50",
        fg="white",
        command=summarize_selected_note
    ).pack(pady=15)

def ai_flashcards():

    if notes == {}:
        messagebox.showinfo(
            "No Notes",
            "There are no notes available."
        )
        return

    flash_window = tk.Toplevel(root)

    flash_window.title("AI Flashcard Generator")

    flash_window.geometry("750x650")

    flash_window.resizable(True, True)

    # -------------------------------
    # Subject
    # -------------------------------

    tk.Label(
        flash_window,
        text="Choose Subject",
        font=("Arial",12,"bold")
    ).pack(pady=(15,5))

    subject_var = tk.StringVar()

    subjects = list(notes.keys())

    subject_var.set(subjects[0])

    tk.OptionMenu(
        flash_window,
        subject_var,
        *subjects
    ).pack()

    # -------------------------------
    # Note List
    # -------------------------------

    tk.Label(
        flash_window,
        text="Choose a Note",
        font=("Arial",12,"bold")
    ).pack(pady=(20,5))

    note_list = tk.Listbox(
        flash_window,
        width=85,
        height=8,
        font=("Consolas",11)
    )

    note_list.pack()

    # -------------------------------
    # AI Flashcards Display
    # -------------------------------

    tk.Label(
        flash_window,
        text="Generated Flashcards",
        font=("Arial",12,"bold")
    ).pack(pady=(20,5))

    flashcard_box = tk.Text(
        flash_window,
        width=85,
        height=12,
        wrap="word",
        font=("Consolas",11)
    )

    flashcard_box.pack()

    # -------------------------------
    # Load Notes
    # -------------------------------

    def load_notes():

        note_list.delete(0, tk.END)

        subject = subject_var.get()

        for note in notes[subject]:

            note_list.insert(
                tk.END,
                note
            )

    load_notes()

    subject_var.trace_add(
        "write",
        lambda *args: load_notes()
    )

    # -------------------------------
    # Generate Flashcards
    # -------------------------------

    def create_flashcards():

        selection = note_list.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a note first."
            )

            return

        note = note_list.get(selection[0])

        flashcard_box.delete("1.0", tk.END)

        flashcard_box.insert(
            tk.END,
            "Generating flashcards..."
        )

        flash_window.update()

        cards = generate_flashcards(note)

        flashcard_box.delete("1.0", tk.END)

        flashcard_box.insert(
            tk.END,
            cards
        )

    # -------------------------------
    # Button
    # -------------------------------

    tk.Button(
        flash_window,
        text="📚 Generate Flashcards",
        bg="#4CAF50",
        fg="white",
        width=24,
        command=create_flashcards
    ).pack(pady=15)

def ai_quiz():

    if notes == {}:
        messagebox.showinfo(
            "No Notes",
            "There are no notes available."
        )
        return

    quiz_window = tk.Toplevel(root)

    quiz_window.title("AI Quiz Generator")

    quiz_window.geometry("750x650")

    quiz_window.resizable(True, True)

    # -------------------------------
    # Subject
    # -------------------------------

    tk.Label(
        quiz_window,
        text="Choose Subject",
        font=("Arial",12,"bold")
    ).pack(pady=(15,5))

    subject_var = tk.StringVar()

    subjects = list(notes.keys())

    subject_var.set(subjects[0])

    tk.OptionMenu(
        quiz_window,
        subject_var,
        *subjects
    ).pack()

    # -------------------------------
    # Note List
    # -------------------------------

    tk.Label(
        quiz_window,
        text="Choose a Note",
        font=("Arial",12,"bold")
    ).pack(pady=(20,5))

    note_list = tk.Listbox(
        quiz_window,
        width=85,
        height=8,
        font=("Consolas",11)
    )

    note_list.pack()

    # -------------------------------
    # Quiz Display
    # -------------------------------

    tk.Label(
        quiz_window,
        text="Generated Quiz",
        font=("Arial",12,"bold")
    ).pack(pady=(20,5))

    # -------------------------------
    # Quiz Display Frame
    # -------------------------------

    quiz_frame = tk.Frame(quiz_window)

    quiz_frame.pack(pady=5)

    quiz_scrollbar = tk.Scrollbar(quiz_frame)

    quiz_scrollbar.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )

    quiz_box = tk.Text(
        quiz_frame,
        width=85,
        height=12,
        wrap="word",
        font=("Consolas",11),
        yscrollcommand=quiz_scrollbar.set
    )

    quiz_box.pack(
        side=tk.LEFT
    )

    quiz_scrollbar.config(
        command=quiz_box.yview
    )

    # -------------------------------
    # Load Notes
    # -------------------------------

    def load_notes():

        note_list.delete(0, tk.END)

        subject = subject_var.get()

        for note in notes[subject]:

            note_list.insert(
                tk.END,
                note
            )

    load_notes()

    subject_var.trace_add(
        "write",
        lambda *args: load_notes()
    )

    # -------------------------------
    # Generate Quiz
    # -------------------------------

    def create_quiz():

        selection = note_list.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a note first."
            )

            return

        note = note_list.get(selection[0])

        quiz_box.delete("1.0", tk.END)

        quiz_box.insert(
            tk.END,
            "🤖 AI is generating your quiz...\n\nPlease wait..."
        )

        generate_button.config(
            state="disabled",
            text="Generating..."
        )

        quiz_window.update()

        quiz = generate_quiz(note)

        quiz_box.delete("1.0", tk.END)

        quiz_box.insert(
            tk.END,
            quiz
        )
        generate_button.config(
            state="normal",
            text="🧠 Generate Quiz"
        )

    # -------------------------------
    # Generate Button
    # -------------------------------

    generate_button = tk.Button(
        quiz_window,
        text="🧠 Generate Quiz",
        bg="#4CAF50",
        fg="white",
        width=24,
        command=create_quiz
    )

    generate_button.pack(pady=15)

def ai_study_planner():

    planner_window = tk.Toplevel(root)

    planner_window.title("AI Study Planner")

    planner_window.geometry("750x650")

    planner_window.resizable(True, True)

    # -------------------------------
    # Title
    # -------------------------------

    tk.Label(
        planner_window,
        text="📅 AI Study Planner",
        font=("Arial",18,"bold")
    ).pack(pady=15)

    # -------------------------------
    # Subject
    # -------------------------------

    tk.Label(
        planner_window,
        text="Subject",
        font=("Arial",12,"bold")
    ).pack()

    subject_entry = tk.Entry(
        planner_window,
        width=40,
        font=("Arial",12)
    )

    subject_entry.pack(pady=10)

    # -------------------------------
    # Days
    # -------------------------------

    tk.Label(
        planner_window,
        text="Days Until Exam",
        font=("Arial",12,"bold")
    ).pack()

    days_entry = tk.Entry(
        planner_window,
        width=15,
        font=("Arial",12)
    )

    days_entry.pack(pady=10)

    # -------------------------------
    # Output
    # -------------------------------

    tk.Label(
        planner_window,
        text="Study Plan",
        font=("Arial",12,"bold")
    ).pack(pady=(20,5))

    frame = tk.Frame(planner_window)

    frame.pack()

    scrollbar = tk.Scrollbar(frame)

    scrollbar.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )

    plan_box = tk.Text(
        frame,
        width=85,
        height=16,
        wrap="word",
        font=("Consolas",11),
        yscrollcommand=scrollbar.set
    )

    plan_box.pack(
        side=tk.LEFT
    )

    scrollbar.config(
        command=plan_box.yview
    )

    # -------------------------------
    # Generate
    # -------------------------------

    def generate_plan():

        subject = subject_entry.get().strip()

        days = days_entry.get().strip()

        if subject == "" or days == "":

            messagebox.showwarning(
                "Missing Information",
                "Please fill in every field."
            )

            return

        if not days.isdigit():

            messagebox.showwarning(
                "Invalid Days",
                "Days must be a number."
            )

            return

        plan_box.delete(
            "1.0",
            tk.END
        )

        plan_box.insert(
            tk.END,
            "📅 Creating your study plan...\n\n"
        )

        planner_window.update()

        plan = create_study_plan(
            subject,
            int(days)
        )

        plan_box.delete(
            "1.0",
            tk.END
        )

        plan_box.insert(
            tk.END,
            plan
        )

    generate_button = tk.Button(
        planner_window,
        text="📅 Generate Study Plan",
        width=25,
        bg="#4CAF50",
        fg="white",
        command=generate_plan
    )

    generate_button.pack(pady=20)
# ----------------------------
# GUI
# ----------------------------

root = tk.Tk()

root.title("AI Study Assistant")

root.geometry("850x650")

root.configure(bg="#f4f4f4")

root.resizable(True, True)

# ----------------------------
# Title
# ----------------------------

title = tk.Label(
    root,
    text="AI Study Assistant",
    font=("Helvetica", 24, "bold"),
    bg="#f4f4f4"
)

title.pack(pady=20)

# ----------------------------
# Button Frame
# ----------------------------

button_frame = tk.Frame(
    root,
    bg="#f4f4f4"
)

button_frame.pack()

# ----------------------------
# Buttons
# ----------------------------

add_button = tk.Button(
    button_frame,
    text="➕ Add Note",
    width=18,
    height=2,
    bg="#4CAF50",
    fg="white",
    command=add_note
)

add_button.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

view_button = tk.Button(
    button_frame,
    text="📖 View Notes",
    width=18,
    height=2,
    bg="#2196F3",
    fg="white",
    command=view_notes
)

view_button.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)

search_button = tk.Button(
    button_frame,
    text="🔍 Search",
    width=18,
    height=2,
    bg="#9C27B0",
    fg="white",
    command=search_note
)

search_button.grid(
    row=0,
    column=2,
    padx=10,
    pady=10
)

delete_button = tk.Button(
    button_frame,
    text="🗑 Delete",
    width=18,
    height=2,
    bg="#F44336",
    fg="white",
    command=delete_note
)

delete_button.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

edit_button = tk.Button(
    button_frame,
    text="✏ Edit",
    width=18,
    height=2,
    bg="#FF9800",
    fg="white",
    command=edit_note
)

edit_button.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)

flash_button = tk.Button(
    button_frame,
    text="📚 Flashcards",
    width=18,
    height=2,
    bg="#009688",
    fg="white",
    command=flashcards
)

flash_button.grid(
    row=1,
    column=2,
    padx=10,
    pady=10
)

quiz_button = tk.Button(
    button_frame,
    text="📝 Practice Quiz",
    width=18,
    height=2,
    bg="#3F51B5",
    fg="white",
    command=quiz_mode
)

quiz_button.grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)

clear_button = tk.Button(
    button_frame,
    text="Clear Display",
    width=18,
    height=2,
    command=clear_display
)

clear_button.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)

about_button = tk.Button(
    button_frame,
    text="ℹ About",
    width=18,
    height=2,
    command=about
)

about_button.grid(
    row=2,
    column=2,
    padx=10,
    pady=10
)

stats_button = tk.Button(
    button_frame,
    text="📊 Statistics",
    width=18,
    height=2,
    command=study_statistics
)

stats_button.grid(
    row=3,
    column=0,
    padx=10,
    pady=10
)

export_button = tk.Button(
    button_frame,
    text="📄 Export",
    width=18,
    height=2,
    command=export_notes
)

export_button.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)

dark_button = tk.Button(
    button_frame,
    text="🌙 Dark Mode",
    width=18,
    height=2,
    command=toggle_dark_mode
)

dark_button.grid(
    row=3,
    column=2,
    padx=10,
    pady=10
)

ai_button = tk.Button(
    button_frame,
    text="🤖 Ask AI",
    width=18,
    command=ai_chat
)

ai_button.grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)

tk.Button(
    button_frame,
    text="✨ Summarize Note",
    width=18,
    command=ai_summarizer
).grid(row=4, column=0, padx=10, pady=10)

tk.Button(
    button_frame,
    text="📚 AI Flashcards",
    width=18,
    command=ai_flashcards
).grid(
    row=5,
    column=0,
    padx=10,
    pady=10
)

tk.Button(
    button_frame,
    text="🧠 AI Quiz",
    width=18,
    command=ai_quiz
).grid(
    row=6,
    column=0,
    padx=10,
    pady=10
)

tk.Button(
    button_frame,
    text="📅 Study Planner",
    width=18,
    command=ai_study_planner
).grid(
    row=7,
    column=0,
    padx=10,
    pady=10
)
# ----------------------------
# Notes Display
# ----------------------------

display_frame = tk.Frame(root)

display_frame.pack(pady=20)

scrollbar = tk.Scrollbar(display_frame)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

notes_display = tk.Text(
    display_frame,
    width=85,
    height=24,
    font=("Consolas", 11),
    yscrollcommand=scrollbar.set
)

notes_display.pack()

scrollbar.config(command=notes_display.yview)

notes_display.config(state="disabled")

# ----------------------------
# Status Bar
# ----------------------------

status = tk.Label(
    root,
    text="Ready",
    bd=1,
    relief=tk.SUNKEN,
    anchor=tk.W
)

status.pack(side=tk.BOTTOM, fill=tk.X)

# ----------------------------
# Load Existing Notes
# ----------------------------

view_notes()

# ----------------------------
# Run Program
# ----------------------------

def close_program():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()

root.protocol(
    "WM_DELETE_WINDOW",
    close_program
)

root.mainloop()
