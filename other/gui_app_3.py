import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime, timedelta

class Contact:
    def __init__(self, name, phone, email, group=None, birthday=None, favorite=False):
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group
        self.birthday = birthday
        self.favorite = favorite


class Node:
    def __init__(self, contact):
        self.contact = contact
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.deleted_contact = None

    def add_contact(self, name, phone, email, group, birthday):
        new_contact = Contact(name, phone, email, group, birthday)
        if self.root is None:
            self.root = Node(new_contact)
        else:
            self._insert(self.root, new_contact)

    def _insert(self, node, new_contact):
        if new_contact.name < node.contact.name:
            if node.left is None:
                node.left = Node(new_contact)
            else:
                self._insert(node.left, new_contact)
        else:
            if node.right is None:
                node.right = Node(new_contact)
            else:
                self._insert(node.right, new_contact)

    def find_contact(self, query):
        return self._find(self.root, query)

    def _find(self, node, query):
        if node is None:
            return None
        if query in (node.contact.name, node.contact.phone, node.contact.email):
            return node.contact
        left_result = self._find(node.left, query)
        return left_result if left_result else self._find(node.right, query)

    def delete_contact(self, name):
        self.deleted_contact = self.find_contact(name)
        if self.deleted_contact:
            self.root = self._delete(self.root, name)

    def _delete(self, node, name):
        if node is None:
            return node
        if name < node.contact.name:
            node.left = self._delete(node.left, name)
        elif name > node.contact.name:
            node.right = self._delete(node.right, name)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.contact = temp.contact
            node.right = self._delete(node.right, temp.contact.name)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def update_contact(self, name, new_phone=None, new_email=None):
        contact = self.find_contact(name)
        if contact:
            if new_phone:
                contact.phone = new_phone
            if new_email:
                contact.email = new_email

    def toggle_favorite(self, name):
        contact = self.find_contact(name)
        if contact:
            contact.favorite = not contact.favorite

    def list_contacts(self, node, contacts):
        if node:
            self.list_contacts(node.left, contacts)
            contacts.append(f"{node.contact.name} - {node.contact.phone} - {node.contact.email}")
            self.list_contacts(node.right, contacts)
        return contacts

    def list_favorite_contacts(self, node, favorites):
        if node:
            self.list_favorite_contacts(node.left, favorites)
            if node.contact.favorite:
                favorites.append(f"{node.contact.name} - {node.contact.phone} - {node.contact.email}")
            self.list_favorite_contacts(node.right, favorites)
        return favorites

    def export_contacts_to_csv(self, file_name):
        contacts = self.list_contacts(self.root, [])
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email", "Group", "Birthday"])
            for contact in contacts:
                writer.writerow(contact.split(" - "))

    def import_contacts_from_csv(self, file_name):
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_contact(row['Name'], row['Phone'], row['Email'], row.get('Group', ''), row.get('Birthday', ''))

    def list_upcoming_birthdays(self, node, birthdays, days_ahead):
        today = datetime.now()
        upcoming_date = today + timedelta(days=days_ahead)
        if node:
            self.list_upcoming_birthdays(node.left, birthdays, days_ahead)
            if node.contact.birthday:
                birthday_date = datetime.strptime(node.contact.birthday, "%Y-%m-%d")
                birthday_this_year = birthday_date.replace(year=today.year)
                if today <= birthday_this_year <= upcoming_date:
                    birthdays.append(f"{node.contact.name} - {birthday_date.strftime('%Y-%m-%d')}")
            self.list_upcoming_birthdays(node.right, birthdays, days_ahead)
        return birthdays

    def undo_delete(self):
        if self.deleted_contact:
            self.add_contact(self.deleted_contact.name, self.deleted_contact.phone,
                             self.deleted_contact.email, self.deleted_contact.group,
                             self.deleted_contact.birthday)


class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.contact_book = BinarySearchTree()

        # Styling
        self.style = {
            "font": ("Arial", 12),
            "bg": "#f0f0f0",
            "fg": "#333",
            "highlightbackground": "#aaa",
            "highlightcolor": "#555",
            "padx": 10,
            "pady": 10
        }

        # Output Text Area
        self.output_text = tk.Text(self.root, wrap=tk.WORD, height=15, width=50, bg="#ffffff", fg="#000000")
        self.output_text.pack(pady=10)

        # Buttons
        self.button_frame = tk.Frame(self.root, bg=self.style["bg"])
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Contact", command=self.add_contact_window, **self.style)
        self.add_button.grid(row=0, column=0, padx=5)

        self.find_button = tk.Button(self.button_frame, text="Find Contact", command=self.find_contact_window, **self.style)
        self.find_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact_window, **self.style)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Update Contact", command=self.update_contact_window, **self.style)
        self.update_button.grid(row=0, column=3, padx=5)

        self.toggle_favorite_button = tk.Button(self.button_frame, text="Toggle Favorite", command=self.toggle_favorite_window, **self.style)
        self.toggle_favorite_button.grid(row=0, column=4, padx=5)

        self.list_favorites_button = tk.Button(self.button_frame, text="List Favorite Contacts", command=self.list_favorite_contacts, **self.style)
        self.list_favorites_button.grid(row=0, column=5, padx=5)

        self.list_contacts_button = tk.Button(self.button_frame, text="List All Contacts", command=self.list_contacts, **self.style)
        self.list_contacts_button.grid(row=0, column=6, padx=5)

        self.export_button = tk.Button(self.button_frame, text="Export to CSV", command=self.export_contacts, **self.style)
        self.export_button.grid(row=0, column=7, padx=5)

        self.import_button = tk.Button(self.button_frame, text="Import from CSV", command=self.import_contacts, **self.style)
        self.import_button.grid(row=0, column=8, padx=5)

        self.list_birthdays_button = tk.Button(self.button_frame, text="List Upcoming Birthdays", command=self.list_upcoming_birthdays_window, **self.style)
        self.list_birthdays_button.grid(row=0, column=9, padx=5)

        self.undo_button = tk.Button(self.button_frame, text="Undo Delete", command=self.undo_delete, **self.style)
        self.undo_button.grid(row=0, column=10, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.root.quit, **self.style)
        self.exit_button.grid(row=0, column=11, padx=5)

    def add_contact_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add Contact")
        AddContactWindow(self.new_window, self.contact_book)

    def find_contact_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Find Contact")
        FindContactWindow(self.new_window, self.contact_book, self.output_text)

    def delete_contact_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Delete Contact")
        DeleteContactWindow(self.new_window, self.contact_book)

    def update_contact_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Update Contact")
        UpdateContactWindow(self.new_window, self.contact_book)

    def toggle_favorite_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Toggle Favorite")
        ToggleFavoriteWindow(self.new_window, self.contact_book)

    def list_contacts(self):
        contacts = self.contact_book.list_contacts(self.contact_book.root, [])
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "\n".join(contacts) if contacts else "No contacts found.")

    def list_favorite_contacts(self):
        favorites = self.contact_book.list_favorite_contacts(self.contact_book.root, [])
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "\n".join(favorites) if favorites else "No favorite contacts found.")

    def export_contacts(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".csv",
                                                   filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_name:
            self.contact_book.export_contacts_to_csv(file_name)
            messagebox.showinfo("Success", "Contacts exported successfully!")

    def import_contacts(self):
        file_name = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_name:
            self.contact_book.import_contacts_from_csv(file_name)
            messagebox.showinfo("Success", "Contacts imported successfully!")

    def list_upcoming_birthdays_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Upcoming Birthdays")
        ListUpcomingBirthdaysWindow(self.new_window, self.contact_book)

    def undo_delete(self):
        self.contact_book.undo_delete()
        messagebox.showinfo("Success", "Last deleted contact restored.")


class AddContactWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.name_label = tk.Label(master, text="Name:", **contact_book.style)
        self.name_label.pack()
        self.name_entry = tk.Entry(master, **contact_book.style)
        self.name_entry.pack()

        self.phone_label = tk.Label(master, text="Phone:", **contact_book.style)
        self.phone_label.pack()
        self.phone_entry = tk.Entry(master, **contact_book.style)
        self.phone_entry.pack()

        self.email_label = tk.Label(master, text="Email:", **contact_book.style)
        self.email_label.pack()
        self.email_entry = tk.Entry(master, **contact_book.style)
        self.email_entry.pack()

        self.group_label = tk.Label(master, text="Group:", **contact_book.style)
        self.group_label.pack()
        self.group_entry = tk.Entry(master, **contact_book.style)
        self.group_entry.pack()

        self.birthday_label = tk.Label(master, text="Birthday (YYYY-MM-DD):", **contact_book.style)
        self.birthday_label.pack()
        self.birthday_entry = tk.Entry(master, **contact_book.style)
        self.birthday_entry.pack()

        self.add_button = tk.Button(master, text="Add Contact", command=self.add_contact, **contact_book.style)
        self.add_button.pack(pady=5)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        group = self.group_entry.get()
        birthday = self.birthday_entry.get()
        self.contact_book.add_contact(name, phone, email, group, birthday)
        messagebox.showinfo("Success", "Contact added successfully!")
        self.master.destroy()


class FindContactWindow:
    def __init__(self, master, contact_book, output_text):
        self.master = master
        self.contact_book = contact_book
        self.output_text = output_text
        self.query_label = tk.Label(master, text="Enter name, phone, or email:", **contact_book.style)
        self.query_label.pack()
        self.query_entry = tk.Entry(master, **contact_book.style)
        self.query_entry.pack()

        self.find_button = tk.Button(master, text="Find Contact", command=self.find_contact, **contact_book.style)
        self.find_button.pack(pady=5)

    def find_contact(self):
        query = self.query_entry.get()
        contact = self.contact_book.find_contact(query)
        self.output_text.delete(1.0, tk.END)
        if contact:
            self.output_text.insert(tk.END, f"Found: {contact.name} - {contact.phone} - {contact.email}")
        else:
            self.output_text.insert(tk.END, "Contact not found.")


class DeleteContactWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.name_label = tk.Label(master, text="Enter name of the contact to delete:", **contact_book.style)
        self.name_label.pack()
        self.name_entry = tk.Entry(master, **contact_book.style)
        self.name_entry.pack()

        self.delete_button = tk.Button(master, text="Delete Contact", command=self.delete_contact, **contact_book.style)
        self.delete_button.pack(pady=5)

    def delete_contact(self):
        name = self.name_entry.get()
        self.contact_book.delete_contact(name)
        messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")
        self.master.destroy()


class UpdateContactWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.name_label = tk.Label(master, text="Enter name of the contact to update:", **contact_book.style)
        self.name_label.pack()
        self.name_entry = tk.Entry(master, **contact_book.style)
        self.name_entry.pack()

        self.phone_label = tk.Label(master, text="New Phone (leave blank to keep current):", **contact_book.style)
        self.phone_label.pack()
        self.phone_entry = tk.Entry(master, **contact_book.style)
        self.phone_entry.pack()

        self.email_label = tk.Label(master, text="New Email (leave blank to keep current):", **contact_book.style)
        self.email_label.pack()
        self.email_entry = tk.Entry(master, **contact_book.style)
        self.email_entry.pack()

        self.update_button = tk.Button(master, text="Update Contact", command=self.update_contact, **contact_book.style)
        self.update_button.pack(pady=5)

    def update_contact(self):
        name = self.name_entry.get()
        new_phone = self.phone_entry.get() or None
        new_email = self.email_entry.get() or None
        self.contact_book.update_contact(name, new_phone, new_email)
        messagebox.showinfo("Success", "Contact updated successfully!")
        self.master.destroy()


class ToggleFavoriteWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.name_label = tk.Label(master, text="Enter name of the contact to toggle favorite:", **contact_book.style)
        self.name_label.pack()
        self.name_entry = tk.Entry(master, **contact_book.style)
        self.name_entry.pack()

        self.toggle_button = tk.Button(master, text="Toggle Favorite", command=self.toggle_favorite, **contact_book.style)
        self.toggle_button.pack(pady=5)

    def toggle_favorite(self):
        name = self.name_entry.get()
        self.contact_book.toggle_favorite(name)
        messagebox.showinfo("Success", f"Favorite status toggled for '{name}'.")
        self.master.destroy()


class ListUpcomingBirthdaysWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.days_label = tk.Label(master, text="Enter number of days to check for upcoming birthdays:", **contact_book.style)
        self.days_label.pack()
        self.days_entry = tk.Entry(master, **contact_book.style)
        self.days_entry.pack()

        self.list_button = tk.Button(master, text="List Upcoming Birthdays", command=self.list_birthdays, **contact_book.style)
        self.list_button.pack(pady=5)

        self.output_text = tk.Text(master, wrap=tk.WORD, height=10, width=50, bg="#ffffff", fg="#000000")
        self.output_text.pack(pady=10)

    def list_birthdays(self):
        days_ahead = int(self.days_entry.get())
        birthdays = self.contact_book.list_upcoming_birthdays(self.contact_book.root, [], days_ahead)
        self.output_text.delete(1.0, tk.END)
        if birthdays:
            self.output_text.insert(tk.END, "\n".join(birthdays))
        else:
            self.output_text.insert(tk.END, "No upcoming birthdays found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
