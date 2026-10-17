# 📚 LibraSmart – Smart Library Management System

**LibraSmart** is a Python-based desktop application designed to simplify library operations through a modern graphical user interface (GUI), interactive data visualizations, and automated book management.

Built using **Python, Tkinter, Matplotlib, and JSON**, the application enables librarians to manage books and members, issue and return books, calculate late fines, handle reservations, and explore library borrowing statistics through interactive charts.

## ✨ Features

### 📊 Interactive Dashboard
- View total book titles, total copies, available copies, registered members, issued books, and overdue books.
- Access common library operations through quick-action buttons.

### 📖 Book Management
- Add books with unique book IDs, titles, authors, and copy counts.
- View the complete book collection in a structured table.
- Search books by ID, title, or author.
- Track total and available copies.

### 👥 Member Management
- Register new library members with unique member IDs.
- Store member names and contact information.
- View registered members and their active book issues.

### 📤 Book Issuing and Returns
- Issue available books to registered members.
- Automatically assign a 14-day loan period.
- Record issue dates and due dates.
- Process returns and calculate late fines at ₹2 per day.
- Track active, returned, and overdue transactions.

### 📈 Interactive Analytics and Graphs
- **Borrowing Popularity:** Identify the most frequently borrowed books using a bar chart.
- **Book Availability:** Visualize available versus issued copies using a pie chart.
- **Borrowing Activity:** Explore borrowing transactions by issue date using a line chart.
- **Member Activity:** Compare borrowing frequency among members.
- Interact with charts using Matplotlib's navigation toolbar to zoom, pan, and save visualizations.

### ⏰ Overdue Tracking
- Identify currently overdue books.
- Display overdue status in circulation records.
- Calculate late fines when books are returned.

### 🔖 Reservation Management
- Allow members to reserve books when no copies are available.
- Maintain a reservation queue for each book.
- Give priority to the first member in the queue when issuing a reserved book.

### 💾 Data Persistence
- Store books, members, borrowing records, and reservations in `library_data.json`.
- Preserve saved records between application sessions.
- Save updates to a temporary file before replacing the data file.

### 🎨 Desktop User Interface
- Graphical interface built with Tkinter.
- Sidebar navigation for different library modules.
- Form-based data entry and searchable tables.
- Dashboard cards, status indicators, and interactive charts.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.8+ | Core programming language |
| Tkinter | Desktop graphical user interface |
| Matplotlib | Interactive graphs and data visualization |
| JSON | Local data storage and persistence |
| `datetime` | Issue dates, due dates, and fine calculations |
| `collections.Counter` | Borrowing statistics and analytics |
| `os` | File operations and data-file replacement |

## ⚙️ Prerequisites

- Python 3.8 or later
- Matplotlib
- Tkinter support in your Python installation
- Visual Studio Code or another Python-compatible editor (optional)

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sinchana624/LibraryManagementSystem.git
```

### 2. Navigate to the project folder

```bash
cd LibraryManagementSystem
```

### 3. Install the required dependency

```bash
python -m pip install matplotlib
```

Tkinter is generally included with standard Windows Python installations.

### 4. Run the application

```bash
python library.py
```

The LibraSmart desktop window will open. The application uses `library_data.json` in the current working directory to store library records.

## 🧪 How to Test the Application

1. Open **Books** and add a few books.
2. Open **Members** and register members.
3. Navigate to **Circulation** and issue a book.
4. Open **Analytics & Graphs** to explore the charts.
5. Return an issued book and verify the recorded fine.
6. Reserve an unavailable book and inspect the reservation queue.
7. Close and reopen the application to verify data persistence.

## 🎯 Project Objective

The objective of LibraSmart is to develop a practical desktop-based library management solution while applying Python programming concepts, GUI development, file handling, exception handling, date calculations, data structures, and data visualization.

The project demonstrates how traditional library operations can be organized into a user-friendly application with data-driven insights.

## 🔮 Future Enhancements

- Role-based librarian and administrator login.
- Barcode or QR-code-based book identification.
- Exportable borrowing and overdue reports.
- Email or desktop notifications for due dates.
- Database integration using MySQL or SQLite.
- Advanced analytics with monthly and yearly borrowing trends.

## 👩‍💻 Project Information

- **Project Name:** LibraSmart – Smart Library Management System
- **Project Type:** Individual Python Mini Project
- **Interface:** Tkinter Desktop GUI
- **Visualization:** Matplotlib
- **Storage:** JSON
- **Repository:** [LibraryManagementSystem](https://github.com/sinchana624/LibraryManagementSystem)

---

*Developed as a Python mini project to explore desktop application development, library automation, and interactive data visualization.*
