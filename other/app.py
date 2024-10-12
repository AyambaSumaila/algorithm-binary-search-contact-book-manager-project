class ContactNode:
    """Defining a Contact Node."""
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.left = None
        self.right = None


class ContactBookBST:
    """Binary Search Tree to store contacts."""
    def __init__(self):
        self.root = None

    def insert(self, root, node):
        if root is None:
            return node
        if node.name.lower() < root.name.lower():
            root.left = self.insert(root.left, node)
        else:
            root.right = self.insert(root.right, node)
        return root

    def add_contact(self, name, phone, email):
        new_contact = ContactNode(name, phone, email)
        if self.root is None:
            self.root = new_contact
        else:
            self.insert(self.root, new_contact)

    def search(self, root, name):
        if root is None or root.name.lower() == name.lower():
            return root
        if name.lower() < root.name.lower():
            return self.search(root.left, name)
        return self.search(root.right, name)

    def find_contact(self, name):
        """Search functionality."""
        return self.search(self.root, name)

    def delete_contact_util(self, root, name):
        """Delete contact functionality."""
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
        self.root = self.delete_contact_util(self.root, name)

    def in_order_traversal(self, root):
        """In-order traversal to list contacts."""
        if root:
            self.in_order_traversal(root.left)
            print(f"{root.name}: {root.phone}, {root.email}")
            self.in_order_traversal(root.right)

    def list_contacts(self):
        """List all contacts."""
        if self.root is None:
            print("No contacts found.")
        else:
            self.in_order_traversal(self.root)


def display_menu():
    """Display menu options to the user."""
    print("\n--- Contact Book Menu ---")
    print("1. Add Contact")
    print("2. Find Contact")
    print("3. Delete Contact")
    print("4. List All Contacts")
    print("5. Exit")


def main():
    contact_book = ContactBookBST()

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            name = input("Enter contact name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email: ")
            contact_book.add_contact(name, phone, email)
            print(f"Contact '{name}' added successfully!")

        elif choice == '2':
            name = input("Enter name to search: ")
            contact = contact_book.find_contact(name)
            if contact:
                print(f"Contact Found: {contact.name}, {contact.phone}, {contact.email}")
            else:
                print(f"Contact '{name}' not found.")

        elif choice == '3':
            name = input("Enter name of the contact to delete: ")
            contact_book.delete_contact(name)
            print(f"Contact '{name}' deleted if it existed.")

        elif choice == '4':
            print("Listing all contacts:")
            contact_book.list_contacts()

        elif choice == '5':
            print("Exiting Contact Book. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a valid option (1-5).")


if __name__ == "__main__":
    main()
