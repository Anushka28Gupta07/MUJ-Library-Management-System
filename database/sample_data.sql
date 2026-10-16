USE LibraryManagementDB;

-- Publishers
INSERT INTO Publisher VALUES
(1, 'Pearson', 'Delhi'),
(2, 'McGraw Hill', 'Mumbai'),
(3, 'OReilly Media', 'Bangalore');

-- Categories
INSERT INTO Category VALUES
(1, 'Programming'),
(2, 'Mathematics'),
(3, 'Database Systems'),
(4, 'Fiction');

-- Authors
INSERT INTO Author VALUES
(1, 'Brian Kernighan', 'American'),
(2, 'Thomas Cormen', 'American'),
(3, 'Abraham Silberschatz', 'American'),
(4, 'Robert Martin', 'American'),
(5, 'R. D. Sharma', 'Indian');

-- Books
INSERT INTO Book VALUES
(101, 'The C Programming Language',
 '9780131103627', 1, 1, 1988),

(102, 'Introduction to Algorithms',
 '9780262046305', 2, 1, 2022),

(103, 'Database System Concepts',
 '9780078022159', 2, 3, 2019),

(104, 'Clean Code',
 '9780132350884', 1, 1, 2008),

(105, 'Mathematics for Engineers',
 '9789355012345', 1, 2, 2023),

(106, 'The Pragmatic Programmer',
 '9780135957059', 3, 1, 2019);

-- Book-author relationships
INSERT INTO Book_Author VALUES
(101, 1),
(102, 2),
(103, 3),
(104, 4),
(105, 5),
(106, 4);

-- Library members
INSERT INTO Member
(MemberID, MemberName, Email, Phone, JoinDate)
VALUES
(201, 'Ayushi Verma', 'ayushi@example.com',
 '9876543210', '2026-01-10'),

(202, 'Rahul Sharma', 'rahul@example.com',
 '9876543211', '2026-01-15'),

(203, 'Priya Singh', 'priya@example.com',
 '9876543212', '2026-02-01'),

(204, 'Arjun Mehta', 'arjun@example.com',
 '9876543213', '2026-02-12'),

(205, 'Neha Gupta', 'neha@example.com',
 '9876543214', '2026-03-05');

-- Physical book copies
INSERT INTO Book_Copy VALUES
(1001, 101, 'Issued'),
(1002, 101, 'Available'),
(1003, 102, 'Issued'),
(1004, 103, 'Available'),
(1005, 103, 'Issued'),
(1006, 104, 'Available'),
(1007, 105, 'Available'),
(1008, 106, 'Maintenance');

-- Loan history
INSERT INTO Loan VALUES
(5001, 1001, 201, '2026-09-01',
 '2026-09-15', NULL, 0.00),

(5002, 1003, 202, '2026-09-05',
 '2026-09-19', NULL, 0.00),

(5003, 1005, 203, '2026-08-01',
 '2026-08-15', '2026-08-20', 50.00),

(5004, 1002, 204, '2026-07-01',
 '2026-07-15', '2026-07-12', 0.00),

(5005, 1004, 205, '2026-06-01',
 '2026-06-15', '2026-06-18', 30.00);

-- Display all tables' data
SELECT * FROM Publisher;
SELECT * FROM Category;
SELECT * FROM Author;
SELECT * FROM Book;
SELECT * FROM Book_Author;
SELECT * FROM Member;
SELECT * FROM Book_Copy;
SELECT * FROM Loan;
