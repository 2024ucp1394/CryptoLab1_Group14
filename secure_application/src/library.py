import sqlite3
from datetime import datetime

DB_NAME = "library.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            issue_date TEXT,
            return_date TEXT
        )
    """)

    conn.commit()
    conn.close()


def register_member():
    name = input("Enter member name: ")
    email = input("Enter email: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO members (name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()

    print("Member registered successfully.")


def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    conn.commit()
    conn.close()

    print("Book added successfully.")


def search_books():
    search = input("Enter book title to search: ")

    conn = connect_db()
    cursor = conn.cursor()

    # VULNERABILITY 1: SQL Injection
    query = "SELECT * FROM books WHERE title LIKE '%" + search + "%'"

    cursor.execute(query)

    books = cursor.fetchall()

    if books:
        print("\nBooks found:")
        for book in books:
            print(book)
    else:
        print("No books found.")

    conn.close()


def issue_book():
    book_id = input("Enter book ID: ")
    member_id = input("Enter member ID: ")

    # VULNERABILITY 2: Improper Input Validation

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT available FROM books WHERE id = " + book_id
    )

    book = cursor.fetchone()

    if book is None:
        print("Book does not exist.")
        conn.close()
        return

    if book[0] == 0:
        print("Book is already issued.")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO issues "
        "(book_id, member_id, issue_date) "
        "VALUES (?, ?, ?)",
        (
            book_id,
            member_id,
            datetime.now().strftime("%Y-%m-%d")
        )
    )

    cursor.execute(
        "UPDATE books SET available = 0 WHERE id = " + book_id
    )

    conn.commit()
    conn.close()

    print("Book issued successfully.")


def return_book():
    book_id = input("Enter book ID: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT issue_date FROM issues "
        "WHERE book_id = ? AND return_date IS NULL",
        (book_id,)
    )

    issue = cursor.fetchone()

    if issue is None:
        print("Book is not currently issued.")
        conn.close()
        return

    issue_date = datetime.strptime(
        issue[0],
        "%Y-%m-%d"
    )

    current_date = datetime.now()

    days = (current_date - issue_date).days

    fine = 0

    if days > 14:
        fine = (days - 14) * 5

    cursor.execute(
        "UPDATE issues SET return_date = ? "
        "WHERE book_id = ? AND return_date IS NULL",
        (
            current_date.strftime("%Y-%m-%d"),
            book_id
        )
    )

    cursor.execute(
        "UPDATE books SET available = 1 WHERE id = ?",
        (book_id,)
    )

    conn.commit()
    conn.close()

    print("Book returned successfully.")
    print("Fine: Rs.", fine)


def view_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    print("\nBooks:")

    for book in books:
        print(book)

    conn.close()


def view_file():
    filename = input("Enter filename: ")

    # VULNERABILITY 3: Directory Traversal
    with open(filename, "r") as file:
        print(file.read())


def main():
    initialize_database()

    while True:

        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Register Member")
        print("2. Add Book")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. View Books")
        print("7. View File")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_member()

        elif choice == "2":
            add_book()

        elif choice == "3":
            search_books()

        elif choice == "4":
            issue_book()

        elif choice == "5":
            return_book()

        elif choice == "6":
            view_books()

        elif choice == "7":
            view_file()

        elif choice == "8":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
