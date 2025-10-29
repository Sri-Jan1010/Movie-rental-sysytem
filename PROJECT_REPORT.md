# MOVIE RENTAL MANAGEMENT SYSTEM
## Project Report

---

**Victorian Institute of Technology**  
**Course:** Developing Data Access Solution - Semester 2, 2025  
**Submission Date:** October 29, 2025

---

## TABLE OF CONTENTS

1. Executive Summary
2. Project Overview
3. System Architecture
4. Technical Specifications
5. Database Design
6. System Features
7. Implementation Details
8. Testing and Validation
9. User Manual
10. Conclusion and Future Enhancements
11. Appendices

---

## 1. EXECUTIVE SUMMARY

The Movie Rental Management System is a comprehensive desktop application developed using Python and MySQL to manage movie rental operations efficiently. The system provides an intuitive graphical user interface (GUI) for managing movies, customers, and rental transactions with features including:

- **User Authentication:** Secure employee login system
- **CRUD Operations:** Complete Create, Read, Update, Delete functionality for movies and customers
- **Rental Management:** Issue and return movies with automatic late fee calculation
- **Advanced Search:** Multi-criteria search across all entities
- **Reporting:** Excel export with data visualization and analytics
- **Data Integrity:** Foreign key constraints and validation

The system successfully addresses the business requirements of a modern movie rental store while maintaining data consistency and providing comprehensive reporting capabilities.

---

## 2. PROJECT OVERVIEW

### 2.1 Purpose and Scope

The Movie Rental Management System is designed to streamline rental operations for video rental businesses. The system replaces manual record-keeping with an automated, database-driven solution that:

- Tracks movie inventory and availability
- Manages customer information and rental history
- Calculates rental fees and late charges automatically
- Generates reports for business analytics
- Ensures data accuracy through validation and constraints

### 2.2 Project Objectives

1. Develop a user-friendly desktop application using Python Tkinter
2. Implement secure MySQL database with proper normalization
3. Provide comprehensive CRUD operations for all entities
4. Enable efficient search and filtering capabilities
5. Generate business reports with data visualization
6. Calculate late fees automatically based on due dates
7. Ensure data integrity and security

### 2.3 Target Users

- **Store Managers:** Access to all features including reports
- **Employees:** Handle daily rental operations
- **Administrators:** System configuration and user management

---

## 3. SYSTEM ARCHITECTURE

### 3.1 Architecture Overview

The system follows a **three-tier architecture**:

```
┌─────────────────────────────────────┐
│     Presentation Layer (GUI)        │
│   • Tkinter-based Interface         │
│   • User Input Validation           │
│   • Data Visualization              │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│      Business Logic Layer           │
│   • Movie Management                │
│   • Customer Management             │
│   • Rental Management               │
│   • Report Generation               │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│       Data Access Layer             │
│   • MySQL Database Connector        │
│   • Query Execution                 │
│   • Transaction Management          │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│         Database Layer              │
│   • MySQL 5.7+                      │
│   • Normalized Schema               │
│   • Stored Data                     │
└─────────────────────────────────────┘
```

### 3.2 Component Diagram

**Core Modules:**

1. **main.py** - Application entry point and navigation
2. **db_config.py** - Database configuration and connection management
3. **movie_management.py** - Movie CRUD operations
4. **customer_management.py** - Customer CRUD operations
5. **rental_management.py** - Rental transactions (issue/return)
6. **reports.py** - Report generation and visualization

---

## 4. TECHNICAL SPECIFICATIONS

### 4.1 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Programming Language | Python | 3.8+ |
| Database | MySQL | 5.7+ |
| GUI Framework | Tkinter | Built-in |
| Database Connector | mysql-connector-python | 8.0+ |
| Data Processing | Pandas | 2.1+ |
| Visualization | Matplotlib | 3.5+ |
| Excel Export | OpenPyXL | 3.0+ |
| Operating System | Windows/Linux/Mac | Cross-platform |

### 4.2 System Requirements

**Minimum Requirements:**
- Processor: Intel Core i3 or equivalent
- RAM: 4 GB
- Storage: 500 MB free space
- Display: 1366x768 resolution
- Python 3.8 or higher
- MySQL Server 5.7 or higher

**Recommended Requirements:**
- Processor: Intel Core i5 or higher
- RAM: 8 GB or higher
- Storage: 1 GB free space
- Display: 1920x1080 resolution
- Python 3.10+
- MySQL Server 8.0+

### 4.3 Dependencies

All Python dependencies are managed through `requirements.txt`:

```
mysql-connector-python>=8.0.0
pandas>=2.1.0
numpy>=1.24.0
matplotlib>=3.5.0
openpyxl>=3.0.0
pillow>=10.0.0
python-dateutil>=2.8.0
```

---

## 5. DATABASE DESIGN

### 5.1 Entity-Relationship Diagram (ERD)

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  EMPLOYEES   │         │   CUSTOMER   │         │   MOVIES     │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ EmployeeID PK│         │ CustomerID PK│         │ MovieID   PK │
│ FirstName    │         │ Title        │         │ Title        │
│ LastName     │         │ FirstName    │         │ ReleaseYear  │
│ Email        │         │ LastName     │         │ Genre        │
│ Password     │         │ Phone        │         │ RentalPrice  │
└──────────────┘         │ Email        │         │ ProducerID FK│
                         └──────────────┘         └──────────────┘
                                │                         │
                                │                         │
                                └────────┬────────────────┘
                                         │
                                         ↓
                                ┌──────────────┐
                                │  ISSUETRAN   │
                                ├──────────────┤
                                │ IssueID   PK │
                                │ CustomerID FK│
                                │ MovieID   FK │
                                │ IssueDate    │
                                │ dueDate      │
                                │ ReturnDate   │
                                └──────────────┘

┌──────────────┐
│  PRODUCERS   │
├──────────────┤
│ ProducerID PK│
│ Name         │
│ Country      │
└──────────────┘
```

### 5.2 Database Schema

**5.2.1 employees Table**
```sql
CREATE TABLE employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255) NOT NULL
);
```

**5.2.2 customer Table**
```sql
CREATE TABLE customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(10),
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    CONSTRAINT chk_phone CHECK (LENGTH(Phone) = 10)
);
```

**5.2.3 producers Table**
```sql
CREATE TABLE producers (
    ProducerID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Country VARCHAR(50)
);
```

**5.2.4 movies Table**
```sql
CREATE TABLE movies (
    MovieID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(200) NOT NULL,
    ReleaseYear INT,
    Genre VARCHAR(50),
    RentalPrice DECIMAL(10,2) NOT NULL,
    ProducerID INT,
    FOREIGN KEY (ProducerID) REFERENCES producers(ProducerID),
    CONSTRAINT chk_genre CHECK (Genre IN ('Action', 'Comedy', 'Drama'))
);
```

**5.2.5 issuetran Table (Rental Transactions)**
```sql
CREATE TABLE issuetran (
    IssueID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT NOT NULL,
    MovieID INT NOT NULL,
    IssueDate DATE NOT NULL,
    dueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID),
    FOREIGN KEY (MovieID) REFERENCES movies(MovieID)
);
```

### 5.3 Database Normalization

The database follows **Third Normal Form (3NF)**:

- **1NF:** All tables have atomic values with no repeating groups
- **2NF:** All non-key attributes are fully dependent on primary key
- **3NF:** No transitive dependencies exist

### 5.4 Relationships and Constraints

1. **One-to-Many:** Producer → Movies (One producer can produce many movies)
2. **Many-to-Many:** Customer ↔ Movies (through issuetran junction table)
3. **Foreign Key Constraints:** Maintain referential integrity
4. **Check Constraints:** Validate data at database level
5. **NOT NULL Constraints:** Ensure required fields are populated

---

## 6. SYSTEM FEATURES

### 6.1 User Authentication

**Login System:**
- Employee ID and password authentication
- Password hashing using SHA-256
- Session management
- Secure logout functionality

**Security Features:**
- Encrypted password storage
- SQL injection prevention through parameterized queries
- Input validation and sanitization

### 6.2 Movie Management

**Features:**
1. **Add Movie**
   - Auto-generated Movie ID
   - Title, release year, genre selection
   - Rental price configuration
   - Producer assignment

2. **Update Movie**
   - Modify all movie attributes
   - Price adjustments
   - Producer reassignment

3. **Delete Movie**
   - Validation check for active rentals
   - Confirmation dialog
   - Cascade considerations

4. **Search Movies**
   - Search by title (partial match)
   - Filter by genre
   - Filter by release year
   - Price range filtering

5. **Generate Reports**
   - Complete movie inventory
   - Statistics by genre
   - Top 10 most rented movies
   - Excel export with charts

### 6.3 Customer Management

**Features:**
1. **Add Customer**
   - Auto-generated Customer ID
   - Title selection (Mr/Mrs/Ms/Dr/Prof)
   - Name and contact information
   - Phone validation (10 digits)
   - Email validation

2. **Update Customer**
   - Modify contact details
   - Update email and phone
   - Change title

3. **Delete Customer**
   - Check for active rentals
   - Prevent deletion if rentals exist
   - Confirmation required

4. **Search Customers**
   - Search by name (first or last)
   - Search by Customer ID
   - View all customers

5. **Customer Reports**
   - Complete customer database
   - Top customers by rental count
   - Customers with pending late fees

### 6.4 Rental Management

**6.4.1 View Rentals**
- List all rental transactions
- Status indicators (Active/Returned/Overdue)
- Calculated late fees
- Multi-criteria search:
  - Customer name
  - Movie title
  - Issue date
  - Rental status

**6.4.2 Rent a Movie**
- Customer selection dropdown
- Available movies listing
- Rental period configuration (1-30 days)
- Automatic due date calculation
- Availability check

**6.4.3 Return a Movie**
- Active rental selection
- Rental details display
- Automatic late fee calculation ($2/day)
- Return date recording
- Late fee notification

**6.4.4 Late Fee Calculation**
```python
Late Fee Formula:
IF (Return Date > Due Date):
    Days Late = Return Date - Due Date
    Late Fee = Days Late × $2.00
ELSE:
    Late Fee = $0.00
```

### 6.5 Reporting and Analytics

**6.5.1 Movie Reports**
- Complete inventory listing
- Genre distribution statistics
- Top performing movies
- Average pricing by genre
- Visual charts (pie, bar, horizontal bar)

**6.5.2 Customer Reports**
- Customer database export
- Top 10 customers by rental count
- Active rentals per customer
- Pending late fees summary

**6.5.3 Rental Reports**
- Currently rented movies with contact info
- Overdue rentals with late fees
- Statistics by genre and producer
- Revenue analysis
- Multiple Excel sheets with formatted data

**6.5.4 Data Visualization**
- Interactive charts using Matplotlib
- Genre distribution pie charts
- Rental trends bar graphs
- Top movies horizontal bar chart
- Embedded in Tkinter windows

---

## 7. IMPLEMENTATION DETAILS

### 7.1 Application Flow

```
START → Login Screen
    ↓ [Authenticate]
Management Options Menu
    ├→ Movie Management
    │   ├→ Add/Update/Delete Movies
    │   ├→ Search Movies
    │   └→ Generate Movie Report
    ├→ Customer Management
    │   ├→ Add/Update/Delete Customers
    │   ├→ Search Customers
    │   └→ Generate Customer Report
    └→ Rental Management
        ├→ View All Rentals
        ├→ Rent a Movie
        ├→ Return a Movie
        └→ Generate Rental Report
    ↓ [Logout]
END → Return to Login
```

### 7.2 Code Structure

**7.2.1 main.py - Entry Point**
```python
Classes:
- LoginWindow: Authentication interface
- ManagementOptions: Main menu navigation
- MainApplication: Container for management modules
```

**7.2.2 db_config.py - Database Layer**
```python
Class: DatabaseConfig
Methods:
- get_connection(): Create DB connection
- execute_query(): INSERT/UPDATE/DELETE
- fetch_data(): SELECT multiple rows
- fetch_one(): SELECT single row
- authenticate_user(): Login validation
- hash_password(): SHA-256 encryption
```

**7.2.3 movie_management.py**
```python
Class: MovieManagement
Methods:
- load_movies(): Populate treeview
- add_movie(): Insert new movie
- update_movie(): Modify movie details
- delete_movie(): Remove movie with validation
- search_movies(): Multi-criteria search
- generate_report(): Create Excel report
```

**7.2.4 customer_management.py**
```python
Class: CustomerManagement
Methods:
- load_customers(): Display customers
- add_customer(): Insert with validation
- update_customer(): Modify details
- delete_customer(): Remove with rental check
- search_customers(): Search functionality
- validate_phone(): 10-digit validation
- validate_email(): Email format check
```

**7.2.5 rental_management.py**
```python
Class: RentalManagement
Methods:
- show_view_rentals(): Display all rentals
- show_rent_movie(): Issue interface
- show_return_movie(): Return interface
- issue_movie(): Create rental transaction
- process_return(): Calculate late fee & return
- calculate_late_fee(): Fee computation
- load_active_rentals(): Get unreturned movies
```

**7.2.6 reports.py**
```python
Class: ReportGenerator
Static Methods:
- generate_movie_report(): Movie Excel export
- generate_customer_report(): Customer Excel
- generate_rental_report(): Rental statistics
- show_movie_visualization(): Charts
- show_rental_visualization(): Analytics
```

### 7.3 Key Algorithms

**7.3.1 Late Fee Calculation**
```python
def calculate_late_fee(due_date, return_date):
    if return_date is None:
        return_date = datetime.now().date()
    
    late_days = max(0, (return_date - due_date).days)
    late_fee = late_days * 2.0  # $2 per day
    
    return late_days, late_fee
```

**7.3.2 Movie Availability Check**
```python
def is_movie_available(movie_id):
    query = """
        SELECT COUNT(*) as count 
        FROM issuetran 
        WHERE MovieID = %s AND ReturnDate IS NULL
    """
    result = db.fetch_one(query, (movie_id,))
    return result['count'] == 0
```

**7.3.3 Auto-ID Generation**
```python
def get_next_id(table_name, id_column):
    query = f"""
        SELECT COALESCE(MAX({id_column}), 0) + 1 as NextID 
        FROM {table_name}
    """
    result = db.fetch_one(query)
    return result['NextID']
```

### 7.4 Error Handling

```python
try:
    # Database operation
    connection = db.get_connection()
    cursor.execute(query, params)
    connection.commit()
    return True
except mysql.connector.Error as e:
    # Log error
    print(f"Database Error: {e}")
    # Rollback transaction
    connection.rollback()
    # Show user-friendly message
    messagebox.showerror("Error", "Operation failed")
    return False
finally:
    # Clean up resources
    if connection.is_connected():
        cursor.close()
        connection.close()
```

---

## 8. TESTING AND VALIDATION

### 8.1 Test Cases

**8.1.1 Login Module**
| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TC-L01 | Valid login | Valid ID & password | Access granted | ✓ Pass |
| TC-L02 | Invalid password | Valid ID, wrong password | Error message | ✓ Pass |
| TC-L03 | Empty fields | Blank ID/password | Validation error | ✓ Pass |
| TC-L04 | SQL injection | SQL code in input | Prevented | ✓ Pass |

**8.1.2 Movie Management**
| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TC-M01 | Add movie | Valid movie data | Movie added | ✓ Pass |
| TC-M02 | Update movie | Modified data | Movie updated | ✓ Pass |
| TC-M03 | Delete rented movie | Movie with active rental | Error, delete prevented | ✓ Pass |
| TC-M04 | Search by title | Partial title | Matching movies shown | ✓ Pass |
| TC-M05 | Price validation | Negative price | Validation error | ✓ Pass |

**8.1.3 Customer Management**
| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TC-C01 | Add customer | Valid customer data | Customer added | ✓ Pass |
| TC-C02 | Phone validation | 9-digit phone | Validation error | ✓ Pass |
| TC-C03 | Email validation | Invalid email | Validation error | ✓ Pass |
| TC-C04 | Delete with rentals | Customer with active rental | Error, delete prevented | ✓ Pass |

**8.1.4 Rental Management**
| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TC-R01 | Rent available movie | Valid customer & movie | Rental created | ✓ Pass |
| TC-R02 | Rent unavailable movie | Already rented movie | Not in dropdown | ✓ Pass |
| TC-R03 | Return on time | Return before due date | $0 late fee | ✓ Pass |
| TC-R04 | Return late | Return 5 days late | $10 late fee | ✓ Pass |
| TC-R05 | Search by status | Filter "Overdue" | Only overdue shown | ✓ Pass |

**8.1.5 Reporting Module**
| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TC-RP01 | Generate movie report | Click report button | Excel file created | ✓ Pass |
| TC-RP02 | Generate customer report | Click report button | Excel file with sheets | ✓ Pass |
| TC-RP03 | Generate rental report | Click report button | Multiple sheets created | ✓ Pass |
| TC-RP04 | Show visualization | Generate report | Charts displayed | ✓ Pass |

### 8.2 Validation Rules

**Input Validation:**
- Phone: Exactly 10 digits
- Email: Must contain @ and .
- Price: Positive decimal number
- Year: Integer between 1900-2100
- Dates: Valid date format (YYYY-MM-DD)
- Required fields: Not empty

**Business Rules:**
- Cannot delete movie with active rentals
- Cannot delete customer with active rentals
- Cannot rent already rented movie
- Rental period: 1-30 days
- Late fee: $2 per day

### 8.3 Test Results Summary

| Module | Total Tests | Passed | Failed | Pass Rate |
|--------|-------------|--------|--------|-----------|
| Login | 4 | 4 | 0 | 100% |
| Movie Management | 5 | 5 | 0 | 100% |
| Customer Management | 4 | 4 | 0 | 100% |
| Rental Management | 5 | 5 | 0 | 100% |
| Reporting | 4 | 4 | 0 | 100% |
| **TOTAL** | **22** | **22** | **0** | **100%** |

---

## 9. USER MANUAL

### 9.1 Installation Guide

**Step 1: Install Prerequisites**
1. Download and install Python 3.8+ from python.org
2. Download and install MySQL Server from mysql.com
3. During MySQL installation, set root password

**Step 2: Setup Project**
1. Extract project folder to desired location
2. Open Command Prompt in project directory
3. Run: `pip install -r requirements.txt`

**Step 3: Configure Database**
1. Start MySQL Server
2. Open MySQL Command Line Client
3. Run: `source MovieRental_MYSQL.sql`
4. Edit `db_config.py` with your MySQL credentials:
   ```python
   self.host = 'localhost'
   self.user = 'root'
   self.password = 'your_password'
   self.database = 'movierental'
   ```

**Step 4: Run Application**
1. In Command Prompt, run: `python main.py`
2. Login with Employee ID (1, 2, 3, etc.)
3. Default password: `abc@123`

### 9.2 User Guide

**9.2.1 Login**
1. Enter your Employee ID
2. Enter password
3. Click "Login" or press Enter

**9.2.2 Movie Management**

*Adding a Movie:*
1. Click "Movie Management" from main menu
2. Fill in movie details:
   - Title (required)
   - Release Year (required)
   - Select Genre from dropdown
   - Enter Rental Price
   - Select Producer from dropdown
3. Click "Add Movie"
4. Movie ID is auto-generated

*Searching Movies:*
1. Enter search criteria (title, genre, year, or price range)
2. Click "Search"
3. Click "Reset" to view all movies

*Updating a Movie:*
1. Click on movie in the list
2. Modify details in the form
3. Click "Update Movie"

*Deleting a Movie:*
1. Select movie from list
2. Click "Delete Movie"
3. Confirm deletion (only if no active rentals)

**9.2.3 Customer Management**

*Adding a Customer:*
1. Click "Customer Management"
2. Fill in:
   - Select Title
   - First Name and Last Name
   - 10-digit Phone number
   - Valid Email address
3. Click "Add Customer"

*Managing Customers:*
- Same process as movies (select, update, or delete)
- Search by name or Customer ID

**9.2.4 Rental Management**

*Viewing Rentals:*
1. Click "Rental Management"
2. Click "View Rentals" tab
3. Use search filters:
   - Customer name
   - Movie title
   - Issue date
   - Status (All/Active/Returned/Overdue)
4. Click "Search" or "Reset"

*Renting a Movie:*
1. Click "Rent a Movie" tab
2. Select customer from dropdown
3. Select available movie
4. Set rental period (days)
5. Click "Issue Movie"
6. Note the due date shown

*Returning a Movie:*
1. Click "Return a Movie" tab
2. Select active rental from dropdown
3. Review rental details and late fee
4. Click "Process Return"
5. Collect late fee if applicable

**9.2.5 Generating Reports**

*Movie Report:*
1. In Movie Management, click "Generate Report"
2. Excel file saved to `reports/` folder
3. View visualization charts

*Customer Report:*
1. In Customer Management, click "Generate Report"
2. Review customer statistics and top customers

*Rental Report:*
1. In Rental Management, click "Generate Report"
2. Multiple sheets created:
   - Currently Rented
   - Overdue Rentals
   - Statistics by Genre
   - Top Producers

### 9.3 Troubleshooting

**Problem: "Error connecting to MySQL"**
- Solution: Verify MySQL server is running
- Check credentials in `db_config.py`
- Ensure database "movierental" exists

**Problem: "Module not found" errors**
- Solution: Run `pip install -r requirements.txt`
- Ensure using correct Python environment

**Problem: Cannot delete movie/customer**
- Solution: Check for active rentals
- Return all movies first, then delete

**Problem: Reports folder not created**
- Solution: Reports folder is auto-created
- Check write permissions in project directory

---

## 10. CONCLUSION AND FUTURE ENHANCEMENTS

### 10.1 Project Achievements

The Movie Rental Management System successfully achieves all project objectives:

✓ **Functional Requirements:**
- Complete CRUD operations for movies, customers, and rentals
- Secure authentication and session management
- Multi-criteria search and filtering
- Automatic late fee calculation
- Comprehensive reporting with visualizations

✓ **Technical Requirements:**
- Well-structured Python code following best practices
- Normalized MySQL database with referential integrity
- User-friendly GUI with intuitive navigation
- Error handling and input validation
- Cross-platform compatibility

✓ **Business Value:**
- Streamlined rental operations
- Accurate fee calculations
- Data-driven decision making through reports
- Improved customer tracking
- Enhanced inventory management

### 10.2 Lessons Learned

**Technical Skills:**
- Advanced Python GUI development with Tkinter
- MySQL database design and normalization
- Data visualization using Matplotlib
- Excel report generation with OpenPyXL
- Exception handling and error management

**Software Engineering:**
- Modular code architecture
- Separation of concerns
- Code reusability
- Documentation best practices
- Testing and validation

### 10.3 Future Enhancements

**Phase 1 - Short Term (1-3 months):**
1. **Advanced User Roles**
   - Admin, Manager, Employee roles
   - Permission-based access control
   - User management interface

2. **Email Notifications**
   - Automated due date reminders
   - Overdue rental notifications
   - Receipt generation

3. **Enhanced Reporting**
   - PDF report generation
   - Monthly revenue reports
   - Customer behavior analytics

**Phase 2 - Medium Term (3-6 months):**
4. **Payment Integration**
   - Payment processing
   - Receipt printing
   - Transaction history

5. **Barcode System**
   - Barcode generation for movies
   - Barcode scanner integration
   - Quick checkout process

6. **Inventory Management**
   - Multiple copies per movie
   - Stock alerts
   - Acquisition tracking

**Phase 3 - Long Term (6-12 months):**
7. **Web Application**
   - Browser-based interface
   - Online reservation system
   - Customer self-service portal

8. **Mobile Application**
   - iOS/Android apps
   - Push notifications
   - Mobile checkout

9. **Advanced Analytics**
   - Machine learning for recommendations
   - Predictive analytics
   - Customer segmentation
   - Trend analysis

10. **Additional Features**
    - Loyalty rewards program
    - Membership tiers
    - Discount management
    - SMS notifications
    - Multi-language support

### 10.4 Recommendations

**For Deployment:**
1. Implement regular database backups
2. Setup SSL/TLS for database connections
3. Implement logging and audit trails
4. Regular security updates
5. User training sessions

**For Maintenance:**
1. Schedule database optimization (weekly)
2. Monitor system performance
3. Review and update reports quarterly
4. Collect user feedback
5. Plan incremental updates

---

## 11. APPENDICES

### Appendix A: Database Schema Script

See `MovieRental_MYSQL.sql` for complete database creation script including:
- Table definitions
- Foreign key constraints
- Sample data insertion
- Index creation

### Appendix B: Configuration Files

**db_config.py Settings:**
```python
host = 'localhost'
database = 'movierental'
user = 'root'
password = 'your_password'
```

### Appendix C: Sample Data

**Default Login Credentials:**
- Employee ID: 1, 2, 3, etc.
- Password: abc@123 (SHA-256 hashed in database)

**Sample Movies:**
- Various genres: Action, Comedy, Drama
- Price range: $2.99 - $9.99
- Multiple producers

**Sample Customers:**
- Pre-populated test customers
- Valid contact information

### Appendix D: File Structure

```
tutorialB/
├── main.py                 # Main application
├── db_config.py           # Database config
├── movie_management.py    # Movie module
├── customer_management.py # Customer module
├── rental_management.py   # Rental module
├── reports.py             # Reporting module
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── MovieRental_MYSQL.sql  # Database script
├── PROJECT_REPORT.md      # This document
├── reports/               # Generated reports
│   ├── Movie_Report_*.xlsx
│   ├── Customer_Report_*.xlsx
│   └── Rental_Report_*.xlsx
└── __pycache__/           # Python cache
```

### Appendix E: References

1. **Python Documentation**
   - https://docs.python.org/3/
   - Tkinter: https://docs.python.org/3/library/tkinter.html

2. **MySQL Documentation**
   - https://dev.mysql.com/doc/
   - SQL Tutorial: https://www.w3schools.com/sql/

3. **Libraries**
   - Pandas: https://pandas.pydata.org/docs/
   - Matplotlib: https://matplotlib.org/
   - OpenPyXL: https://openpyxl.readthedocs.io/

4. **Database Design**
   - Normalization: Database Management Systems by Ramakrishnan
   - ER Modeling: Database System Concepts by Silberschatz

### Appendix F: Glossary

| Term | Definition |
|------|------------|
| CRUD | Create, Read, Update, Delete operations |
| GUI | Graphical User Interface |
| ERD | Entity-Relationship Diagram |
| FK | Foreign Key |
| PK | Primary Key |
| SHA-256 | Secure Hash Algorithm 256-bit |
| SQL | Structured Query Language |
| 3NF | Third Normal Form |
| OOP | Object-Oriented Programming |

---

## PROJECT TEAM

*(Add your team member information here)*

| Name | Student ID | Role | Responsibilities |
|------|-----------|------|------------------|
| [Name] | [ID] | Project Leader | Overall coordination, database design |
| [Name] | [ID] | Developer | GUI development, movie management |
| [Name] | [ID] | Developer | Customer management, testing |
| [Name] | [ID] | Developer | Rental management, reporting |

---

## DECLARATION

We declare that this project is our original work and has been completed in accordance with the academic integrity policies of Victorian Institute of Technology. All external sources and references have been properly cited.

**Signatures:**

_______________________  
Project Leader

_______________________  
Team Member

_______________________  
Team Member

_______________________  
Team Member

**Date:** October 29, 2025

---

## ACKNOWLEDGMENTS

We would like to express our gratitude to:

- **Victorian Institute of Technology** for providing the learning opportunity
- **Course Instructor** for guidance and support throughout the project
- **MySQL Community** for excellent database documentation
- **Python Community** for comprehensive libraries and frameworks
- **Stack Overflow Community** for technical problem-solving assistance

---

**END OF REPORT**

---

**Document Information:**
- **Version:** 1.0
- **Date:** October 29, 2025
- **Total Pages:** [Auto-generated when converted to Word]
- **File Name:** PROJECT_REPORT.md
- **Status:** Final Submission

---

**For More Information:**
- Project Repository: [Add if applicable]
- Documentation: README.md
- Database Script: MovieRental_MYSQL.sql
- Contact: [Your email or contact information]

