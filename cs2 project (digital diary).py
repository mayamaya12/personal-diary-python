import tkinter as tk
from tkinter import messagebox
import hashlib
from tkinter import ttk
import json
from datetime import datetime

# Function to hash the password (to store it securely)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify the entered password
def verify_password():
    entered_password = password_entry.get()
    if hash_password(entered_password) == correct_password:
        password_window.destroy()  # Close the password window
        main_window.deiconify()  # Show the main window
    else:
        messagebox.showerror("Error", "Incorrect password. Please try again.")

# Save diary entry function
def save_entry():
    content = entry_box.get("1.0", tk.END).strip()
    mood = mood_var.get()

    if content and content != "Write your thoughts here :)":
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": mood,
            "content": content,
        }

        try:
            with open("diary_entries.json", "r") as file:
                entries = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            entries = []

        entries.append(entry)

        try:
            with open("diary_entries.json", "w") as file:
                json.dump(entries, file, indent=4)
            messagebox.showinfo("Success", "Your entry has been saved!")
            entry_box.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save your entry. Error: {str(e)}")
    else:
        messagebox.showwarning("Warning", "Please write something before saving.")

# View entries function
def view_entries():
    try:
        with open("diary_entries.json", "r") as file:
            entries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        entries = []

    if not entries:
        entries_text = "No entries found."
    else:
        entries_text = "\n".join(
            [f"Date: {entry['date']}\nMood: {entry['mood']}\n{entry['content']}\n{'-' * 50}" for entry in entries]
        )

    view_window = tk.Toplevel(main_window)
    view_window.title("View Entries")
    view_window.geometry("500x400")
    view_window.configure(bg="#e6f7ff")

    entries_label = tk.Label(view_window, text="Saved Entries", font=("Comic Sans MS", 16), bg="#e6f7ff", fg="#006d77")
    entries_label.pack(pady=10)

    entries_textbox = tk.Text(view_window, font=("Comic Sans MS", 12), wrap=tk.WORD, bd=2, padx=10, pady=10, bg="#ffffff",
                              fg="#264653", relief="flat")
    entries_textbox.insert("1.0", entries_text)
    entries_textbox.configure(state="disabled")
    entries_textbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Delete entry function
def delete_entry():
    def delete_selected():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select an entry to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
        if confirm:
            index = selected_index[0]

            # Remove the entry from the JSON file
            try:
                with open("diary_entries.json", "r") as file:
                    entries = json.load(file)

                if index < len(entries):
                    deleted_entry = entries.pop(index)

                    # Save the updated entries back to the file
                    with open("diary_entries.json", "w") as file:
                        json.dump(entries, file, indent=4)

                    messagebox.showinfo("Success", f"Deleted entry:\nDate: {deleted_entry['date']}\nMood: {deleted_entry['mood']}")
                    listbox.delete(index)  # Remove from the Listbox
                else:
                    messagebox.showerror("Error", "Entry index out of range.")
            except FileNotFoundError:
                messagebox.showinfo("No Entries", "No entries found to delete.")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Error reading entries from the file.")

    # Load the entries into the listbox
    try:
        with open("diary_entries.json", "r") as file:
            entries = json.load(file)

        if not entries:
            messagebox.showinfo("No Entries", "No entries found to delete.")
            return
    except FileNotFoundError:
        messagebox.showinfo("No Entries", "No entries found to delete.")
        return

    # Create a window for displaying and deleting entries
    delete_window = tk.Toplevel(main_window)
    delete_window.title("Delete Entry")
    delete_window.geometry("500x400")
    delete_window.configure(bg="#e6f7ff")

    tk.Label(delete_window, text="Select an Entry to Delete", font=("Comic Sans MS", 16), bg="#e6f7ff",
             fg="#006d77").pack(pady=10)

    listbox = tk.Listbox(delete_window, font=("Comic Sans MS", 12), bg="#ffffff", fg="#264653", width=50, height=15, relief="flat")
    listbox.pack(pady=10, padx=10)

    # Add entries to the listbox
    for entry in entries:
        listbox.insert(tk.END, f"{entry['date']} - {entry['mood']}")

    delete_button = tk.Button(
        delete_window,
        text="Delete Selected Entry",
        font=("Comic Sans MS", 12),
        bg="#ff6f61",
        fg="white",
        activebackground="#e63946",
        activeforeground="white",
        command=delete_selected,
        relief="flat",
        bd=0,
    )
    delete_button.pack(pady=10)  # Ensure the button is packed


# Search function
def search_entries():
    def perform_search():
        keyword = search_entry.get().strip().lower()
        results = []

        for entry in entries:
            if keyword in entry["content"].lower() or keyword in entry["mood"].lower() or keyword in entry["date"]:
                results.append(entry)

        if not results:
            search_results_text = "No entries match your search."
        else:
            search_results_text = "\n".join(
                [f"Date: {entry['date']}\nMood: {entry['mood']}\n{entry['content']}\n{'-' * 50}" for entry in results]
            )

        search_results_box.configure(state="normal")
        search_results_box.delete("1.0", tk.END)
        search_results_box.insert("1.0", search_results_text)
        search_results_box.configure(state="disabled")

    try:
        with open("diary_entries.json", "r") as file:
            entries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        entries = []

    search_window = tk.Toplevel(main_window)
    search_window.title("Search Entries")
    search_window.geometry("500x400")
    search_window.configure(bg="#e6f7ff")

    tk.Label(search_window, text="Search Entries", font=("Comic Sans MS", 16), bg="#e6f7ff", fg="#006d77").pack(pady=10)

    search_entry = tk.Entry(search_window, font=("Comic Sans MS", 14), bg="#ffffff", fg="#264653", relief="flat")
    search_entry.pack(pady=10)

    search_button = tk.Button(
        search_window,
        text="Search",
        font=("Comic Sans MS", 12),
        bg="#87cefa",
        fg="#264653",
        activebackground="#4682b4",
        activeforeground="#fff",
        command=perform_search,
        relief="flat",
        bd=0,
    )
    search_button.pack(pady=5)

    search_results_box = tk.Text(search_window, font=("Comic Sans MS", 12), wrap=tk.WORD, bd=2, padx=10, pady=10, bg="#ffffff",
                                 fg="#264653", relief="flat")
    search_results_box.configure(state="disabled")
    search_results_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Utility function
def clear_placeholder(event):
    if entry_box.get("1.0", tk.END).strip() == "Write your thoughts here :)":
        entry_box.delete("1.0", tk.END)

# Exit application function
def exit_app():
    main_window.destroy()

# Initialize password
correct_password = hash_password("password")

# Main application window
main_window = tk.Tk()
main_window.geometry("600x600")
main_window.configure(bg="#e6f7ff")
main_window.title("Personal Diary")
main_window.withdraw()

# Mood tracker
mood_var = tk.StringVar(value="Neutral")
mood_label = tk.Label(main_window, text="Select Mood:", font=("Comic Sans MS", 14), bg="#e6f7ff", fg="#006d77")
mood_label.pack()
mood_menu = ttk.Combobox(main_window, textvariable=mood_var, values=["Happy", "Sad", "Excited", "Anxious", "Neutral"],
                         font=("Comic Sans MS", 12), state="readonly")
mood_menu.pack(pady=5)

# Entry box
entry_box = tk.Text(main_window, font=("Comic Sans MS", 14), bd=2, wrap=tk.WORD, bg="#ffffff", fg="#264653", height=15,
                    relief="flat")
entry_box.insert("1.0", "Write your thoughts here :)")
entry_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
entry_box.bind("<FocusIn>", clear_placeholder)

# Buttons
button_frame = tk.Frame(main_window, bg="#e6f7ff")
button_frame.pack(pady=10, fill=tk.X)

save_button = tk.Button(button_frame, text="Save Entry", font=("Comic Sans MS", 14), bg="#87cefa", fg="#264653",
                        activebackground="#4682b4", activeforeground="#fff", command=save_entry, relief="flat", bd=0)
save_button.pack(side=tk.LEFT, padx=5)

view_button = tk.Button(button_frame, text="View Entries", font=("Comic Sans MS", 14), bg="#87cefa", fg="#264653",
                        activebackground="#4682b4", activeforeground="#fff", command=view_entries, relief="flat", bd=0)
view_button.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(button_frame, text="Search Entries", font=("Comic Sans MS", 14), bg="#87cefa", fg="#264653",
                          activebackground="#4682b4", activeforeground="#fff", command=search_entries, relief="flat", bd=0)
search_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete Entry", font=("Comic Sans MS", 14), bg="#ff6f61", fg="#fff",
                          activebackground="#e63946", activeforeground="#fff", command=delete_entry, relief="flat", bd=0)
delete_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(button_frame, text="Exit", font=("Comic Sans MS", 14), bg="#ff6f61", fg="#fff",
                        activebackground="#e63946", activeforeground="#fff", command=exit_app, relief="flat", bd=0)
exit_button.pack(side=tk.LEFT, padx=5)

# Password window
password_window = tk.Tk()
password_window.geometry("400x200")
password_window.configure(bg="#e6f7ff")
password_window.title("Enter Password")

password_label = tk.Label(password_window, text="Enter Password", font=("Comic Sans MS", 16), bg="#e6f7ff", fg="#006d77")
password_label.pack(pady=20)

password_entry = tk.Entry(password_window, font=("Comic Sans MS", 14), show="*", bg="#ffffff", fg="#264653", relief="flat")
password_entry.pack(pady=10)

submit_button = tk.Button(password_window, text="Submit", font=("Comic Sans MS", 14), bg="#87cefa", fg="#264653",
                          activebackground="#4682b4", activeforeground="#fff", command=verify_password, relief="flat", bd=0)
submit_button.pack(pady=10)

password_window.mainloop()
