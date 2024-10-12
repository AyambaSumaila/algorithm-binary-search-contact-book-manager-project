import csv
from datetime import datetime, timedelta

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
        print(f"Contact '{name}' added successfully!")

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

    def update_contact(self, name):
        contact = self.find_contact(name)
        if contact:
            print(f"Current Details: {contact.name}, {contact.phone}, {contact.email}")
            phone = input("Enter new phone number (leave blank to keep current): ")
            email = input("Enter new email (leave blank to keep current): ")

            if phone:
                contact.phone = phone
            if email:
                contact.email = email

            print(f"Contact '{name}' updated successfully!")
        else:
            print(f"Contact '{name}' not found.")

    def toggle_favorite(self, name):
        contact = self.find_contact(name)
        if contact:
            contact.favorite = not contact.favorite
            status = "marked as favorite" if contact.favorite else "removed from favorites"
            print(f"Contact '{name}' {status}.")
        else:
            print(f"Contact '{name}' not found.")

    def list_favorite_contacts(self):
        def favorite_filter(root):
            if root:
                favorite_filter(root.left)
                if root.favorite:
                    print(f"{root.name}: {root.phone}, {root.email}")
                favorite_filter(root.right)
        print("Favorite Contacts:")
        favorite_filter(self.root)

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

    def delete_contact(self, name):
        contact = self.find_contact(name)
        if contact:
            self.root = self.delete_contact_util(self.root, name)
            self.last_deleted_contact = contact
            print(f"Contact '{name}' deleted successfully!")
        else:
            print(f"Contact '{name}' not found.")

    def undo_delete(self):
        if self.last_deleted_contact:
            self.add_contact(self.last_deleted_contact.name, self.last_deleted_contact.phone,
                             self.last_deleted_contact.email, self.last_deleted_contact.group,
                             self.last_deleted_contact.birthday)
            print(f"Undo successful! Restored '{self.last_deleted_contact.name}'")
            self.last_deleted_contact = None
        else:
            print("No contact to undo delete.")

    def in_order_traversal(self, root):
        if root:
            self.in_order_traversal(root.left)
            print(f"{root.name}: {root.phone}, {root.email}")
            self.in_order_traversal(root.right)

    def list_contacts(self):
        print("All Contacts:")
        self.in_order_traversal(self.root)

    def list_upcoming_birthdays(self, days_ahead=7):
        upcoming_date = datetime.now() + timedelta(days=days_ahead)

        def birthday_filter(root):
            if root:
                birthday_filter(root.left)
                if root.birthday:
                    birth_date = datetime.strptime(root.birthday, '%Y-%m-%d')
                    if birth_date <= upcoming_date:
                        print(f"{root.name} has a birthday on {root.birthday}")
                birthday_filter(root.right)

        birthday_filter(self.root)

    def export_contacts_to_csv(self, file_name='contacts.csv'):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phone', 'Email', 'Group', 'Favorite', 'Birthday'])
            def write_node(root):
                if root:
                    write_node(root.left)
                    writer.writerow([root.name, root.phone, root.email, root.group,
                                     root.favorite, root.birthday])
                    write_node(root.right)
            write_node(self.root)
        print(f"Contacts exported to {file_name}")

    def import_contacts_from_csv(self, file_name='contacts.csv'):
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_contact(row['Name'], row['Phone'], row['Email'], row['Group'],
                                 birthday=row['Birthday'])
        print(f"Contacts imported from {file_name}")


def display_menu():
    print("\n--- Contact Book Menu ---")
    print("1. Add Contact")
    print("2. Find Contact")
    print("3. Delete Contact")
    print("4. List All Contacts")
    print("5. Update Contact")
    print("6. Toggle Favorite")
    print("7. List Favorite Contacts")
    print("8. Export Contacts to CSV")
    print("9. Import Contacts from CSV")
    print("10. List Upcoming Birthdays")
    print("11. Undo Delete")
    print("12. Exit")


def main():
    contact_book = ContactBookBST()
    while True:
        display_menu()
        choice = input("Choose an option (1-12): ")

        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            email = input("Enter email: ")
            group = input("Enter group (optional): ")
            birthday = input("Enter birthday (YYYY-MM-DD, optional): ")
            contact_book.add_contact(name, phone, email, group, birthday)

        elif choice == '2':
            name = input("Enter name to find: ")
            contact = contact_book.find_contact(name)
            if contact:
                print(f"Contact Found: {contact.name}, {contact.phone}, {contact.email}")
            else:
                print(f"Contact '{name}' not found.")

        elif choice == '3':
            name = input("Enter name to delete: ")
            contact_book.delete_contact(name)

        elif choice == '4':
            contact_book.list_contacts()

        elif choice == '5':
            name = input("Enter name of the contact to update: ")
            contact_book.update_contact(name)

        elif choice == '6':
            name = input("Enter name of the contact to toggle favorite: ")
            contact_book.toggle_favorite(name)

        elif choice == '7':
            contact_book.list_favorite_contacts()

        elif choice == '8':
            file_name = input("Enter file name to export contacts (default: contacts.csv): ")
            contact_book.export_contacts_to_csv(file_name or 'contacts.csv')

        elif choice == '9':
            file_name = input("Enter file name to import contacts from (default: contacts.csv): ")
            contact_book.import_contacts_from_csv(file_name or 'contacts.csv')

        elif choice == '10':
            days = int(input("Enter number of days to check for upcoming birthdays: "))
            contact_book.list_upcoming_birthdays(days)

        elif choice == '11':
            contact_book.undo_delete()

        elif choice == '12':
            print("Exiting Contact Book. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a valid option (1-12).")


if __name__ == "__main__":
    main()
