# 📚 Library Management System (LMS)

An enterprise-grade, normalized relational database management system built with **MySQL**, **Python**, and a modular **Streamlit** frontend. Designed for academic demonstration of relational integrity constraints, ACID transactions, and role-based library circulation.

---

## 🌟 Key Features

- **Role-Based Authentication:** Distinct portal sessions for Administrators/Librarians and Members.
- **Dynamic Catalog Management:** Real-time catalog view, multi-author book registration, and edition tracking.
- **Physical Inventory & Copy Tracking:** Tracks specific book copy IDs and their discrete circulation lifecycles (`Available`, `Issued`, `Maintenance`, `Lost`, `Damaged`).
- **Circulation Management:** Multi-step loan dispatching, automated due date enforcement, and return reconciliation.
- **Auditing & Advanced Reports:** Live audit tables for overdue loans, lost inventory replacement fees, and circulation analytics.
- **Adaptive UI:** Responsive portal supporting both Light and Dark display modes with high-contrast data visualization.

---

## 🏛️ Database Architecture & Normalization

The relational backend is decomposed to **Third Normal Form (3NF)** across 8 tables to eliminate data redundancy and anomalies:

1. **`Publisher`** — Maintains unique publication entities (`PublisherID`, `PublisherName`, `Address`, `Contact`).
2. **`Category`** — Subject classifications (`CategoryID`, `CategoryName`, `ShelfLocation`).
3. **`Author`** — Individual author biographical records (`AuthorID`, `AuthorName`, `Nationality`).
4. **`Book`** — Abstract conceptual book title (`BookID`, `Title`, `ISBN` [UNIQUE], `PublicationYear`, `PublisherID` [FK], `CategoryID` [FK]).
5. **`Book_Author`** — Resolves the Many-to-Many ($M:N$) relationship between `Book` and `Author`.
6. **`Book_Copy`** — Tracks discrete physical barcode items ($1:N$ from `Book`) and their status (`CopyID`, `BookID` [FK], `CopyStatus`).
7. **`Member`** — Reader profile registry (`MemberID`, `FullName`, `Email` [UNIQUE], `Phone`, `MembershipDate`).
8. **`Loan`** — Records borrowing events and tracks ACID circulation transactions (`LoanID`, `CopyID` [FK], `MemberID` [FK], `IssueDate`, `DueDate`, `ReturnDate`, `FineAmount`).

### Integrity Constraints & ACID Enforcement
- **Domain Constraints:** `PublicationYear BETWEEN 1450 AND 2100`, `FineAmount >= 0.00`.
- **Referential Integrity:** Foreign keys enforce strict cascades on categorization and restrictions on active loan deletions.
- **ACID Transactions:** Checkout and copy disposal operations use explicit transaction boundaries (`BEGIN` ... `COMMIT` / `ROLLBACK`) to prevent inconsistent copy states.

---

## 📁 Repository Structure

```text
library-management-system/
│
├── database/
│   ├── schema.sql           # DDL: Table definitions, constraints, foreign keys
│   ├── sample_database.sql  # DML: Mock seed dataset for academic demo
│   └── queries.sql          # Core analytical, audit, and search SQL queries
│
├── backend/
│   ├── config.py            # MySQL database connection parameters
│   ├── db.py                # Database transactions, stored procedures, & queries
│   └── __init__.py
│
├── frontend/
│   ├── app.py               # Main application routing and navigation logic
│   ├── login.py             # Authentication screen with custom background
│   ├── styles.py            # Adaptive theme engine (Dark / Light mode CSS)
│   ├── dashboard.py         # Summary metrics and catalog visualization
│   ├── books.py             # Book catalog CRUD & Lost/Damaged Copy tracking
│   ├── members.py           # Member roster registration and profile updates
│   ├── issue_return.py      # Circulation desk (Borrowing & Return transactions)
│   ├── search.py            # Multi-attribute catalog lookup engine
│   ├── reports.py           # Overdue audits, fines, and borrowing reports
│   └── master_data.py       # Master author, publisher, and category tables
│
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation