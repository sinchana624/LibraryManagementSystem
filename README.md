# 📚 LibraSmart – Smart Library Management System

LibraSmart is a command-line Library Management System developed using Python to simplify everyday library operations. It provides an organized way to manage books, register members, track issued and returned books, and maintain borrowing records.

The application features a colorful terminal interface, a live statistics dashboard, automatic late fine calculation, overdue reports, popular book analytics, and a reservation queue.

## ✨ Features

- 📖 **Book Management:** Add, view, and search books.
- 👥 **Member Management:** Register and view library members.
- 📤 **Book Issuing:** Issue available books with a 14-day loan period.
- 📥 **Book Returns:** Track returns and calculate late fines at ₹2 per day.
- 💾 **Data Persistence:** Automatically save library records in JSON format.
- 📊 **Dashboard:** View book availability, member count, issued books, overdue records, and reservations.
- ⏰ **Overdue Reports:** Identify overdue books and calculate current fines.
- 📜 **Borrowing History:** View a member's issue and return records.
- 🏆 **Popular Books Analytics:** Rank books by borrowing frequency.
- 🔖 **Reservation Queue:** Allow members to reserve unavailable books.
- 🎨 **Terminal UI:** Colorful interface with formatted tables and status messages.

## 🛠️ Technologies Used

- Python 3.8+
- JSON
- `datetime`
- `os`

## ▶️ How to Run

1. Install Python 3.8 or later.
2. Clone or download this repository.
3. Open the project folder in a terminal.
4. Run:

   `python library.py`

The application creates `library_data.json` automatically when the first successful change is saved.

## 🎯 Project Objective

To develop a simple and reliable library management application while applying Python programming concepts such as functions, dictionaries, loops, conditional statements, exception handling, date calculations, and file handling.

