

# Contact Book Application Documentation

## Table of Contents
- [Contact Book Application Documentation](#contact-book-application-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Application Structure](#application-structure)
  - [Functionality](#functionality)
  - [Future Enhancements](#future-enhancements)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction
The Contact Book Application is a Python-based GUI application built using Tkinter that allows users to manage their contacts efficiently. It supports adding, finding, updating, deleting contacts, and managing favorites, along with birthday tracking and CSV import/export functionality.

## Features
- Add new contacts with name, phone number, email, and birthday.
- Find contacts by name.
- Update existing contact details.
- Delete contacts.
- Mark contacts as favorites.
- List favorite contacts and upcoming birthdays within a specified timeframe.
- Import and export contacts to and from CSV files.
- Intuitive user interface with easy navigation.

## Technologies Used
- **Python**: Programming language used for the application.
- **Tkinter**: GUI toolkit for creating the user interface.
- **CSV**: For importing and exporting contact data.
- **Datetime**: For managing birthday dates and upcoming birthdays.

## Installation
To set up the Contact Book Application, follow these steps:

1. **Clone the repository** (or download the source code):
   ```bash
   git clone <repository-url>
   cd contact-book-application
   ```

2. **Ensure you have Python installed** on your system. You can download it from [python.org](https://www.python.org/downloads/).

3. **Run the application**:
   ```bash
   python contact_book_app.py
   ```

## Usage
1. **Launching the Application**: After running the application, the main window will open with buttons for various functionalities.
  
2. **Adding a Contact**: Click on "Add Contact" to open the add contact window. Enter the required details and click "Add".

3. **Finding a Contact**: Click "Find Contact" to search for a contact by name.

4. **Updating a Contact**: Use the "Update Contact" option to change the details of an existing contact.

5. **Deleting a Contact**: Click "Delete Contact" and enter the contact's name to remove them from your list.

6. **Toggling Favorite Status**: Mark or unmark a contact as a favorite using the "Toggle Favorite" option.

7. **Listing Contacts**: View all contacts or just favorite contacts using the respective buttons.

8. **Managing Birthdays**: List upcoming birthdays within a specified number of days.

9. **Importing and Exporting Contacts**: Use the respective buttons to import contacts from a CSV file or export the current contacts to a CSV file.

## Application Structure
```
contact_book_app.py         # Main application file
contact.py                  # Contains Contact class definition
binary_search_tree.py       # Contains Binary Search Tree class definition
README.md                   # Documentation file
contacts.csv                # Example contacts CSV file (if applicable)
```

## Functionality
- **Contact Class**: Represents a contact with attributes for name, phone, email, birthday, and favorite status.
- **BinarySearchTree Class**: Implements a binary search tree to store contacts, allowing for efficient insertion, searching, deletion, and traversal.
- **ContactBookApp Class**: Manages the GUI, handling user interactions and linking them to the corresponding functionalities of the binary search tree.

## Future Enhancements
- Implement search functionality with fuzzy matching for better user experience.
- Add data validation to ensure correct formats for phone numbers and emails.
- Enable user authentication for better data security.
- Implement a more advanced database system (e.g., SQLite) for contact storage.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to the branch.
4. Create a pull request explaining your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This documentation provides a thorough overview of your project, making it easier for others to understand its functionality, installation process, and contribution guidelines. You can modify or expand any sections as needed.