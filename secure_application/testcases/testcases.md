# Test Cases

## Test Case 1 - Member Registration

Input:
Name = nidhi
Email = nidhi2@gmail.com

Expected:
Member should be registered successfully.


## Test Case 2 - Add Book

Input:
Title = Python Programming
Author = John Smith

Expected:
Book should be added successfully.


## Test Case 3 - Search Book

Input:
Python

Expected:
Matching books should be displayed.


## Test Case 4 - Issue Book

Input:
Book ID = 1
Member ID = 1

Expected:
Book should be issued successfully.


## Test Case 5 - Return Book

Input:
Book ID = 1

Expected:
Book should be returned and fine should be calculated.


## Test Case 6 - SQL Injection

Input:
' OR 1=1 --

Expected:
SQL injection vulnerability should be demonstrated.


## Test Case 7 - Improper Input Validation

Input:
abc as Book ID

Expected:
Invalid input should be handled.


## Test Case 8 - Directory Traversal

Input:
../secret.txt

Expected:
Directory traversal vulnerability should be demonstrated.
