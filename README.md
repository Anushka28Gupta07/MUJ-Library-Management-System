# 📚 Library Management System (LMS)

A database-driven Library Management System built using **MySQL, Python, and Streamlit** for the CSC2131 RDBMS laboratory project. It demonstrates relational database design, data integrity, book circulation, member management, and reporting.

## 🌟 Key Features

* **Admin Login:** Demo administrator login for accessing the application.
* **Book Management:** Add, search, edit, and delete book records.
* **Member Management:** Register members, view details, update records, and delete eligible members.
* **Inventory Tracking:** Track individual physical copies and their availability.
* **Issue and Return:** Issue available copies, record returns, and calculate overdue fines.
* **Reports:** View issued books, overdue loans, most-issued books, and fine reports.
* **Master Data Management:** Add authors, publishers, and book categories.
* **Dashboard:** View library statistics and books by category.

## 🏛️ Database Architecture

The database is named `LibraryManagementDB` and contains eight relational tables:

1. **Publisher** — Stores publisher details.
2. **Category** — Organizes books by subject.
3. **Author** — Stores author information.
4. **Book** — Stores book details, ISBN, publication year, publisher, and category.
5. **Book_Author** — Links books and authors through a many-to-many relationship.
6. **Member** — Stores library member details.
7. **Book_Copy** — Tracks individual physical copies and their status.
8. **Loan** — Records issue dates, due dates, returns, and fines.

### Database Concepts Demonstrated

* Primary keys and foreign keys
* One-to-many and many-to-many relationships
* Referential integrity and data validation
* Normalized relational database design
* Transactions for book issue and return operations
* SQL queries for searching, reporting, and overdue tracking

## 💰 Library Rules

* Standard loan period: **14 days**
* Overdue fine: **₹2 per overdue day**
* Only available book copies can be issued.
* Book and member deletion is restricted when loan history exists.
* Returning a book updates the loan record and makes the physical copy available again.

## 📁 Repository Structure

```text
MUJ-Library-Management-System/
├── backend/
│   ├── __init__.py
│   ├── config.py
│   └── db.py
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── queries.sql
├── frontend/
│   ├── Banner.jpeg
│   ├── app.py
│   ├── books.py
│   ├── dashboard.py
│   ├── issue_return.py
│   ├── login.py
│   ├── master_data.py
│   ├── members.py
│   ├── reports.py
│   ├── search.py
│   ├── settings_page.py
│   └── styles.py
├── .gitignore
├── README.md
└── requirements.txt