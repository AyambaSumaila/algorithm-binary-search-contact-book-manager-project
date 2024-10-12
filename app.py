import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime, timedelta

class Contact:
    def __init__(self, name, phone, email, birthday, favorite=False):
        self.name = name
        self.phone = phone
        self.email = email
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

    def insert(self, contact):
        if self.root is None:
            self.root = Node(contact)
        else:
            self._insert(self.root, contact)

    def _insert(self, node, contact):
        if contact.name < node.contact.name:
            if node.left is None:
                node.left = Node(contact)
            else:
                self._insert(node.left, contact)
        else:
            if node.right is None:
                node.right = Node(contact)
            else:
                self._insert(node.right, contact)

    def find(self, name):
        return self._find(self.root, name)

    def _find(self, node, name):
        if node is None:
            return None
        if node.contact.name == name:
            return node.contact
        elif name < node.contact.name:
            return self._find(node.left, name)
        else:
            return self._find(node.right, name)

    def delete(self, name):
        self.root, deleted_contact = self._delete(self.root, name)
        return deleted_contact

    def _delete(self, node, name):
        if node is None:
            return node, None
        deleted_contact = None
        if name < node.contact.name:
            node.left, deleted_contact = self._delete(node.left, name)
        elif name > node.contact.name:
            node.right, deleted_contact = self._delete(node.right, name)
        else:
            deleted_contact = node.contact
            if node.left is None:
                return node.right, deleted_contact
            elif node.right is None:
                return node.left, deleted_contact
            temp = self._min_value_node(node.right)
            node.contact = temp.contact
            node.right, _ = self._delete(node.right, temp.contact.name)
        return node, deleted_contact

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def list_contacts(self):
        contacts = []
        self._in_order_traversal(self.root, contacts)
        return contacts

    def _in_order_traversal(self, node, contacts):
        if node is not None:
            self._in_order_traversal(node.left, contacts)
            contacts.append(node.contact)
            self._in_order_traversal(node.right, contacts)

    def toggle_favorite(self, name):
        contact = self.find(name)
        if contact:
            contact.favorite = not contact.favorite
            return contact
        return None

    def list_favorites(self):
        favorites = []
        self._in_order_favorites(self.root, favorites)
        return favorites

    def _in_order_favorites(self, node, favorites):
        if node is not None:
            self._in_order_favorites(node.left, favorites)
            if node.contact.favorite:
                favorites.append(node.contact)
            self._in_order_favorites(node.right, favorites)

    def list_upcoming_birthdays(self, days):
        upcoming = []
        today = datetime.now().date()
        for contact in self.list_contacts():
            birthday_date = datetime.strptime(contact.birthday, "%Y-%m-%d").date()
            birthday_this_year = birthday_date.replace(year=today.year)
            if today <= birthday_this_year <= today + timedelta(days=days):
                upcoming.append(contact)
        return upcoming

    def export_to_csv(self, filename):
        contacts = self.list_contacts()
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phone', 'Email', 'Birthday', 'Favorite'])
            for contact in contacts:
                writer.writerow([contact.name, contact.phone, contact.email, contact.birthday, contact.favorite])

    def import_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contact = Contact(row['Name'], row['Phone'], row['Email'], row['Birthday'], row['Favorite'] == 'True')
                self.insert(contact)

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.contact_book = BinarySearchTree()
        self.root.title("Contact Book")
        self.style = {
            'bg': "#f0f0f0",
            'fg': "#333333",
            'font': ("Arial", 12)
        }
        self.create_widgets()

    def create_widgets(self):
        self.list_button = tk.Button(self.root, text="List All Contacts", command=self.list_contacts, **self.style)
        self.list_button.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact_window, **self.style)
        self.add_button.pack(pady=5)

        self.find_button = tk.Button(self.root, text="Find Contact", command=self.find_contact_window, **self.style)
        self.find_button.pack(pady=5)

        self.update_button = tk.Button(self.root, text="Update Contact", command=self.update_contact_window, **self.style)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact_window, **self.style)
        self.delete_button.pack(pady=5)

        self.toggle_favorite_button = tk.Button(self.root, text="Toggle Favorite", command=self.toggle_favorite_window, **self.style)
        self.toggle_favorite_button.pack(pady=5)

        self.list_favorites_button = tk.Button(self.root, text="List Favorite Contacts", command=self.list_favorite_contacts, **self.style)
        self.list_favorites_button.pack(pady=5)

        self.export_button = tk.Button(self.root, text="Export Contacts to CSV", command=self.export_contacts, **self.style)
        self.export_button.pack(pady=5)

        self.import_button = tk.Button(self.root, text="Import Contacts from CSV", command=self.import_contacts, **self.style)
        self.import_button.pack(pady=5)

        self.birthday_button = tk.Button(self.root, text="List Upcoming Birthdays", command=self.list_upcoming_birthdays_window, **self.style)
        self.birthday_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, **self.style)
        self.exit_button.pack(pady=5)

    def add_contact_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Contact")

        tk.Label(window, text="Name:", **self.style).pack(pady=5)
        name_entry = tk.Entry(window, **self.style)
        name_entry.pack(pady=5)

        tk.Label(window, text="Phone:", **self.style).pack(pady=5)
        phone_entry = tk.Entry(window, **self.style)
        phone_entry.pack(pady=5)

        tk.Label(window, text="Email:", **self.style).pack(pady=5)
        email_entry = tk.Entry(window, **self.style)
        email_entry.pack(pady=5)

        tk.Label(window, text="Birthday (YYYY-MM-DD):", **self.style).pack(pady=5)
        birthday_entry = tk.Entry(window, **self.style)
        birthday_entry.pack(pady=5)

        def add_contact():
            contact = Contact(name_entry.get(), phone_entry.get(), email_entry.get(), birthday_entry.get())
            self.contact_book.insert(contact)
            messagebox.showinfo("Success", "Contact added successfully!")
            window.destroy()

        tk.Button(window, text="Add", command=add_contact, **self.style).pack(pady=5)

    def find_contact_window(self):
        window = tk.Toplevel(self.root)
        window.title("Find Contact")

        tk.Label(window, text="Enter name of the contact:", **self.style).pack(pady=5)
        name_entry = tk.Entry(window, **self.style)
        name_entry.pack(pady=5)

        output_text = tk.Text(window, height=10, width=40, **self.style)
        output_text.pack(pady=5)

        def find_contact():
            contact = self.contact_book.find(name_entry.get())
            if contact:
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}\nBirthday: {contact.birthday}\nFavorite: {contact.favorite}")
            else:
                messagebox.showinfo("Not Found", "Contact not found.")

        tk.Button(window, text="Find", command=find_contact, **self.style).pack(pady=5)

    def update_contact_window(self):
        window = tk.Toplevel(self.root)
        window.title("Update Contact")

        tk.Label(window, text="Enter name of the contact to update:", **self.style).pack(pady=5)
        name_entry = tk.Entry(window, **self.style)
        name_entry.pack(pady=5)

        output_text = tk.Text(window, height=10, width=40, **self.style)
        output_text.pack(pady=5)

        def update_contact():
            contact = self.contact_book.find(name_entry.get())
            if contact:
                contact.phone = phone_entry.get()
                contact.email = email_entry.get()
                contact.birthday = birthday_entry.get()
                messagebox.showinfo("Success", "Contact updated successfully!")
                window.destroy()
            else:
                messagebox.showinfo("Not Found", "Contact not found.")

        tk.Label(window, text="New Phone:", **self.style).pack(pady=5)
        phone_entry = tk.Entry(window, **self.style)
        phone_entry.pack(pady=5)

        tk.Label(window, text="New Email:", **self.style).pack(pady=5)
        email_entry = tk.Entry(window, **self.style)
        email_entry.pack(pady=5)

        tk.Label(window, text="New Birthday (YYYY-MM-DD):", **self.style).pack(pady=5)
        birthday_entry = tk.Entry(window, **self.style)
        birthday_entry.pack(pady=5)

        tk.Button(window, text="Update", command=update_contact, **self.style).pack(pady=5)

    def delete_contact_window(self):
        window = tk.Toplevel(self.root)
        window.title("Delete Contact")

        tk.Label(window, text="Enter name of the contact to delete:", **self.style).pack(pady=5)
        name_entry = tk.Entry(window, **self.style)
        name_entry.pack(pady=5)

        def delete_contact():
            deleted_contact = self.contact_book.delete(name_entry.get())
            if deleted_contact:
                messagebox.showinfo("Deleted", f"Contact {deleted_contact.name} deleted successfully!")
                window.destroy()
            else:
                messagebox.showinfo("Not Found", "Contact not found.")

        tk.Button(window, text="Delete", command=delete_contact, **self.style).pack(pady=5)

    def toggle_favorite_window(self):
        window = tk.Toplevel(self.root)
        window.title("Toggle Favorite")

        tk.Label(window, text="Enter name of the contact:", **self.style).pack(pady=5)
        name_entry = tk.Entry(window, **self.style)
        name_entry.pack(pady=5)

        def toggle_favorite():
            contact = self.contact_book.toggle_favorite(name_entry.get())
            if contact:
                status = "marked as favorite." if contact.favorite else "unmarked as favorite."
                messagebox.showinfo("Success", f"Contact {contact.name} has been {status}")
                window.destroy()
            else:
                messagebox.showinfo("Not Found", "Contact not found.")

        tk.Button(window, text="Toggle Favorite", command=toggle_favorite, **self.style).pack(pady=5)

    def list_favorite_contacts(self):
        favorites = self.contact_book.list_favorites()
        if not favorites:
            messagebox.showinfo("Favorites", "No favorite contacts found.")
            return
        output_text = "\n".join([f"{contact.name} - {contact.phone}" for contact in favorites])
        messagebox.showinfo("Favorite Contacts", output_text)

    def list_contacts(self):
        contacts = self.contact_book.list_contacts()
        if not contacts:
            messagebox.showinfo("Contacts", "No contacts found.")
            return
        output_text = "\n".join([f"{contact.name} - {contact.phone}" for contact in contacts])
        messagebox.showinfo("All Contacts", output_text)

    def list_upcoming_birthdays_window(self):
        window = tk.Toplevel(self.root)
        window.title("Upcoming Birthdays")

        tk.Label(window, text="Enter number of days:", **self.style).pack(pady=5)
        days_entry = tk.Entry(window, **self.style)
        days_entry.pack(pady=5)

        def list_birthdays():
            days = int(days_entry.get())
            upcoming_birthdays = self.contact_book.list_upcoming_birthdays(days)
            if not upcoming_birthdays:
                messagebox.showinfo("Upcoming Birthdays", "No upcoming birthdays found.")
                return
            output_text = "\n".join([f"{contact.name} - {contact.birthday}" for contact in upcoming_birthdays])
            messagebox.showinfo("Upcoming Birthdays", output_text)

        tk.Button(window, text="List Birthdays", command=list_birthdays, **self.style).pack(pady=5)

    def export_contacts(self):
        self.contact_book.export_to_csv("contacts.csv")
        messagebox.showinfo("Export", "Contacts exported successfully!")

    def import_contacts(self):
        self.contact_book.import_from_csv("contacts.csv")
        messagebox.showinfo("Import", "Contacts imported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
