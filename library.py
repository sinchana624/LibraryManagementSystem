
# ==============================================================
# LIBRASMART | SMART LIBRARY MANAGEMENT SYSTEM
# Python Mini Project | Python 3.8+
# Storage: JSON | Interface: Colorful Command-Line Dashboard
# ==============================================================

import json
import os
from datetime import date, datetime, timedelta

# ------------------------- SETTINGS ----------------------------

FILE = "library_data.json"
LOAN_DAYS = 14
FINE_PER_DAY = 2

# ANSI terminal colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"


# ---------------------- DESIGN FUNCTIONS -----------------------

def line(char="─", width=68, color=CYAN):
    print(f"{color}{char * width}{RESET}")


def heading(title):
    print()
    line("═", color=PURPLE)
    print(f"{BOLD}{PURPLE}  {title.upper()}{RESET}")
    line("═", color=PURPLE)


def success(message):
    print(f"\n{GREEN}{BOLD}  ✔ {message}{RESET}")


def warning(message):
    print(f"\n{YELLOW}  ⚠ {message}{RESET}")


def error(message):
    print(f"\n{RED}  ✘ {message}{RESET}")


def pause():
    input(f"\n{DIM}Press Enter to return to the main menu...{RESET}")


def welcome_screen():
    print(f"\n{PURPLE}{BOLD}")
    print(r"  ██╗     ██╗██████╗ ██████╗  █████╗ ███████╗███╗   ███╗")
    print(r"  ██║     ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗ ████║")
    print(r"  ██║     ██║██████╔╝██████╔╝███████║███████╗██╔████╔██║")
    print(r"  ██║     ██║██╔══██╗██╔══██╗██╔══██║╚════██║██║╚██╔╝██║")
    print(r"  ███████╗██║██████╔╝██║  ██║██║  ██║███████║██║ ╚═╝ ██║")
    print(r"  ╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝")
    print(f"{RESET}{CYAN}{BOLD}             SMART LIBRARY MANAGEMENT SYSTEM{RESET}")
    line("═", color=PURPLE)
    print(f"{WHITE}  Manage books. Empower readers. Simplify library life.{RESET}")
    line("═", color=PURPLE)


# ---------------------- DATA MANAGEMENT -----------------------

def empty_data():
    """Create the initial library database structure."""
    return {
        "books": {},
        "members": {},
        "issued": [],
        "reservations": []
    }


def load_data():
    """Load the JSON database or initialize an empty library."""
    if not os.path.exists(FILE):
        return empty_data()

    try:
        with open(FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("The database must contain a JSON object.")

        # Support older versions of this project.
        data.setdefault("books", {})
        data.setdefault("members", {})
        data.setdefault("issued", [])
        data.setdefault("reservations", [])

        return data

    except (OSError, json.JSONDecodeError, ValueError) as exc:
        error(f"Unable to load the database: {exc}")
        print("Check library_data.json before continuing.")
        raise SystemExit(1)


def save_data(data):
    """Save all library data to the JSON file."""
    temp_file = FILE + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        # Replace the old file only after writing succeeds.
        os.replace(temp_file, FILE)
        return True

    except OSError as exc:
        error(f"Could not save data: {exc}")

        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except OSError:
            pass

        return False


# ----------------------- INPUT HELPERS ------------------------

def get_text(prompt):
    """Accept non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        warning("This field cannot be empty.")


def get_id(prompt):
    """Standardize IDs to uppercase."""
    return get_text(prompt).upper()


def get_positive_int(prompt):
    """Accept only positive whole numbers."""
    while True:
        try:
            number = int(input(prompt))
            if number > 0:
                return number
            warning("Enter a number greater than zero.")
        except ValueError:
            error("Please enter a valid whole number.")


def get_choice(prompt, valid_choices):
    """Accept a choice from a specified set."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        error("Invalid choice. Please try again.")


# ---------------------- DASHBOARD -----------------------------

def dashboard(data):
    """Display current library statistics."""
    total_titles = len(data["books"])
    total_copies = sum(
        book["total"] for book in data["books"].values()
    )
    available_copies = sum(
        book["available"] for book in data["books"].values()
    )
    issued_count = sum(
        record["return_date"] is None
        for record in data["issued"]
    )
    overdue_count = sum(
        record["return_date"] is None
        and record["due_date"] < str(date.today())
        for record in data["issued"]
    )

    heading("Library Dashboard")

    print(f"""
  {CYAN}BOOK COLLECTION{RESET}
  Unique titles           : {BOLD}{total_titles}{RESET}
  Total physical copies   : {BOLD}{total_copies}{RESET}
  Available copies        : {GREEN}{available_copies}{RESET}

  {CYAN}LIBRARY ACTIVITY{RESET}
  Registered members      : {BOLD}{len(data['members'])}{RESET}
  Currently issued        : {YELLOW}{issued_count}{RESET}
  Overdue records         : {RED}{overdue_count}{RESET}
  Active reservations     : {PURPLE}{len(data['reservations'])}{RESET}
""")
    line()


# ----------------------- BOOK MANAGEMENT ----------------------

def add_book(data):
    heading("Add a New Book")

    book_id = get_id("  Book ID       : ")

    if book_id in data["books"]:
        error("A book with this ID already exists.")
        return

    title = get_text("  Book title    : ")
    author = get_text("  Author        : ")
    copies = get_positive_int("  Number of copies: ")

    data["books"][book_id] = {
        "title": title,
        "author": author,
        "total": copies,
        "available": copies
    }

    if save_data(data):
        success("Book added successfully!")


def view_books(data):
    heading("Book Collection")

    if not data["books"]:
        warning("No books found. Add your first book using option 1.")
        return

    print(
        f"{BOLD}{'BOOK ID':<12}{'TITLE':<24}"
        f"{'AUTHOR':<18}{'STOCK':<10}{'STATUS'}{RESET}"
    )
    line()

    for book_id, book in sorted(data["books"].items()):
        title = book["title"][:22]
        author = book["author"][:16]
        stock = f"{book['available']}/{book['total']}"

        if book["available"] > 0:
            status = f"{GREEN}Available{RESET}"
        else:
            status = f"{RED}Out of stock{RESET}"

        print(
            f"{CYAN}{book_id:<12}{RESET}"
            f"{title:<24}{author:<18}{stock:<10}{status}"
        )

    line()
    print(f"{DIM}Stock = available copies / total copies{RESET}")


def search_books(data):
    heading("Search the Collection")

    if not data["books"]:
        warning("The library has no books yet.")
        return

    keyword = get_text("  Enter ID, title or author: ").lower()
    results = []

    for book_id, book in data["books"].items():
        if (
            keyword in book_id.lower()
            or keyword in book["title"].lower()
            or keyword in book["author"].lower()
        ):
            results.append((book_id, book))

    if not results:
        warning("No matching books found.")
        return

    print()
    for book_id, book in results:
        print(f"{CYAN}  [{book_id}]{RESET} {BOLD}{book['title']}{RESET}")
        print(f"       Author    : {book['author']}")
        print(
            f"       Available : "
            f"{book['available']} / {book['total']}"
        )
        line("─", color=BLUE)


# ---------------------- MEMBER MANAGEMENT ---------------------

def add_member(data):
    heading("Register a Member")

    member_id = get_id("  Member ID    : ")

    if member_id in data["members"]:
        error("A member with this ID already exists.")
        return

    name = get_text("  Full name    : ")
    phone = get_text("  Phone number : ")

    data["members"][member_id] = {
        "name": name,
        "phone": phone
    }

    if save_data(data):
        success(f"Member {name} registered successfully!")


def view_members(data):
    heading("Registered Members")

    if not data["members"]:
        warning("No members registered yet.")
        return

    print(f"{BOLD}{'MEMBER ID':<16}{'NAME':<30}{'PHONE'}{RESET}")
    line()

    for member_id, member in sorted(data["members"].items()):
        print(
            f"{CYAN}{member_id:<16}{RESET}"
            f"{member['name'][:28]:<30}{member['phone']}"
        )

    line()


# ------------------------ ISSUE BOOK --------------------------

def issue_book(data):
    heading("Issue a Book")

    book_id = get_id("  Book ID   : ")
    member_id = get_id("  Member ID : ")

    if book_id not in data["books"]:
        error("Book ID not found.")
        return

    if member_id not in data["members"]:
        error("Member ID not found.")
        return

    book = data["books"][book_id]

    if book["available"] < 1:
        warning("No copies are currently available.")
        return

    already_issued = any(
        record["book_id"] == book_id
        and record["member_id"] == member_id
        and record["return_date"] is None
        for record in data["issued"]
    )

    if already_issued:
        warning("This member already has this book issued.")
        return

    # Serve the reservation queue in order.
    queue = [
        item for item in data["reservations"]
        if item["book_id"] == book_id
    ]

    if queue and queue[0]["member_id"] != member_id:
        next_id = queue[0]["member_id"]
        next_name = data["members"][next_id]["name"]
        warning(f"This book is reserved for {next_name} ({next_id}).")
        return

    today = date.today()
    due_date = today + timedelta(days=LOAN_DAYS)

    record = {
        "book_id": book_id,
        "member_id": member_id,
        "issue_date": str(today),
        "due_date": str(due_date),
        "return_date": None,
        "fine": 0
    }

    # Save a rollback copy in case saving fails.
    old_available = book["available"]
    old_issued_length = len(data["issued"])

    data["issued"].append(record)
    book["available"] -= 1

    removed_reservation = None
    if queue and queue[0]["member_id"] == member_id:
        removed_reservation = queue[0]
        data["reservations"].remove(removed_reservation)

    if save_data(data):
        success("Book issued successfully!")
        print(f"  Title      : {book['title']}")
        print(f"  Member     : {data['members'][member_id]['name']}")
        print(f"  Issue date : {today}")
        print(f"  Due date   : {due_date}")
        print(f"  Loan period: {LOAN_DAYS} days")
    else:
        book["available"] = old_available
        del data["issued"][old_issued_length:]
        if removed_reservation is not None:
            data["reservations"].append(removed_reservation)


# ------------------------ RETURN BOOK -------------------------

def return_book(data):
    heading("Return a Book")

    book_id = get_id("  Book ID   : ")
    member_id = get_id("  Member ID : ")

    for record in data["issued"]:
        if (
            record["book_id"] == book_id
            and record["member_id"] == member_id
            and record["return_date"] is None
        ):
            due_date = datetime.strptime(
                record["due_date"], "%Y-%m-%d"
            ).date()

            today = date.today()
            days_late = max(0, (today - due_date).days)
            fine = days_late * FINE_PER_DAY

            book = data["books"][book_id]
            old_available = book["available"]

            record["return_date"] = str(today)
            record["fine"] = fine
            book["available"] += 1

            if save_data(data):
                success("Book returned successfully!")
                print(f"  Book       : {book['title']}")
                print(f"  Days late  : {days_late}")
                print(f"  Fine       : Rs. {fine}")

                queue = [
                    item for item in data["reservations"]
                    if item["book_id"] == book_id
                ]

                if queue:
                    next_id = queue[0]["member_id"]
                    next_name = data["members"][next_id]["name"]
                    warning(
                        f"Next reservation: {next_name} ({next_id})"
                    )
            else:
                record["return_date"] = None
                record["fine"] = 0
                book["available"] = old_available
            return

    error("No active issue record found for this book and member.")


# ----------------------- OVERDUE REPORT -----------------------

def overdue_report(data):
    heading("Overdue Books Report")

    today = date.today()
    found = False

    for record in data["issued"]:
        if record["return_date"] is not None:
            continue

        due_date = datetime.strptime(
            record["due_date"], "%Y-%m-%d"
        ).date()

        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * FINE_PER_DAY

            book = data["books"].get(
                record["book_id"], {"title": "Unknown"}
            )
            member = data["members"].get(
                record["member_id"], {"name": "Unknown"}
            )

            print(f"\n{RED}{BOLD}  OVERDUE RECORD{RESET}")
            print(f"  Book      : {book['title']}")
            print(f"  Member    : {member['name']}")
            print(f"  Due date  : {due_date}")
            print(f"  Days late : {days_late}")
            print(f"  Fine due  : Rs. {fine}")
            line("─", color=RED)
            found = True

    if not found:
        success("No overdue books. Everything is up to date!")


# --------------------- BORROWING HISTORY ----------------------

def member_history(data):
    heading("Member Borrowing History")

    member_id = get_id("  Member ID: ")

    if member_id not in data["members"]:
        error("Member ID not found.")
        return

    member = data["members"][member_id]
    print(f"\n  Name: {member['name']}")
    line()

    records = [
        record for record in data["issued"]
        if record["member_id"] == member_id
    ]

    if not records:
        warning("This member has no borrowing history.")
        return

    for record in records:
        book = data["books"].get(
            record["book_id"], {"title": "Unknown book"}
        )

        status = (
            f"{YELLOW}ISSUED{RESET}"
            if record["return_date"] is None
            else f"{GREEN}RETURNED{RESET}"
        )

        print(f"  Book       : {book['title']}")
        print(f"  Issue date : {record['issue_date']}")
        print(f"  Due date   : {record['due_date']}")
        print(f"  Returned   : {record['return_date'] or 'Pending'}")
        print(f"  Fine       : Rs. {record['fine']}")
        print(f"  Status     : {status}")
        line("─", color=BLUE)


# --------------------- POPULAR BOOKS --------------------------

def popular_books(data):
    heading("Popular Books Analytics")

    if not data["books"]:
        warning("No books available.")
        return

    counts = {book_id: 0 for book_id in data["books"]}

    for record in data["issued"]:
        book_id = record["book_id"]
        if book_id in counts:
            counts[book_id] += 1

    ranked = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    print(f"{BOLD}{'RANK':<8}{'BOOK TITLE':<35}{'BORROWINGS'}{RESET}")
    line()

    for rank, (book_id, count) in enumerate(ranked, start=1):
        title = data["books"][book_id]["title"][:33]
        print(
            f"{CYAN}{rank:<8}{RESET}"
            f"{title:<35}{count}"
        )

    line()
    print(f"{DIM}Rankings use recorded borrowing transactions.{RESET}")


# --------------------- BOOK RESERVATIONS -----------------------

def reserve_book(data):
    heading("Reserve a Book")

    book_id = get_id("  Book ID   : ")
    member_id = get_id("  Member ID : ")

    if book_id not in data["books"]:
        error("Book ID not found.")
        return

    if member_id not in data["members"]:
        error("Member ID not found.")
        return

    if data["books"][book_id]["available"] > 0:
        warning("A copy is available. You can issue it directly.")
        return

    if any(
        record["book_id"] == book_id
        and record["member_id"] == member_id
        for record in data["reservations"]
    ):
        warning("This member already has a reservation for this book.")
        return

    if any(
        record["book_id"] == book_id
        and record["member_id"] == member_id
        and record["return_date"] is None
        for record in data["issued"]
    ):
        warning("This member already has this book issued.")
        return

    reservation = {
        "book_id": book_id,
        "member_id": member_id,
        "reservation_date": str(date.today())
    }

    data["reservations"].append(reservation)

    if save_data(data):
        position = sum(
            item["book_id"] == book_id
            for item in data["reservations"]
        )
        success("Reservation added successfully!")
        print(f"  Book     : {data['books'][book_id]['title']}")
        print(f"  Member   : {data['members'][member_id]['name']}")
        print(f"  Position : {position}")


def view_reservations(data):
    heading("Reservation Queue")

    if not data["reservations"]:
        warning("No active reservations.")
        return

    positions = {}

    for item in data["reservations"]:
        book_id = item["book_id"]
        positions[book_id] = positions.get(book_id, 0) + 1

        book = data["books"].get(
            book_id, {"title": "Unknown book"}
        )
        member = data["members"].get(
            item["member_id"], {"name": "Unknown member"}
        )

        print(f"\n  Book     : {book['title']}")
        print(f"  Member   : {member['name']}")
        print(f"  Position : {positions[book_id]}")
        print(f"  Reserved : {item['reservation_date']}")
        line("─", color=BLUE)


# ------------------------- MAIN MENU --------------------------

def main():
    """Start and manage the LibraSmart application."""
    data = load_data()

    actions = {
        "1": add_book,
        "2": view_books,
        "3": search_books,
        "4": add_member,
        "5": view_members,
        "6": issue_book,
        "7": return_book,
        "8": overdue_report,
        "9": member_history,
        "10": popular_books,
        "11": reserve_book,
        "12": view_reservations
    }

    while True:
        welcome_screen()
        dashboard(data)

        print(f"""
  {BOLD}{CYAN}BOOK MANAGEMENT{RESET}
  {GREEN}[1]{RESET}  Add a book
  {GREEN}[2]{RESET}  Browse all books
  {GREEN}[3]{RESET}  Search the collection

  {BOLD}{CYAN}MEMBER MANAGEMENT{RESET}
  {GREEN}[4]{RESET}  Register a member
  {GREEN}[5]{RESET}  View members

  {BOLD}{CYAN}CIRCULATION DESK{RESET}
  {GREEN}[6]{RESET}  Issue a book
  {GREEN}[7]{RESET}  Return a book
  {GREEN}[8]{RESET}  Overdue report
  {GREEN}[9]{RESET}  Member borrowing history

  {BOLD}{CYAN}SMART FEATURES{RESET}
  {GREEN}[10]{RESET} Popular books analytics
  {GREEN}[11]{RESET} Reserve a book
  {GREEN}[12]{RESET} View reservation queue

  {RED}[13]{RESET} Exit application
""")

        line("═", color=PURPLE)

        choice = input(
            f"{BOLD}{PURPLE}  Enter your choice (1-13): {RESET}"
        ).strip()

        if choice == "13":
            line("═", color=PURPLE)
            print(f"{PURPLE}{BOLD}")
            print("  Thank you for using LibraSmart!")
            print(f"{RESET}{CYAN}  Your library journey continues. Goodbye!{RESET}")
            line("═", color=PURPLE)
            break

        action = actions.get(choice)

        if action:
            try:
                action(data)
            except (KeyError, TypeError, ValueError) as exc:
                error(f"Could not complete this operation: {exc}")
            pause()
        else:
            error("Invalid choice. Please select a number from 1 to 13.")
            pause()


# Run the application when this file is executed directly.
if __name__ == "__main__":
    main()
