-- ========================================================= -- LIBRARY MANAGEMENT SYSTEM -- File: database/queries.sql -- Database: MySQL -- Purpose: Queries for Python backend functionality -- =========================================================

USE LibraryManagementDB;

-- ========================================================= -- 1. DASHBOARD -- =========================================================

-- Total book titles
SELECT COUNT(*) AS titles FROM Book;

-- Total physical copies 
SELECT COUNT(*) AS copies FROM Book_Copy;

-- Copies currently issued 
SELECT COUNT(*) AS issued FROM Book_Copy WHERE CopyStatus = 'Issued';

-- Total library members 
SELECT COUNT(*) AS members FROM Member;

-- Number of book titles in each category 
SELECT c.CategoryID, c.CategoryName, COUNT(b.BookID) AS book_count FROM Category c LEFT JOIN Book b ON c.CategoryID = b.CategoryID GROUP BY c.CategoryID, c.CategoryName ORDER BY c.CategoryName;

-- ========================================================= -- 2. BOOKS -- =========================================================

-- List all books with publisher, category, authors and copy counts 
SELECT b.BookID, b.Title, b.ISBN, b.PublicationYear, p.PublisherName, c.CategoryName, GROUP_CONCAT(DISTINCT a.AuthorName ORDER BY a.AuthorName SEPARATOR ', ') AS Authors, COUNT(DISTINCT bc.CopyID) AS TotalCopies, COUNT(DISTINCT CASE WHEN bc.CopyStatus = 'Available' THEN bc.CopyID END) AS AvailableCopies FROM Book b JOIN Publisher p ON b.PublisherID = p.PublisherID JOIN Category c ON b.CategoryID = c.CategoryID LEFT JOIN Book_Author ba ON b.BookID = ba.BookID LEFT JOIN Author a ON ba.AuthorID = a.AuthorID LEFT JOIN Book_Copy bc ON b.BookID = bc.BookID GROUP BY b.BookID, b.Title, b.ISBN, b.PublicationYear, p.PublisherName, c.CategoryName ORDER BY b.Title;

-- Search by title, author or category -- Python supplies the same search term three times. 
SELECT DISTINCT b.BookID, b.Title, b.ISBN, b.PublicationYear, p.PublisherName, c.CategoryName FROM Book b JOIN Publisher p ON b.PublisherID = p.PublisherID JOIN Category c ON b.CategoryID = c.CategoryID LEFT JOIN Book_Author ba ON b.BookID = ba.BookID LEFT JOIN Author a ON ba.AuthorID = a.AuthorID WHERE b.Title LIKE %s OR a.AuthorName LIKE %s OR c.CategoryName LIKE %s ORDER BY b.Title;

-- Publisher dropdown 
SELECT PublisherID, PublisherName FROM Publisher ORDER BY PublisherName;

-- Category dropdown 
SELECT CategoryID, CategoryName FROM Category ORDER BY CategoryName;

-- Author multi-select 
SELECT AuthorID, AuthorName FROM Author ORDER BY AuthorName;

-- Book selection dropdown 
SELECT BookID, Title FROM Book ORDER BY Title;

-- Available book titles for issuing 
SELECT b.BookID, b.Title, COUNT(bc.CopyID) AS AvailableCopies FROM Book b JOIN Book_Copy bc ON b.BookID = bc.BookID WHERE bc.CopyStatus = 'Available' GROUP BY b.BookID, b.Title HAVING COUNT(bc.CopyID) > 0 ORDER BY b.Title;

-- List book titles for editing 
SELECT BookID, Title FROM Book ORDER BY Title;

-- Update book details 
UPDATE Book SET Title = %s, PublicationYear = %s WHERE BookID = %s;

-- Check whether a book has loan history before deletion 
SELECT COUNT(*) AS loan_count FROM Loan l JOIN Book_Copy bc ON l.CopyID = bc.CopyID WHERE bc.BookID = %s;

-- Delete author relationships only after confirming -- that the book has no loan history. 
DELETE FROM Book_Author WHERE BookID = %s;

-- Delete associated copies only when they have no loan history. 
DELETE FROM Book_Copy WHERE BookID = %s AND NOT EXISTS ( SELECT 1 FROM Loan WHERE Loan.CopyID = Book_Copy.CopyID );

-- Delete book only after checking loan history and -- removing dependent records in the correct order. 
DELETE FROM Book WHERE BookID = %s AND NOT EXISTS ( SELECT 1 FROM Book_Copy bc JOIN Loan l ON l.CopyID = bc.CopyID WHERE bc.BookID = Book.BookID );

-- ========================================================= -- 3. MEMBERS -- =========================================================

-- List all members 
SELECT MemberID, MemberName, Email, Phone, JoinDate FROM Member ORDER BY MemberName;

-- Member selection dropdown 
SELECT MemberID, MemberName FROM Member ORDER BY MemberName;

-- Get one member's details 
SELECT MemberID, MemberName, Email, Phone, JoinDate FROM Member WHERE MemberID = %s;

-- Update member details 
UPDATE Member SET MemberName = %s, Email = %s, Phone = %s WHERE MemberID = %s;

-- Check whether a member has loan history 
SELECT COUNT(*) AS loan_count FROM Loan WHERE MemberID = %s;

-- Delete a member only if no loan history exists 
DELETE FROM Member WHERE MemberID = %s AND NOT EXISTS ( SELECT 1 FROM Loan WHERE Loan.MemberID = Member.MemberID );

-- ========================================================= -- 4. AUTHORS, PUBLISHERS AND CATEGORIES -- =========================================================

-- Add author 
INSERT INTO Author (AuthorID, AuthorName, Nationality) VALUES (%s, %s, %s);

-- Add publisher 
INSERT INTO Publisher (PublisherID, PublisherName, City) VALUES (%s, %s, %s);

-- Add category 
INSERT INTO Category (CategoryID, CategoryName) VALUES (%s, %s);

-- ========================================================= -- 5. ISSUE BOOK -- Execute the following steps inside one transaction. -- Select and lock one available physical copy. -- =========================================================

SELECT CopyID FROM Book_Copy WHERE BookID = %s AND CopyStatus = 'Available' ORDER BY CopyID LIMIT 1 FOR UPDATE;

-- Create a loan with a 14-day loan period. 
-- Python must generate a unique LoanID. 
INSERT INTO Loan (LoanID, CopyID, MemberID, IssueDate, DueDate, FineAmount) VALUES (%s, %s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), 0.00);

-- Mark the selected physical copy as issued. 
UPDATE Book_Copy SET CopyStatus = 'Issued' WHERE CopyID = %s AND CopyStatus = 'Available';

-- ========================================================= -- 6. RETURN BOOK -- =========================================================

-- List all open loans 
SELECT l.LoanID, l.CopyID, l.MemberID, l.IssueDate, l.DueDate, b.Title, m.MemberName FROM Loan l JOIN Book_Copy bc ON l.CopyID = bc.CopyID JOIN Book b ON bc.BookID = b.BookID JOIN Member m ON l.MemberID = m.MemberID WHERE l.ReturnDate IS NULL ORDER BY l.DueDate;

-- Calculate fine at Rs 2 per overdue calendar day. 
-- Use the actual return date in Python when returning a book. 
SELECT LoanID, GREATEST(DATEDIFF(CURDATE(), DueDate), 0) * 2 AS FineAmount FROM Loan WHERE LoanID = %s AND ReturnDate IS NULL;

-- Mark loan returned and save calculated fine. 
UPDATE Loan SET ReturnDate = CURDATE(), FineAmount = %s WHERE LoanID = %s AND ReturnDate IS NULL;

-- Mark physical copy available again. 
UPDATE Book_Copy SET CopyStatus = 'Available' WHERE CopyID = %s;

-- ========================================================= -- 7. REPORTS -- =========================================================

-- Report: currently issued books 
SELECT l.LoanID, b.Title, bc.CopyID, m.MemberName, m.Email, l.IssueDate, l.DueDate FROM Loan l JOIN Book_Copy bc ON l.CopyID = bc.CopyID JOIN Book b ON bc.BookID = b.BookID JOIN Member m ON l.MemberID = m.MemberID WHERE l.ReturnDate IS NULL ORDER BY l.DueDate;

-- Report: overdue books not yet returned 
SELECT l.LoanID, b.Title, bc.CopyID, m.MemberName, m.Phone, l.DueDate, DATEDIFF(CURDATE(), l.DueDate) AS DaysOverdue, GREATEST(DATEDIFF(CURDATE(), l.DueDate), 0) * 2 AS CurrentFine FROM Loan l JOIN Book_Copy bc ON l.CopyID = bc.CopyID JOIN Book b ON bc.BookID = b.BookID JOIN Member m ON l.MemberID = m.MemberID WHERE l.ReturnDate IS NULL AND l.DueDate < CURDATE() ORDER BY l.DueDate;

-- Report: most-issued book titles 
SELECT b.BookID, b.Title, COUNT(l.LoanID) AS TimesIssued FROM Book b JOIN Book_Copy bc ON bc.BookID = b.BookID JOIN Loan l ON l.CopyID = bc.CopyID GROUP BY b.BookID, b.Title ORDER BY TimesIssued DESC, b.Title;

-- Report: recorded fines 
SELECT l.LoanID, m.MemberName, b.Title, l.IssueDate, l.DueDate, l.ReturnDate, l.FineAmount FROM Loan l JOIN Member m ON l.MemberID = m.MemberID JOIN Book_Copy bc ON l.CopyID = bc.CopyID JOIN Book b ON bc.BookID = b.BookID WHERE l.FineAmount > 0 ORDER BY l.FineAmount DESC;

-- ========================================================= -- END OF QUERIES -- =========================================================
