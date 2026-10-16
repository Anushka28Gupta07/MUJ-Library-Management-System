-- ==========================================
-- LIBRARY MANAGEMENT SYSTEM
-- MUJ CSC2131 RDBMS LAB PROJECT
-- Database: MySQL
-- ==========================================

CREATE DATABASE IF NOT EXISTS LibraryManagementDB;

USE LibraryManagementDB;


-- ==========================================
-- 1. PUBLISHER TABLE
-- ==========================================

CREATE TABLE Publisher (
    PublisherID INT PRIMARY KEY,
    PublisherName VARCHAR(100) NOT NULL,
    City VARCHAR(50)
);


-- ==========================================
-- 2. CATEGORY TABLE
-- ==========================================

CREATE TABLE Category (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(50) NOT NULL UNIQUE
);


-- ==========================================
-- 3. AUTHOR TABLE
-- ==========================================

CREATE TABLE Author (
    AuthorID INT PRIMARY KEY,
    AuthorName VARCHAR(100) NOT NULL,
    Nationality VARCHAR(50)
);


-- ==========================================
-- 4. BOOK TABLE
-- ==========================================

CREATE TABLE Book (
    BookID INT PRIMARY KEY,
    Title VARCHAR(150) NOT NULL,
    ISBN VARCHAR(20) NOT NULL UNIQUE,
    PublisherID INT NOT NULL,
    CategoryID INT NOT NULL,
    PublicationYear INT,

    CONSTRAINT fk_book_publisher
        FOREIGN KEY (PublisherID)
        REFERENCES Publisher(PublisherID),

    CONSTRAINT fk_book_category
        FOREIGN KEY (CategoryID)
        REFERENCES Category(CategoryID),

    CONSTRAINT chk_publication_year
        CHECK (
            PublicationYear IS NULL
            OR PublicationYear BETWEEN 1450 AND 2100
        )
);


-- ==========================================
-- 5. BOOK_AUTHOR TABLE
-- Resolves many-to-many relationship
-- ==========================================

CREATE TABLE Book_Author (
    BookID INT,
    AuthorID INT,

    PRIMARY KEY (BookID, AuthorID),

    CONSTRAINT fk_ba_book
        FOREIGN KEY (BookID)
        REFERENCES Book(BookID),

    CONSTRAINT fk_ba_author
        FOREIGN KEY (AuthorID)
        REFERENCES Author(AuthorID)
);


-- ==========================================
-- 6. MEMBER TABLE
-- ==========================================

CREATE TABLE Member (
    MemberID INT PRIMARY KEY,
    MemberName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(15),
    JoinDate DATE NOT NULL DEFAULT (CURRENT_DATE)
);


-- ==========================================
-- 7. BOOK_COPY TABLE
-- Each physical copy is tracked separately
-- ==========================================

CREATE TABLE Book_Copy (
    CopyID INT PRIMARY KEY,
    BookID INT NOT NULL,
    CopyStatus VARCHAR(20) NOT NULL DEFAULT 'Available',

    CONSTRAINT fk_copy_book
        FOREIGN KEY (BookID)
        REFERENCES Book(BookID),

    CONSTRAINT chk_copy_status
        CHECK (
            CopyStatus IN (
                'Available',
                'Issued',
                'Maintenance'
            )
        )
);


-- ==========================================
-- 8. LOAN TABLE
-- Tracks issue, return and fine details
-- ==========================================

CREATE TABLE Loan (
    LoanID INT PRIMARY KEY,
    CopyID INT NOT NULL,
    MemberID INT NOT NULL,
    IssueDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE DEFAULT NULL,
    FineAmount DECIMAL(8,2) NOT NULL DEFAULT 0.00,

    CONSTRAINT fk_loan_copy
        FOREIGN KEY (CopyID)
        REFERENCES Book_Copy(CopyID),

    CONSTRAINT fk_loan_member
        FOREIGN KEY (MemberID)
        REFERENCES Member(MemberID),

    CONSTRAINT chk_loan_dates
        CHECK (
            DueDate >= IssueDate
            AND (
                ReturnDate IS NULL
                OR ReturnDate >= IssueDate
            )
        ),

    CONSTRAINT chk_fine_amount
        CHECK (FineAmount >= 0)
);
