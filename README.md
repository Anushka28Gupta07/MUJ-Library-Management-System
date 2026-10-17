
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
library-management-system/
├── backend/
│   ├── __init__.py
│   ├── config.py
│   └── db.py
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── queries.sql
├── frontend/
│   └── app.py
└── requirements.txt
```

## 🛠️ Technologies Used

* **Database:** MySQL
* **Programming Language:** Python
* **Frontend:** Streamlit
* **Database Connector:** MySQL Connector/Python
* **Version Control:** Git and GitHub

## 🚀 Setup and Installation

### Prerequisites

Install Python and MySQL Server on your computer.

### 1. Clone the repository

```bash
git clone https://github.com/vrindainink/library-management-system.git
cd library-management-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create and populate the database

Open MySQL Workbench or a MySQL command-line client and execute the SQL files in this order:

1. `database/schema.sql`
2. `database/sample_data.sql`

Execute `database/queries.sql` separately when you want to explore the project's SQL queries.

### 4. Configure the database connection

The application reads these environment variables:

* `DB_HOST` — defaults to `localhost`
* `DB_USER` — defaults to `root`
* `DB_PASSWORD` — defaults to an empty password
* `DB_NAME` — defaults to `LibraryManagementDB`

Set them to match your local MySQL configuration.

### 5. Launch the application

Run this command from the repository root:

```bash
streamlit run frontend/app.py
```

Streamlit will provide a local URL where you can access the application.

## 🔐 Demo Login

* **Username:** `admin`
* **Password:** `admin123`

These are demonstration credentials defined in the application code. Change them before using the application beyond a classroom demonstration.

## 🎓 Project Purpose

This project demonstrates the practical application of relational database concepts, SQL operations, integrity constraints, transaction handling, and Python–MySQL integration in a library environment.

---

**Academic Project:** CSC2131 — Relational Database Management Systems (RDBMS)