import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import csv

class ContactNode:
    def __init__(self, name, phone, email, group=None, favorite=False, birthday=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group
        self.favorite = favorite
        self.birthday = birthday
        self.left = None
        self.right = None


class ContactBookBST:
    def __init__(self):
        self.root = None
        self.last_deleted_contact = None

    def insert(self, root, node):
        if root is None:
            return node
        if node.name.lower() < root.name.lower():
            root.left = self.insert(root.left, node)
        else:
            root.right = self.insert(root.right, node)
        return root

    def add_contact(self, name, phone, email, group=None, birthday=None):
        new_contact = ContactNode(name, phone, email, group, birthday=birthday)
        if self.root is None:
            self.root = new_contact
        else:
            self.insert(self.root, new_contact)
        messagebox.showinfo("Success", f"Contact '{name}' added successfully!")

    def search(self, root, query):
        if root is None:
            return None
        if query.lower() in [root.name.lower(), root.email.lower(), root.phone]:
            return root
        if query.lower() < root.name.lower():
            return self.search(root.left, query)
        return self.search(root.right, query)

    def find_contact(self, name):
        return self.search(self.root, name)

    def update_contact(self, name, new_phone, new_email):
        contact = self.find_contact(name)
        if contact:
            if new_phone:
                contact.phone = new_phone
            if new_email:
                contact.email = new_email
            messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")
        else:
            messagebox.showwarning("Error", f"Contact '{name}' not found.")

    def delete_contact(self, name):
        contact = self.find_contact(name)
        if contact:
            self.root = self.delete_contact_util(self.root, name)
            self.last_deleted_contact = contact
            messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")
        else:
            messagebox.showwarning("Error", f"Contact '{name}' not found.")

    def delete_contact_util(self, root, name):
        if root is None:
            return root
        if name.lower() < root.name.lower():
            root.left = self.delete_contact_util(root.left, name)
        elif name.lower() > root.name.lower():
            root.right = self.delete_contact_util(root.right, name)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp_val = self.min_value_node(root.right)
            root.name = temp_val.name
            root.phone = temp_val.phone
            root.email = temp_val.email
            root.right = self.delete_contact_util(root.right, temp_val.name)
        return root

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def toggle_favorite(self, name):
        contact = self.find_contact(name)
        if contact:
            contact.favorite = not contact.favorite
            status = "Favorite" if contact.favorite else "Not Favorite"
            messagebox.showinfo("Success", f"Contact '{name}' is now {status}!")
        else:
            messagebox.showwarning("Error", f"Contact '{name}' not found.")

    def list_favorite_contacts(self, root, favorites_list):
        if root:
            self.list_favorite_contacts(root.left, favorites_list)
            if root.favorite:
                favorites_list.append(f"{root.name}: {root.phone}, {root.email}")
            self.list_favorite_contacts(root.right, favorites_list)
        return favorites_list

    def list_contacts(self, root, contacts_list):
        if root:
            self.list_contacts(root.left, contacts_list)
            contacts_list.append(f"{root.name}: {root.phone}, {root.email}")
            self.list_contacts(root.right, contacts_list)
        return contacts_list

    def list_upcoming_birthdays(self, root, birthdays_list, days_ahead=7):
        if root:
            self.list_upcoming_birthdays(root.left, birthdays_list, days_ahead)
            if root.birthday:
                birth_date = datetime.strptime(root.birthday, '%Y-%m-%d')
                upcoming_date = datetime.now() + timedelta(days=days_ahead)
                if birth_date.month == upcoming_date.month and birth_date.day >= upcoming_date.day:
                    birthdays_list.append(f"{root.name} has a birthday on {root.birthday}")
            self.list_upcoming_birthdays(root.right, birthdays_list, days_ahead)
        return birthdays_list

    def export_contacts_to_csv(self, file_name='contacts.csv'):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phone', 'Email', 'Group', 'Favorite', 'Birthday'])
            self.write_node(self.root, writer)
        messagebox.showinfo("Success", f"Contacts exported to {file_name}")

    def write_node(self, root, writer):
        if root:
            self.write_node(root.left, writer)
            writer.writerow([root.name, root.phone, root.email, root.group, root.favorite, root.birthday])
            self.write_node(root.right, writer)

    def import_contacts_from_csv(self, file_name='contacts.csv'):
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_contact(row['Name'], row['Phone'], row['Email'], row['Group'], row['Birthday'])
        messagebox.showinfo("Success", f"Contacts imported from {file_name}")

    def undo_delete(self):
        if self.last_deleted_contact:
            self.add_contact(self.last_deleted_contact.name, self.last_deleted_contact.phone,
                             self.last_deleted_contact.email, self.last_deleted_contact.group,
                             self.last_deleted_contact.birthday)
            messagebox.showinfo("Success", f"Contact '{self.last_deleted_contact.name}' restored!")
            self.last_deleted_contact = None
        else:
            messagebox.showwarning("Error", "No contact to undo delete.")


class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Contact Book Application")

        self.contact_book = ContactBookBST()

        # Create frames for layout
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Add buttons for functionalities
        self.add_button = tk.Button(self.frame, text="Add Contact", command=self.add_contact_window)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.find_button = tk.Button(self.frame, text="Find Contact", command=self.find_contact_window)
        self.find_button.grid(row=0, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.frame, text="Delete Contact", command=self.delete_contact_window)
        self.delete_button.grid(row=1, column=0, padx=10, pady=10)

        self.list_button = tk.Button(self.frame, text="List Contacts", command=self.list_contacts)
        self.list_button.grid(row=1, column=1, padx=10, pady=10)

        self.update_button = tk.Button(self.frame, text="Update Contact", command=self.update_contact_window)
        self.update_button.grid(row=2, column=0, padx=10, pady=10)

        self.favorite_button = tk.Button(self.frame, text="Toggle Favorite", command=self.toggle_favorite_window)
        self.favorite_button.grid(row=2, column=1, padx=10, pady=10)

        self.favorite_list_button = tk.Button(self.frame, text="List Favorite Contacts", command=self.list_favorite_contacts)
        self.favorite_list_button.grid(row=3, column=0, padx=10, pady=10)

        self.export_button = tk.Button(self.frame, text="Export Contacts", command=self.export_contacts)
        self.export_button.grid(row=3, column=1, padx=10, pady=10)

        self.import_button = tk.Button(self.frame, text="Import Contacts", command=self.import_contacts)
        self.import_button.grid(row=4, column=0, padx=10, pady=10)

        self.birthday_button = tk.Button(self.frame, text="List Upcoming Birthdays", command=self.list_upcoming_birthdays_window)
        self.birthday_button.grid(row=4, column=1, padx=10, pady=10)

        self.undo_button = tk.Button(self.frame, text="Undo Delete", command=self.undo_delete)
        self.undo_button.grid(row=5, column=0, padx=10, pady=10)

        # Output Text
        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.pack(pady=20)

    def add_contact_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add Contact")
        AddContactWindow(self.new_window, self.contact_book)

    def find_contact_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Find Contact")
        FindContactWindow(self.new_window, self.contact_book)

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
        contacts_list = self.contact_book.list_contacts(self.contact_book.root, [])
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "\n".join(contacts_list) if contacts_list else "No contacts found.")

    def list_favorite_contacts(self):
        favorites_list = self.contact_book.list_favorite_contacts(self.contact_book.root, [])
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "\n".join(favorites_list) if favorites_list else "No favorite contacts found.")

    def import_contacts(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.contact_book.import_contacts_from_csv(file_path)

    def export_contacts(self):
        file_path = filedialog.asksaveasfilename(title="Save CSV File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.contact_book.export_contacts_to_csv(file_path)

    def list_upcoming_birthdays_window(self):
        self.output_text.delete(1.0, tk.END)
        birthdays_list = self.contact_book.list_upcoming_birthdays(self.contact_book.root, [])
        self.output_text.insert(tk.END, "\n".join(birthdays_list) if birthdays_list else "No upcoming birthdays.")

    def undo_delete(self):
        self.contact_book.undo_delete()


class AddContactWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.label_name = tk.Label(master, text="Name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(master)
        self.entry_name.pack()
        self.label_phone = tk.Label(master, text="Phone:")
        self.label_phone.pack()
        self.entry_phone = tk.Entry(master)
        self.entry_phone.pack()
        self.label_email = tk.Label(master, text="Email:")
        self.label_email.pack()
        self.entry_email = tk.Entry(master)
        self.entry_email.pack()
        self.label_group = tk.Label(master, text="Group:")
        self.label_group.pack()
        self.entry_group = tk.Entry(master)
        self.entry_group.pack()
        self.label_birthday = tk.Label(master, text="Birthday (YYYY-MM-DD):")
        self.label_birthday.pack()
        self.entry_birthday = tk.Entry(master)
        self.entry_birthday.pack()

        self.button_add = tk.Button(master, text="Add Contact", command=self.add_contact)
        self.button_add.pack()

    def add_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        group = self.entry_group.get()
        birthday = self.entry_birthday.get()
        self.contact_book.add_contact(name, phone, email, group, birthday)
        self.master.destroy()


class FindContactWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.label_name = tk.Label(master, text="Name / Phone / Email:")
        self.label_name.pack()
        self.entry_name = tk.Entry(master)
        self.entry_name.pack()
        self.button_find = tk.Button(master, text="Find", command=self.find_contact)
        self.button_find.pack()

    def find_contact(self):
        query = self.entry_name.get()
        contact = self.contact_book.find_contact(query)
        if contact:
            messagebox.showinfo("Contact Found", f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}")
        else:
            messagebox.showwarning("Not Found", f"No contact found for '{query}'.")
        self.master.destroy()


class DeleteContactWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.label_name = tk.Label(master, text="Name of Contact to Delete:")
        self.label_name.pack()
        self.entry_name = tk.Entry(master)
        self.entry_name.pack()
        self.button_delete = tk.Button(master, text="Delete", command=self.delete_contact)
        self.button_delete.pack()

    def delete_contact(self):
        name = self.entry_name.get()
        self.contact_book.delete_contact(name)
        self.master.destroy()


class UpdateContactWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.label_name = tk.Label(master, text="Name of Contact to Update:")
        self.label_name.pack()
        self.entry_name = tk.Entry(master)
        self.entry_name.pack()
        self.label_phone = tk.Label(master, text="New Phone (leave empty to keep current):")
        self.label_phone.pack()
        self.entry_phone = tk.Entry(master)
        self.entry_phone.pack()
        self.label_email = tk.Label(master, text="New Email (leave empty to keep current):")
        self.label_email.pack()
        self.entry_email = tk.Entry(master)
        self.entry_email.pack()
        self.button_update = tk.Button(master, text="Update", command=self.update_contact)
        self.button_update.pack()

    def update_contact(self):
        name = self.entry_name.get()
        new_phone = self.entry_phone.get()
        new_email = self.entry_email.get()
        self.contact_book.update_contact(name, new_phone, new_email)
        self.master.destroy()


class ToggleFavoriteWindow:
    def __init__(self, master, contact_book):
        self.master = master
        self.contact_book = contact_book
        self.label_name = tk.Label(master, text="Name of Contact:")
        self.label_name.pack()
        self.entry_name = tk.Entry(master)
        self.entry_name.pack()
        self.button_toggle = tk.Button(master, text="Toggle Favorite", command=self.toggle_favorite)
        self.button_toggle.pack()

    def toggle_favorite(self):
        name = self.entry_name.get()
        self.contact_book.toggle_favorite(name)
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
