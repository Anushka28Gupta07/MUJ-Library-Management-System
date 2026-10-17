"""
Library Management System
Backend database operations
Database: MySQL
"""

from datetime import date
from backend.config import get_connection


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def _next_id(cursor, table, column):
    """Generate the next ID for tables using manual IDs."""
    cursor.execute(
        f"SELECT COALESCE(MAX({column}), 0) + 1 AS next_id FROM {table}"
    )
    return cursor.fetchone()["next_id"]


def _fetch_all(query, params=()):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def _fetch_one(query, params=()):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


# ==================================================
# 1. LOGIN
# ==================================================

def check_login(username, password):
    """Demo administrator login. Password is not stored in MySQL."""
    return username == "admin" and password == "admin123"


# ==================================================
# 2. DASHBOARD
# ==================================================

def dashboard_stats():
    """Return total titles, copies, issued copies and members."""
    query = """
        SELECT
            (SELECT COUNT(*) FROM Book) AS titles,
            (SELECT COUNT(*) FROM Book_Copy) AS copies,
            (SELECT COUNT(*) FROM Book_Copy
             WHERE CopyStatus = 'Issued') AS issued,
            (SELECT COUNT(*) FROM Member) AS members
    """
    return _fetch_one(query)


def books_per_category():
    query = """
        SELECT c.CategoryName,
               COUNT(b.BookID) AS book_count
        FROM Category c
        LEFT JOIN Book b ON c.CategoryID = b.CategoryID
        GROUP BY c.CategoryID, c.CategoryName
        ORDER BY c.CategoryName
    """
    return _fetch_all(query)


# ==================================================
# 3. BOOKS AND MASTER DATA
# ==================================================

def list_publishers():
    return _fetch_all("""
        SELECT PublisherID, PublisherName, City
        FROM Publisher ORDER BY PublisherName
    """)


def list_categories():
    return _fetch_all("""
        SELECT CategoryID, CategoryName
        FROM Category ORDER BY CategoryName
    """)


def list_authors():
    return _fetch_all("""
        SELECT AuthorID, AuthorName, Nationality
        FROM Author ORDER BY AuthorName
    """)


def list_book_titles():
    return _fetch_all("""
        SELECT BookID, Title
        FROM Book ORDER BY Title
    """)


def book_list(term=None):
    """List books, with optional title/author/category search."""
    query = """
        SELECT
            b.BookID, b.Title, b.ISBN, b.PublicationYear,
            p.PublisherName, c.CategoryName,
            GROUP_CONCAT(
                DISTINCT a.AuthorName
                ORDER BY a.AuthorName SEPARATOR ', '
            ) AS Authors,
            COUNT(DISTINCT bc.CopyID) AS TotalCopies,
            COUNT(DISTINCT CASE
                WHEN bc.CopyStatus = 'Available'
                THEN bc.CopyID
            END) AS AvailableCopies
        FROM Book b
        JOIN Publisher p ON b.PublisherID = p.PublisherID
        JOIN Category c ON b.CategoryID = c.CategoryID
        LEFT JOIN Book_Author ba ON b.BookID = ba.BookID
        LEFT JOIN Author a ON ba.AuthorID = a.AuthorID
        LEFT JOIN Book_Copy bc ON b.BookID = bc.BookID
    """

    params = ()

    if term and term.strip():
        search = "%" + term.strip() + "%"
        query += """
            WHERE b.Title LIKE %s
               OR b.ISBN LIKE %s
               OR a.AuthorName LIKE %s
               OR c.CategoryName LIKE %s
        """
        params = (search, search, search, search)

    query += """
        GROUP BY b.BookID, b.Title, b.ISBN,
                 b.PublicationYear, p.PublisherName,
                 c.CategoryName
        ORDER BY b.Title
    """

    return _fetch_all(query, params)


def add_book(isbn, title, year, publisher_id,
             category_id, author_ids, copies):
    """Add a book, its author relationships and physical copies."""
    if not title.strip() or not isbn.strip():
        raise ValueError("Book title and ISBN are required.")

    if int(copies) < 0:
        raise ValueError("Number of copies cannot be negative.")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("START TRANSACTION")

        book_id = _next_id(cursor, "Book", "BookID")

        cursor.execute("""
            INSERT INTO Book
                (BookID, Title, ISBN, PublisherID,
                 CategoryID, PublicationYear)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            book_id, title.strip(), isbn.strip(),
            publisher_id, category_id, year
        ))

        for author_id in set(author_ids or []):
            cursor.execute("""
                INSERT INTO Book_Author (BookID, AuthorID)
                VALUES (%s, %s)
            """, (book_id, author_id))

        for _ in range(int(copies)):
            copy_id = _next_id(cursor, "Book_Copy", "CopyID")
            cursor.execute("""
                INSERT INTO Book_Copy (CopyID, BookID, CopyStatus)
                VALUES (%s, %s, 'Available')
            """, (copy_id, book_id))

        connection.commit()
        return book_id

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def update_book(book_id, title, year):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Book
            SET Title = %s, PublicationYear = %s
            WHERE BookID = %s
        """, (title, year, book_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def delete_book(book_id):
    """Prevent deletion when any physical copy has loan history."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("START TRANSACTION")

        cursor.execute("""
            SELECT CopyID FROM Book_Copy
            WHERE BookID = %s FOR UPDATE
        """, (book_id,))
        copies = cursor.fetchall()

        for copy in copies:
            cursor.execute("""
                SELECT LoanID FROM Loan
                WHERE CopyID = %s LIMIT 1
            """, (copy["CopyID"],))

            if cursor.fetchone():
                raise ValueError(
                    "Cannot delete this book because it has loan history."
                )

        cursor.execute(
            "DELETE FROM Book_Author WHERE BookID = %s",
            (book_id,)
        )
        cursor.execute(
            "DELETE FROM Book_Copy WHERE BookID = %s",
            (book_id,)
        )
        cursor.execute(
            "DELETE FROM Book WHERE BookID = %s",
            (book_id,)
        )

        deleted = cursor.rowcount > 0
        connection.commit()
        return deleted

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


# ==================================================
# 4. MEMBERS
# ==================================================

def add_member(name, email, phone):
    if not name.strip() or not email.strip():
        raise ValueError("Member name and email are required.")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        member_id = _next_id(cursor, "Member", "MemberID")

        cursor.execute("""
            INSERT INTO Member
                (MemberID, MemberName, Email, Phone, JoinDate)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            member_id, name.strip(), email.strip(),
            phone or None, date.today()
        ))

        connection.commit()
        return member_id

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def list_members():
    return _fetch_all("""
        SELECT MemberID, MemberName, Email, Phone, JoinDate
        FROM Member ORDER BY MemberName
    """)


def list_member_names():
    return _fetch_all("""
        SELECT MemberID, MemberName
        FROM Member ORDER BY MemberName
    """)


def get_member(id):
    return _fetch_one("""
        SELECT MemberID, MemberName, Email, Phone, JoinDate
        FROM Member WHERE MemberID = %s
    """, (id,))


def update_member(id, name, email, phone):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Member
            SET MemberName = %s, Email = %s, Phone = %s
            WHERE MemberID = %s
        """, (name, email, phone or None, id))

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def delete_member(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("START TRANSACTION")

        cursor.execute("""
            SELECT LoanID FROM Loan
            WHERE MemberID = %s LIMIT 1
        """, (id,))

        if cursor.fetchone():
            raise ValueError(
                "Cannot delete a member who has loan history."
            )

        cursor.execute(
            "DELETE FROM Member WHERE MemberID = %s",
            (id,)
        )
        deleted = cursor.rowcount > 0
        connection.commit()
        return deleted

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


# ==================================================
# 5. AUTHORS, PUBLISHERS AND CATEGORIES
# ==================================================

def add_author(name, nationality):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        author_id = _next_id(cursor, "Author", "AuthorID")
        cursor.execute("""
            INSERT INTO Author (AuthorID, AuthorName, Nationality)
            VALUES (%s, %s, %s)
        """, (author_id, name.strip(), nationality or None))

        connection.commit()
        return author_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def add_publisher(name, city):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        publisher_id = _next_id(cursor, "Publisher", "PublisherID")
        cursor.execute("""
            INSERT INTO Publisher (PublisherID, PublisherName, City)
            VALUES (%s, %s, %s)
        """, (publisher_id, name.strip(), city or None))

        connection.commit()
        return publisher_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def add_category(name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        category_id = _next_id(cursor, "Category", "CategoryID")
        cursor.execute("""
            INSERT INTO Category (CategoryID, CategoryName)
            VALUES (%s, %s)
        """, (category_id, name.strip()))

        connection.commit()
        return category_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


# ==================================================
# 6. ISSUE BOOK
# ==================================================

def available_books():
    return _fetch_all("""
        SELECT b.BookID, b.Title,
               COUNT(bc.CopyID) AS AvailableCopies
        FROM Book b
        JOIN Book_Copy bc ON b.BookID = bc.BookID
        WHERE bc.CopyStatus = 'Available'
        GROUP BY b.BookID, b.Title
        ORDER BY b.Title
    """)


def issue_book(member_id, book_id):
    """Issue one available physical copy for 14 days."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        connection.start_transaction()

        cursor.execute("""
            SELECT MemberID FROM Member
            WHERE MemberID = %s
        """, (member_id,))

        if not cursor.fetchone():
            raise ValueError("Member does not exist.")

        cursor.execute("""
            SELECT CopyID
            FROM Book_Copy
            WHERE BookID = %s AND CopyStatus = 'Available'
            ORDER BY CopyID
            LIMIT 1 FOR UPDATE
        """, (book_id,))

        copy = cursor.fetchone()

        if not copy:
            raise ValueError("No available copies of this book.")

        copy_id = copy["CopyID"]
        loan_id = _next_id(cursor, "Loan", "LoanID")

        cursor.execute("""
            INSERT INTO Loan
                (LoanID, CopyID, MemberID, IssueDate,
                 DueDate, ReturnDate, FineAmount)
            VALUES (
                %s, %s, %s, CURDATE(),
                DATE_ADD(CURDATE(), INTERVAL 14 DAY),
                NULL, 0.00
            )
        """, (loan_id, copy_id, member_id))

        cursor.execute("""
            UPDATE Book_Copy
            SET CopyStatus = 'Issued'
            WHERE CopyID = %s AND CopyStatus = 'Available'
        """, (copy_id,))

        if cursor.rowcount != 1:
            raise ValueError("This copy is no longer available.")

        connection.commit()
        return loan_id

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


# ==================================================
# 7. RETURNS AND FINES
# ==================================================

def open_loans():
    return _fetch_all("""
        SELECT l.LoanID, l.CopyID, l.MemberID,
               l.IssueDate, l.DueDate,
               b.Title, m.MemberName, m.Email,
               GREATEST(DATEDIFF(CURDATE(), l.DueDate), 0) * 2
                   AS CurrentFine
        FROM Loan l
        JOIN Book_Copy bc ON l.CopyID = bc.CopyID
        JOIN Book b ON bc.BookID = b.BookID
        JOIN Member m ON l.MemberID = m.MemberID
        WHERE l.ReturnDate IS NULL
        ORDER BY l.DueDate
    """)


def return_book(loan_id):
    """Return an open loan and calculate Rs 2 per overdue day."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        connection.start_transaction()

        cursor.execute("""
            SELECT LoanID, CopyID, DueDate
            FROM Loan
            WHERE LoanID = %s AND ReturnDate IS NULL
            FOR UPDATE
        """, (loan_id,))

        loan = cursor.fetchone()

        if not loan:
            raise ValueError(
                "Open loan not found; it may already be returned."
            )

        today = date.today()
        overdue_days = max((today - loan["DueDate"]).days, 0)
        fine = overdue_days * 2

        cursor.execute("""
            UPDATE Loan
            SET ReturnDate = %s, FineAmount = %s
            WHERE LoanID = %s AND ReturnDate IS NULL
        """, (today, fine, loan_id))

        cursor.execute("""
            UPDATE Book_Copy
            SET CopyStatus = 'Available'
            WHERE CopyID = %s
        """, (loan["CopyID"],))

        connection.commit()

        return {
            "LoanID": loan_id,
            "ReturnDate": today,
            "OverdueDays": overdue_days,
            "FineAmount": fine
        }

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


# ==================================================
# 8. REPORTS
# ==================================================

def report_issued():
    return _fetch_all("""
        SELECT l.LoanID, b.Title, bc.CopyID,
               m.MemberName, m.Email,
               l.IssueDate, l.DueDate
        FROM Loan l
        JOIN Book_Copy bc ON l.CopyID = bc.CopyID
        JOIN Book b ON bc.BookID = b.BookID
        JOIN Member m ON l.MemberID = m.MemberID
        WHERE l.ReturnDate IS NULL
        ORDER BY l.DueDate
    """)


def report_overdue():
    return _fetch_all("""
        SELECT l.LoanID, b.Title, bc.CopyID,
               m.MemberName, m.Phone, l.DueDate,
               DATEDIFF(CURDATE(), l.DueDate) AS DaysOverdue,
               GREATEST(DATEDIFF(CURDATE(), l.DueDate), 0) * 2
                   AS CurrentFine
        FROM Loan l
        JOIN Book_Copy bc ON l.CopyID = bc.CopyID
        JOIN Book b ON bc.BookID = b.BookID
        JOIN Member m ON l.MemberID = m.MemberID
        WHERE l.ReturnDate IS NULL
          AND l.DueDate < CURDATE()
        ORDER BY l.DueDate
    """)


def report_most_issued():
    return _fetch_all("""
        SELECT b.BookID, b.Title,
               COUNT(l.LoanID) AS TimesIssued
        FROM Book b
        JOIN Book_Copy bc ON b.BookID = bc.BookID
        JOIN Loan l ON bc.CopyID = l.CopyID
        GROUP BY b.BookID, b.Title
        ORDER BY TimesIssued DESC, b.Title
    """)


def report_fines():
    return _fetch_all("""
        SELECT l.LoanID, m.MemberName, b.Title,
               l.IssueDate, l.DueDate,
               l.ReturnDate, l.FineAmount
        FROM Loan l
        JOIN Member m ON l.MemberID = m.MemberID
        JOIN Book_Copy bc ON l.CopyID = bc.CopyID
        JOIN Book b ON bc.BookID = b.BookID
        WHERE l.FineAmount > 0
        ORDER BY l.FineAmount DESC
    """)
