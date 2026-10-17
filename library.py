
# ==============================================================
# LIBRASMART - SMART LIBRARY MANAGEMENT SYSTEM
# Python 3.8+ | Tkinter GUI | Matplotlib Analytics | JSON Storage
# ==============================================================

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta, datetime
from collections import Counter

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

# ------------------------- CONFIG -------------------------------

DATA_FILE = "library_data.json"
LOAN_DAYS = 14
FINE_PER_DAY = 2

BG = "#F4F3FA"
SIDEBAR = "#211B3B"
PURPLE = "#6C4AB6"
LIGHT_PURPLE = "#EEE8FC"
WHITE = "#FFFFFF"
DARK = "#28243A"
GREEN = "#21966B"
RED = "#D94F5C"
ORANGE = "#E99A35"
MUTED = "#77738A"


def empty_data():
    return {
        "books": {},
        "members": {},
        "issued": [],
        "reservations": []
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        return empty_data()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid database format.")

        for key in ("books", "members", "issued", "reservations"):
            data.setdefault(key, {} if key in ("books", "members") else [])

        return data

    except (OSError, json.JSONDecodeError, ValueError) as exc:
        messagebox.showerror(
            "Database Error",
            f"Could not load {DATA_FILE}:\n{exc}\n\n"
            "Check the file before restarting."
        )
        raise SystemExit(1)


def save_data(data):
    temp_file = DATA_FILE + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        os.replace(temp_file, DATA_FILE)
        return True

    except OSError as exc:
        messagebox.showerror("Save Error", str(exc))
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except OSError:
            pass
        return False


# -------------------------- APP ---------------------------------

class LibraSmartApp:

    def __init__(self, root):
        self.root = root
        self.root.title("LibraSmart | Library Management")
        self.root.geometry("1250x790")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG)

        self.data = load_data()
        self.chart_canvas = None
        self.chart_toolbar = None
        self.current_tab = "Dashboard"

        self.setup_style()
        self.build_layout()
        self.show_dashboard()

    # ----------------------- STYLING ----------------------------

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=DARK,
            fieldbackground=WHITE,
            rowheight=30,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=LIGHT_PURPLE,
            foreground=SIDEBAR,
            font=("Segoe UI", 10, "bold"),
            padding=8
        )
        style.map(
            "Treeview",
            background=[("selected", LIGHT_PURPLE)],
            foreground=[("selected", DARK)]
        )

        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            padding=(18, 10),
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "TCombobox",
            padding=6
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="📚 LibraSmart",
            font=("Segoe UI", 20, "bold"),
            bg=SIDEBAR,
            fg="white"
        ).pack(pady=(28, 4))

        tk.Label(
            self.sidebar,
            text="LIBRARY MANAGEMENT",
            font=("Segoe UI", 9),
            bg=SIDEBAR,
            fg="#C7B7F2"
        ).pack(pady=(0, 28))

        navigation = [
            ("Dashboard", self.show_dashboard),
            ("Books", self.show_books),
            ("Members", self.show_members),
            ("Circulation", self.show_circulation),
            ("Analytics & Graphs", self.show_analytics),
            ("Reservations", self.show_reservations),
        ]

        for label, command in navigation:
            tk.Button(
                self.sidebar,
                text="   " + label,
                command=command,
                anchor="w",
                font=("Segoe UI", 11),
                bg=SIDEBAR,
                fg="white",
                activebackground=PURPLE,
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=12,
                pady=13
            ).pack(fill="x", padx=10, pady=3)

        tk.Frame(
            self.sidebar, bg="#4A4068", height=1
        ).pack(fill="x", padx=18, pady=20)

        tk.Label(
            self.sidebar,
            text="Python • Tkinter • Matplotlib\nJSON Data Storage",
            bg=SIDEBAR,
            fg="#BDB5D3",
            font=("Segoe UI", 9),
            justify="left"
        ).pack(side="bottom", pady=25)

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

    def clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def page_header(self, title, subtitle):
        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 23, "bold"),
            bg=BG,
            fg=DARK
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subtitle,
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            header,
            text=date.today().strftime("%d %b %Y"),
            font=("Segoe UI", 10, "bold"),
            bg=BG,
            fg=PURPLE
        ).pack(anchor="e")

    def button(self, parent, text, command, color=PURPLE):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9
        )

    def card(self, parent, title, value, color=PURPLE):
        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground="#E4E0EF",
            highlightthickness=1
        )

        tk.Frame(frame, bg=color, height=4).pack(fill="x")

        tk.Label(
            frame,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=15, pady=(13, 5))

        tk.Label(
            frame,
            text=str(value),
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w", padx=15, pady=(0, 15))

        return frame

    def make_table(self, parent, columns, headings, widths=None):
        container = tk.Frame(parent, bg=WHITE)

        tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings"
        )

        for i, col in enumerate(columns):
            tree.heading(col, text=headings[i])
            tree.column(
                col,
                width=widths[i] if widths else 130,
                anchor="w"
            )

        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return container, tree

    def make_chart(self, parent, figure):
        if self.chart_canvas:
            try:
                self.chart_canvas.get_tk_widget().destroy()
            except tk.TclError:
                pass

        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, parent, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(fill="x")

        self.chart_canvas = canvas
        self.chart_toolbar = toolbar

    # ----------------------- STATISTICS -------------------------

    def stats(self):
        books = self.data["books"]
        total_titles = len(books)
        total_copies = sum(b["total"] for b in books.values())
        available = sum(b["available"] for b in books.values())

        active = [
            r for r in self.data["issued"]
            if r.get("return_date") is None
        ]

        overdue = [
            r for r in active
            if r["due_date"] < str(date.today())
        ]

        return {
            "titles": total_titles,
            "copies": total_copies,
            "available": available,
            "members": len(self.data["members"]),
            "issued": len(active),
            "overdue": len(overdue),
            "reservations": len(self.data["reservations"])
        }

    # ----------------------- DASHBOARD --------------------------

    def show_dashboard(self):
        self.current_tab = "Dashboard"
        self.clear_main()
        self.page_header(
            "Dashboard",
            "Your library at a glance"
        )

        stats = self.stats()

        cards = tk.Frame(self.main, bg=BG)
        cards.pack(fill="x", padx=25, pady=8)

        card_data = [
            ("BOOK TITLES", stats["titles"], PURPLE),
            ("TOTAL COPIES", stats["copies"], "#4387D7"),
            ("AVAILABLE", stats["available"], GREEN),
            ("MEMBERS", stats["members"], ORANGE),
            ("ISSUED", stats["issued"], "#4387D7"),
            ("OVERDUE", stats["overdue"], RED),
        ]

        for index, (title, value, color) in enumerate(card_data):
            widget = self.card(cards, title, value, color)
            widget.grid(
                row=index // 3,
                column=index % 3,
                sticky="nsew",
                padx=7,
                pady=7
            )

        for col in range(3):
            cards.grid_columnconfigure(col, weight=1)

        content = tk.Frame(self.main, bg=BG)
        content.pack(fill="both", expand=True, padx=32, pady=12)

        tk.Label(
            content,
            text="Quick Actions",
            font=("Segoe UI", 14, "bold"),
            bg=BG,
            fg=DARK
        ).pack(anchor="w", pady=(0, 12))

        actions = tk.Frame(content, bg=BG)
        actions.pack(anchor="w")

        self.button(
            actions, "+ Add Book", self.show_books
        ).pack(side="left", padx=(0, 8))

        self.button(
            actions, "+ Register Member", self.show_members,
            color="#4387D7"
        ).pack(side="left", padx=8)

        self.button(
            actions, "Issue / Return", self.show_circulation,
            color=GREEN
        ).pack(side="left", padx=8)

        self.button(
            actions, "View Graphs", self.show_analytics,
            color=ORANGE
        ).pack(side="left", padx=8)

        tk.Label(
            content,
            text=(
                "Data is stored locally in library_data.json.\n"
                "Use Analytics & Graphs to explore borrowing statistics."
            ),
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10),
            justify="left"
        ).pack(anchor="w", pady=28)

    # ------------------------ BOOKS -----------------------------

    def show_books(self):
        self.current_tab = "Books"
        self.clear_main()
        self.page_header(
            "Book Management",
            "Add, browse, search and manage your collection"
        )

        form = tk.LabelFrame(
            self.main,
            text=" Add New Book ",
            bg=WHITE,
            fg=PURPLE,
            font=("Segoe UI", 11, "bold"),
            padx=12,
            pady=12
        )
        form.pack(fill="x", padx=30, pady=8)

        book_id = tk.StringVar()
        title = tk.StringVar()
        author = tk.StringVar()
        copies = tk.StringVar(value="1")

        fields = [
            ("Book ID", book_id, 14),
            ("Title", title, 24),
            ("Author", author, 20),
            ("Copies", copies, 8)
        ]

        for i, (label, variable, width) in enumerate(fields):
            tk.Label(
                form, text=label, bg=WHITE, fg=DARK
            ).grid(row=0, column=i, sticky="w", padx=5)

            tk.Entry(
                form, textvariable=variable, width=width,
                font=("Segoe UI", 10), relief="solid", bd=1
            ).grid(row=1, column=i, padx=5, pady=7, ipady=5)

        def add_book():
            bid = book_id.get().strip().upper()
            name = title.get().strip()
            writer = author.get().strip()

            if not bid or not name or not writer:
                messagebox.showwarning(
                    "Missing Information",
                    "Fill in Book ID, Title and Author."
                )
                return

            if bid in self.data["books"]:
                messagebox.showwarning(
                    "Duplicate ID", "This Book ID already exists."
                )
                return

            try:
                count = int(copies.get())
                if count <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Invalid Copies",
                    "Enter a positive whole number."
                )
                return

            self.data["books"][bid] = {
                "title": name,
                "author": writer,
                "total": count,
                "available": count
            }

            if save_data(self.data):
                messagebox.showinfo(
                    "Success", f"Added '{name}' successfully."
                )
                self.show_books()

        self.button(form, "Add Book", add_book).grid(
            row=1, column=4, padx=10
        )

        search_row = tk.Frame(self.main, bg=BG)
        search_row.pack(fill="x", padx=30, pady=(12, 5))

        search = tk.StringVar()

        tk.Label(
            search_row,
            text="Search books:",
            bg=BG,
            fg=DARK,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 8))

        search_entry = tk.Entry(
            search_row, textvariable=search, width=32,
            font=("Segoe UI", 10)
        )
        search_entry.pack(side="left", ipady=5)

        table_frame = tk.Frame(self.main, bg=WHITE)
        table_frame.pack(
            fill="both", expand=True, padx=30, pady=(5, 25)
        )

        container, tree = self.make_table(
            table_frame,
            ("id", "title", "author", "total", "available", "status"),
            ("Book ID", "Title", "Author", "Total", "Available", "Status"),
            (100, 230, 190, 75, 90, 120)
        )
        container.pack(fill="both", expand=True, padx=5, pady=5)

        def refresh(*_):
            tree.delete(*tree.get_children())
            keyword = search.get().lower()

            for bid, book in sorted(self.data["books"].items()):
                searchable = (
                    bid + book["title"] + book["author"]
                ).lower()

                if keyword and keyword not in searchable:
                    continue

                status = (
                    "Available" if book["available"] > 0
                    else "Out of stock"
                )

                tree.insert(
                    "", "end",
                    values=(
                        bid,
                        book["title"],
                        book["author"],
                        book["total"],
                        book["available"],
                        status
                    )
                )

        search.trace_add("write", refresh)
        refresh()

    # ----------------------- MEMBERS ---------------------------

    def show_members(self):
        self.current_tab = "Members"
        self.clear_main()
        self.page_header(
            "Member Management",
            "Register and browse library members"
        )

        form = tk.LabelFrame(
            self.main,
            text=" Register Member ",
            bg=WHITE,
            fg=PURPLE,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=12
        )
        form.pack(fill="x", padx=30, pady=10)

        member_id = tk.StringVar()
        name = tk.StringVar()
        phone = tk.StringVar()

        for i, (label, variable) in enumerate([
            ("Member ID", member_id),
            ("Full Name", name),
            ("Phone", phone)
        ]):
            tk.Label(
                form, text=label, bg=WHITE, fg=DARK
            ).grid(row=0, column=i, sticky="w", padx=6)

            tk.Entry(
                form, textvariable=variable, width=24,
                font=("Segoe UI", 10)
            ).grid(row=1, column=i, padx=6, pady=8, ipady=5)

        def register():
            mid = member_id.get().strip().upper()
            full_name = name.get().strip()
            contact = phone.get().strip()

            if not mid or not full_name or not contact:
                messagebox.showwarning(
                    "Missing Information", "Complete all fields."
                )
                return

            if mid in self.data["members"]:
                messagebox.showwarning(
                    "Duplicate ID", "This Member ID already exists."
                )
                return

            self.data["members"][mid] = {
                "name": full_name,
                "phone": contact
            }

            if save_data(self.data):
                messagebox.showinfo(
                    "Success", "Member registered successfully."
                )
                self.show_members()

        self.button(form, "Register", register).grid(
            row=1, column=3, padx=12
        )

        table_frame = tk.Frame(self.main, bg=WHITE)
        table_frame.pack(
            fill="both", expand=True, padx=30, pady=(5, 25)
        )

        container, tree = self.make_table(
            table_frame,
            ("id", "name", "phone", "active"),
            ("Member ID", "Name", "Phone", "Active Issues"),
            (140, 280, 200, 130)
        )
        container.pack(fill="both", expand=True, padx=5, pady=5)

        for mid, member in sorted(self.data["members"].items()):
            active = sum(
                r["member_id"] == mid and r["return_date"] is None
                for r in self.data["issued"]
            )
            tree.insert(
                "", "end",
                values=(mid, member["name"], member["phone"], active)
            )

    # --------------------- CIRCULATION -------------------------

    def show_circulation(self):
        self.current_tab = "Circulation"
        self.clear_main()
        self.page_header(
            "Circulation Desk",
            "Issue books, process returns and calculate late fines"
        )

        form = tk.LabelFrame(
            self.main,
            text=" Book Transaction ",
            bg=WHITE,
            fg=PURPLE,
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=18
        )
        form.pack(fill="x", padx=30, pady=10)

        book_id = tk.StringVar()
        member_id = tk.StringVar()

        tk.Label(
            form, text="Book ID", bg=WHITE, fg=DARK
        ).grid(row=0, column=0, sticky="w", padx=8)

        tk.Entry(
            form, textvariable=book_id, width=25
        ).grid(row=1, column=0, padx=8, pady=8, ipady=5)

        tk.Label(
            form, text="Member ID", bg=WHITE, fg=DARK
        ).grid(row=0, column=1, sticky="w", padx=8)

        tk.Entry(
            form, textvariable=member_id, width=25
        ).grid(row=1, column=1, padx=8, pady=8, ipady=5)

        def issue():
            bid = book_id.get().strip().upper()
            mid = member_id.get().strip().upper()

            if bid not in self.data["books"]:
                messagebox.showerror("Error", "Book ID not found.")
                return

            if mid not in self.data["members"]:
                messagebox.showerror("Error", "Member ID not found.")
                return

            book = self.data["books"][bid]

            if book["available"] <= 0:
                messagebox.showwarning(
                    "Unavailable", "No copies are available."
                )
                return

            if any(
                r["book_id"] == bid
                and r["member_id"] == mid
                and r["return_date"] is None
                for r in self.data["issued"]
            ):
                messagebox.showwarning(
                    "Already Issued",
                    "This member already has this book."
                )
                return

            queue = [
                r for r in self.data["reservations"]
                if r["book_id"] == bid
            ]

            if queue and queue[0]["member_id"] != mid:
                reserved_for = self.data["members"].get(
                    queue[0]["member_id"], {}
                ).get("name", queue[0]["member_id"])

                messagebox.showwarning(
                    "Reserved",
                    f"This book is reserved for {reserved_for}."
                )
                return

            record = {
                "book_id": bid,
                "member_id": mid,
                "issue_date": str(date.today()),
                "due_date": str(date.today() + timedelta(days=LOAN_DAYS)),
                "return_date": None,
                "fine": 0
            }

            book["available"] -= 1
            self.data["issued"].append(record)

            removed = None
            if queue:
                removed = queue[0]
                self.data["reservations"].remove(removed)

            if save_data(self.data):
                messagebox.showinfo(
                    "Book Issued",
                    f"{book['title']} issued successfully.\n\n"
                    f"Issue date: {record['issue_date']}\n"
                    f"Due date: {record['due_date']}"
                )
                self.show_circulation()
            else:
                book["available"] += 1
                self.data["issued"].remove(record)
                if removed:
                    self.data["reservations"].append(removed)

        def return_book():
            bid = book_id.get().strip().upper()
            mid = member_id.get().strip().upper()

            for record in self.data["issued"]:
                if (
                    record["book_id"] == bid
                    and record["member_id"] == mid
                    and record["return_date"] is None
                ):
                    due = datetime.strptime(
                        record["due_date"], "%Y-%m-%d"
                    ).date()

                    today = date.today()
                    late_days = max(0, (today - due).days)
                    fine = late_days * FINE_PER_DAY

                    book = self.data["books"][bid]
                    book["available"] += 1
                    record["return_date"] = str(today)
                    record["fine"] = fine

                    if save_data(self.data):
                        messagebox.showinfo(
                            "Book Returned",
                            f"Book returned successfully!\n\n"
                            f"Days late: {late_days}\n"
                            f"Fine: Rs. {fine}"
                        )
                        self.show_circulation()
                    else:
                        book["available"] -= 1
                        record["return_date"] = None
                        record["fine"] = 0
                    return

            messagebox.showerror(
                "Not Found",
                "No active issue found for these IDs."
            )

        self.button(form, "Issue Book", issue, GREEN).grid(
            row=1, column=2, padx=12
        )

        self.button(form, "Return Book", return_book, ORANGE).grid(
            row=1, column=3, padx=12
        )

        tk.Label(
            self.main,
            text=f"Loan period: {LOAN_DAYS} days    |    "
                 f"Late fine: Rs. {FINE_PER_DAY} per day",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 11)
        ).pack(anchor="w", padx=35, pady=15)

        table_frame = tk.Frame(self.main, bg=WHITE)
        table_frame.pack(
            fill="both", expand=True, padx=30, pady=(0, 20)
        )

        container, tree = self.make_table(
            table_frame,
            ("book", "member", "issue", "due", "status", "fine"),
            ("Book", "Member", "Issue Date", "Due Date", "Status", "Fine"),
            (180, 150, 120, 120, 120, 100)
        )
        container.pack(fill="both", expand=True, padx=5, pady=5)

        for record in reversed(self.data["issued"]):
            book = self.data["books"].get(record["book_id"], {})
            member = self.data["members"].get(record["member_id"], {})

            status = (
                "Returned" if record["return_date"] else
                "Overdue" if record["due_date"] < str(date.today()) else
                "Issued"
            )

            tree.insert(
                "", "end",
                values=(
                    book.get("title", record["book_id"]),
                    member.get("name", record["member_id"]),
                    record["issue_date"],
                    record["due_date"],
                    status,
                    "Rs. " + str(record.get("fine", 0))
                )
            )

    # ---------------------- ANALYTICS --------------------------

    def show_analytics(self):
        self.current_tab = "Analytics & Graphs"
        self.clear_main()
        self.page_header(
            "Analytics & Graphs",
            "Explore your library through interactive charts"
        )

        controls = tk.Frame(self.main, bg=BG)
        controls.pack(fill="x", padx=30, pady=(0, 10))

        chart_type = tk.StringVar(value="Borrowing Popularity")

        tk.Label(
            controls,
            text="Select visualization:",
            bg=BG,
            fg=DARK,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 10))

        choices = [
            "Borrowing Popularity",
            "Book Availability",
            "Borrowing Activity",
            "Member Activity"
        ]

        selector = ttk.Combobox(
            controls,
            textvariable=chart_type,
            values=choices,
            state="readonly",
            width=25
        )
        selector.pack(side="left", padx=5)

        chart_area = tk.Frame(self.main, bg=WHITE)
        chart_area.pack(
            fill="both", expand=True, padx=30, pady=(5, 25)
        )

        def draw_chart(*_):
            for widget in chart_area.winfo_children():
                widget.destroy()

            fig = Figure(figsize=(9, 5), dpi=100)
            ax = fig.add_subplot(111)
            fig.patch.set_facecolor(WHITE)
            ax.set_facecolor(WHITE)

            selected = chart_type.get()

            if selected == "Borrowing Popularity":
                counts = Counter(
                    r["book_id"] for r in self.data["issued"]
                )
                top = counts.most_common(10)

                labels = [
                    self.data["books"].get(
                        bid, {"title": bid}
                    )["title"][:20]
                    for bid, _ in top
                ]
                values = [count for _, count in top]

                if not values:
                    labels, values = ["No borrowing data"], [0]

                bars = ax.barh(
                    labels[::-1],
                    values[::-1],
                    color="#8064C9"
                )
                ax.set_title(
                    "Top Borrowed Books",
                    fontsize=15, fontweight="bold", pad=18
                )
                ax.set_xlabel("Number of borrowing transactions")
                ax.grid(axis="x", alpha=0.2)
                ax.set_axisbelow(True)

                for bar, value in zip(bars, values[::-1]):
                    ax.text(
                        value, bar.get_y() + bar.get_height() / 2,
                        f" {value}", va="center"
                    )

            elif selected == "Book Availability":
                total = sum(
                    b["total"] for b in self.data["books"].values()
                )
                available = sum(
                    b["available"] for b in self.data["books"].values()
                )
                issued = max(0, total - available)

                if total:
                    ax.pie(
                        [available, issued],
                        labels=["Available", "Issued"],
                        colors=["#43B581", "#8064C9"],
                        autopct="%1.1f%%",
                        startangle=90,
                        explode=(0.03, 0.03),
                        wedgeprops={"edgecolor": "white", "linewidth": 2}
                    )
                    ax.set_title(
                        "Available vs Issued Copies",
                        fontsize=15, fontweight="bold", pad=18
                    )
                else:
                    ax.text(
                        0.5, 0.5, "Add books to view availability",
                        ha="center", va="center",
                        transform=ax.transAxes
                    )

            elif selected == "Borrowing Activity":
                counts = Counter(
                    r["issue_date"] for r in self.data["issued"]
                )
                dates = sorted(counts)

                if dates:
                    values = [counts[d] for d in dates]
                    ax.plot(
                        dates, values,
                        marker="o", linewidth=2.5,
                        color="#4387D7"
                    )
                    ax.fill_between(
                        dates, values, alpha=0.15, color="#4387D7"
                    )
                    ax.tick_params(axis="x", rotation=35)
                    ax.set_ylabel("Books issued")
                    ax.set_xlabel("Issue date")
                    ax.grid(alpha=0.2)
                else:
                    ax.text(
                        0.5, 0.5, "No borrowing activity recorded yet",
                        ha="center", va="center",
                        transform=ax.transAxes
                    )

                ax.set_title(
                    "Borrowing Activity by Issue Date",
                    fontsize=15, fontweight="bold", pad=18
                )

            elif selected == "Member Activity":
                counts = Counter(
                    r["member_id"] for r in self.data["issued"]
                )
                top = counts.most_common(10)

                labels = [
                    self.data["members"].get(
                        mid, {"name": mid}
                    )["name"][:20]
                    for mid, _ in top
                ]
                values = [count for _, count in top]

                if not values:
                    labels, values = ["No activity"], [0]

                ax.bar(
                    labels, values,
                    color="#E9A23B"
                )
                ax.set_title(
                    "Most Active Members",
                    fontsize=15, fontweight="bold", pad=18
                )
                ax.set_ylabel("Borrowing transactions")
                ax.tick_params(axis="x", rotation=25)
                ax.grid(axis="y", alpha=0.2)
                ax.set_axisbelow(True)

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=chart_area)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            toolbar = NavigationToolbar2Tk(
                canvas, chart_area, pack_toolbar=False
            )
            toolbar.update()
            toolbar.pack(fill="x")

            # Matplotlib toolbar supports zoom, pan and saving charts.
            # Clicking a chart bar also displays its value.
            def on_click(event):
                if event.inaxes != ax or event.xdata is None:
                    return

                if selected == "Borrowing Popularity":
                    for bar in ax.patches:
                        if bar.contains(event)[0]:
                            label = labels[::-1][
                                list(ax.patches).index(bar)
                            ]
                            messagebox.showinfo(
                                "Book Analytics",
                                f"{label}\nBorrowings: "
                                f"{int(bar.get_width())}"
                            )
                            break

            canvas.mpl_connect("button_press_event", on_click)

        selector.bind("<<ComboboxSelected>>", draw_chart)
        self.button(
            controls, "Refresh Chart", draw_chart
        ).pack(side="left", padx=10)

        draw_chart()

    # ---------------------- RESERVATIONS -----------------------

    def show_reservations(self):
        self.current_tab = "Reservations"
        self.clear_main()
        self.page_header(
            "Reservations",
            "Manage the queue for unavailable books"
        )

        form = tk.LabelFrame(
            self.main,
            text=" Reserve a Book ",
            bg=WHITE,
            fg=PURPLE,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )
        form.pack(fill="x", padx=30, pady=10)

        book_id = tk.StringVar()
        member_id = tk.StringVar()

        tk.Label(
            form, text="Book ID", bg=WHITE, fg=DARK
        ).grid(row=0, column=0, sticky="w", padx=6)

        tk.Entry(
            form, textvariable=book_id, width=24
        ).grid(row=1, column=0, padx=6, pady=7, ipady=5)

        tk.Label(
            form, text="Member ID", bg=WHITE, fg=DARK
        ).grid(row=0, column=1, sticky="w", padx=6)

        tk.Entry(
            form, textvariable=member_id, width=24
        ).grid(row=1, column=1, padx=6, pady=7, ipady=5)

        def reserve():
            bid = book_id.get().strip().upper()
            mid = member_id.get().strip().upper()

            if bid not in self.data["books"]:
                messagebox.showerror("Error", "Book not found.")
                return

            if mid not in self.data["members"]:
                messagebox.showerror("Error", "Member not found.")
                return

            if self.data["books"][bid]["available"] > 0:
                messagebox.showwarning(
                    "Available",
                    "A copy is available. Issue it directly."
                )
                return

            if any(
                r["book_id"] == bid and r["member_id"] == mid
                for r in self.data["reservations"]
            ):
                messagebox.showwarning(
                    "Duplicate", "This reservation already exists."
                )
                return

            if any(
                r["book_id"] == bid
                and r["member_id"] == mid
                and r["return_date"] is None
                for r in self.data["issued"]
            ):
                messagebox.showwarning(
                    "Already Issued",
                    "This member already has the book."
                )
                return

            self.data["reservations"].append({
                "book_id": bid,
                "member_id": mid,
                "reservation_date": str(date.today())
            })

            if save_data(self.data):
                messagebox.showinfo(
                    "Success", "Reservation added to the queue."
                )
                self.show_reservations()

        self.button(form, "Reserve Book", reserve).grid(
            row=1, column=2, padx=15
        )

        table_frame = tk.Frame(self.main, bg=WHITE)
        table_frame.pack(
            fill="both", expand=True, padx=30, pady=(5, 25)
        )

        container, tree = self.make_table(
            table_frame,
            ("position", "book", "member", "date"),
            ("Queue Position", "Book", "Member", "Reservation Date"),
            (130, 250, 220, 170)
        )
        container.pack(fill="both", expand=True, padx=5, pady=5)

        positions = {}

        for item in self.data["reservations"]:
            bid = item["book_id"]
            positions[bid] = positions.get(bid, 0) + 1

            book = self.data["books"].get(bid, {})
            member = self.data["members"].get(item["member_id"], {})

            tree.insert(
                "", "end",
                values=(
                    positions[bid],
                    book.get("title", bid),
                    member.get("name", item["member_id"]),
                    item["reservation_date"]
                )
            )


# ------------------------- START APP ---------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraSmartApp(root)
    root.mainloop()
