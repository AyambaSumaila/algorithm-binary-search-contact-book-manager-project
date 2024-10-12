import tkinter as tk
from tkinter import messagebox
from datetime import datetime
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

    def list_contacts(self, root, contacts_list):
        if root:
            self.list_contacts(root.left, contacts_list)
            contacts_list.append(f"{root.name}: {root.phone}, {root.email}")
            self.list_contacts(root.right, contacts_list)
        return contacts_list


class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Application")

        self.contact_book = ContactBookBST()

        # Create frames for layout
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Add Contact
        self.name_label = tk.Label(self.frame, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        self.phone_label = tk.Label(self.frame, text="Phone:")
        self.phone_label.grid(row=1, column=0)
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.grid(row=1, column=1)

        self.email_label = tk.Label(self.frame, text="Email:")
        self.email_label.grid(row=2, column=0)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=2, column=1)

        self.group_label = tk.Label(self.frame, text="Group (Optional):")
        self.group_label.grid(row=3, column=0)
        self.group_entry = tk.Entry(self.frame)
        self.group_entry.grid(row=3, column=1)

        self.birthday_label = tk.Label(self.frame, text="Birthday (YYYY-MM-DD, Optional):")
        self.birthday_label.grid(row=4, column=0)
        self.birthday_entry = tk.Entry(self.frame)
        self.birthday_entry.grid(row=4, column=1)

        self.add_button = tk.Button(self.frame, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # List Contacts
        self.list_button = tk.Button(self.frame, text="List Contacts", command=self.list_contacts)
        self.list_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Output
        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.pack(pady=20)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        group = self.group_entry.get()
        birthday = self.birthday_entry.get()

        if not name or not phone or not email:
            messagebox.showwarning("Input Error", "Name, phone, and email are required.")
            return

        self.contact_book.add_contact(name, phone, email, group, birthday)

    def list_contacts(self):
        self.output_text.delete(1.0, tk.END)
        contacts = self.contact_book.list_contacts(self.contact_book.root, [])
        if contacts:
            self.output_text.insert(tk.END, "\n".join(contacts))
        else:
            self.output_text.insert(tk.END, "No contacts found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
