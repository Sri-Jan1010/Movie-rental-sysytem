# Movie Rental Management System

## Victorian Institute of Technology
### Developing Data Access Solution - Semester 2, 2025

---

## 📋 Project Overview

A comprehensive Movie Rental Management System built with Python and MySQL, featuring a user-friendly graphical interface for managing movies, customers, and rental transactions. The system implements secure authentication, CRUD operations, advanced search functionality, reporting with Excel export, and data visualization.

---

## ✨ Features

### 1. User Authentication
- Secure employee login system
- Password-based authentication
- User session management

### 2. Movie Management
- ➕ Add new movies with complete details (ID, Title, Genre, Release Year, Rental Price, Producer)
- ✏️ Update existing movie information
- 🗑️ Delete movies (with rental checks)
- 🔍 Advanced search by Title, Genre, Release Year, and Price Range
- 📊 Generate Excel reports with statistics
- 📈 Visual analytics and charts

### 3. Customer Management
- ➕ Add new customers with contact information
- ✏️ Update customer details
- 🗑️ Delete customers (with rental checks)
- 🔍 Search by Name or Customer ID
- 📊 Customer activity reports

### 4. Rental Management
- 🎬 Issue movies to customers
- 📅 Record rental and due dates
- ↩️ Process movie returns with automatic late fee calculation ($2/day)
- 📋 View all rental transactions
- 🔍 Search by customer name, movie title, issue date, and status
- ⚠️ Track overdue rentals
- 💰 Calculate and display late fees

### 5. Reporting & Analytics
- 📑 Export to Excel with multiple sheets
- 📊 Generate reports for:
  - Movies currently rented out
  - Overdue rentals with customer contact info
  - Rental statistics by genre and producer
  - Top performing movies and customers
- 📈 Data visualization with charts:
  - Rental distribution by genre
  - Top movies analysis
  - Revenue statistics
  - Active vs. completed rentals

### 6. Additional Features
- 🎨 Clean and intuitive GUI design
- 🔄 Toggle buttons for easy navigation
- ✅ Form validation and error handling
- 🔒 SQL injection prevention
- 📱 Responsive interface design

---

## 🛠️ Technology Stack

- **Programming Language:** Python 3.8+
- **Database:** MySQL 5.7+
- **GUI Framework:** Tkinter
- **Data Processing:** Pandas
- **Data Visualization:** Matplotlib
- **Excel Export:** OpenPyXL
- **Database Connector:** mysql-connector-python

---

## 📦 Installation Guide

### Prerequisites

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **MySQL Server**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Install and note down root password

3. **Git** (optional, for cloning)

### Step 1: Clone or Download the Project

```bash
# Clone the repository (if using Git)
git clone <repository-url>
cd tutorialB

# OR download and extract the ZIP file
```

### Step 2: Install Required Python Packages

Open Command Prompt or Terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database

1. **Start MySQL Server**

2. **Import the Database Schema**

   Open MySQL Command Line Client or MySQL Workbench and run:

   ```bash
   mysql -u root -p
   ```

   Then execute:

   ```sql
   source MovieRental_MYSQL.sql
   ```

   Or in MySQL Workbench:
   - File → Open SQL Script
   - Select `MovieRental_MYSQL.sql`
   - Execute

3. **Configure Database Connection**

   Edit `db_config.py` and update connection details:

   ```python
   self.host = 'localhost'
   self.database = 'movierental'
   self.user = 'root'          # Your MySQL username
   self.password = 'your_password'  # Your MySQL password
   ```

### Step 4: Run the Application

```bash
python main.py
```

---

## 🚀 Usage Guide

### Login

1. Launch the application
2. Enter Employee ID (e.g., 1, 2, 3, etc.)
3. Enter Password: `abc@123` (default password)
4. Click "Login"

### Movie Management

1. Click **"🎬 Movie Management"** button
2. **Add Movie:**
   - Fill in all required fields
   - Select Genre and Producer from dropdowns
   - Click "Add Movie"
3. **Update Movie:**
   - Click on a movie in the list
   - Modify details in the form
   - Click "Update Movie"
4. **Delete Movie:**
   - Select a movie from the list
   - Click "Delete Movie"
   - Confirm deletion
5. **Search:**
   - Enter search criteria (Title, Genre, Year, Price Range)
   - Click "🔍 Search"
6. **Generate Report:**
   - Click "📊 Generate Report"
   - Report saved in `reports/` folder
   - View visualizations

### Customer Management

1. Click **"👥 Customer Management"** button
2. **Add Customer:**
   - Fill in customer details
   - Phone must be 10 digits
   - Email must be valid format
   - Click "Add Customer"
3. **Update/Delete:** Similar to Movie Management
4. **Search:** By Name or Customer ID

### Rental Management

1. Click **"📀 Rental Management"** button

2. **View Rentals:**
   - Click "📋 View Rentals"
   - Search by customer, movie, date, or status
   - View active, returned, and overdue rentals

3. **Rent a Movie:**
   - Click "➕ Rent a Movie"
   - Select customer from dropdown
   - Select available movie
   - Set rental period (default: 7 days)
   - Click "Issue Movie"

4. **Return a Movie:**
   - Click "↩️ Return a Movie"
   - Select active rental from dropdown
   - Review rental details and late fees
   - Click "Process Return"
   - Late fees are calculated automatically ($2/day)

---

## 📁 Project Structure

```
tutorialB/
│
├── main.py                      # Main application entry point
├── db_config.py                 # Database configuration
├── movie_management.py          # Movie CRUD operations
├── customer_management.py       # Customer CRUD operations
├── rental_management.py         # Rental transactions
├── reports.py                   # Report generation & visualization
├── MovieRental_MYSQL.sql        # Database schema
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── reports/                     # Generated Excel reports
│   ├── Movie_Report_*.xlsx
│   ├── Customer_Report_*.xlsx
│   └── Rental_Report_*.xlsx
│
└── __pycache__/                 # Python cache files

```

---

## 🔒 Security Features

1. **Password Authentication:** Secure employee login
2. **SQL Injection Prevention:** Parameterized queries
3. **Input Validation:** Client-side validation for all inputs
4. **Data Integrity:** Foreign key constraints and transaction checks
5. **Access Control:** Employee-based authentication

---

## 📊 Database Schema

### Main Tables

1. **employees** - Employee authentication and information
2. **movies** - Movie catalog with pricing and details
3. **customer** - Customer contact information
4. **producers** - Movie producers
5. **issuetran** - Rental transactions
6. **country** - Country reference data
7. **documentaries** - Documentary catalog
8. **membercategories** - Membership levels
9. **producerwebsite** - Producer websites
10. **stockadjustment** - Inventory adjustments

---

## 🎯 Key Functionalities

### Late Fee Calculation
- Automatic calculation based on due date
- $2 per day late charge
- Real-time display in return interface
- Included in rental reports

### Report Types

1. **Movie Reports:**
   - Complete movie inventory
   - Genre statistics
   - Top 10 most rented movies
   - Pricing analysis

2. **Customer Reports:**
   - Customer database
   - Top customers by rentals
   - Customers with pending late fees

3. **Rental Reports:**
   - Currently rented movies
   - Overdue rentals with contact info
   - Statistics by genre and producer
   - Revenue analysis

---

## 🐛 Troubleshooting

### Database Connection Error
```
Error connecting to MySQL
```
**Solution:** Check MySQL server is running and credentials in `db_config.py` are correct

### Module Import Error
```
ModuleNotFoundError: No module named 'mysql'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Permission Denied for Reports Folder
**Solution:** Ensure write permissions for the project directory

### Tkinter Not Found
```
ImportError: No module named 'tkinter'
```
**Solution:** 
- Windows: Reinstall Python with tkinter option checked
- Linux: `sudo apt-get install python3-tk`
- Mac: Tkinter comes with Python

---

## 👥 Team Information

**Project Type:** Group Assignment
**Institution:** Victorian Institute of Technology
**Course:** Developing Data Access Solution - Semester 2, 2025

### Team Members:
1. SRIJAN PARAJULI — Student ID: 55537 (Team Leader)
2. BIJAYA TAMANG — Student ID: 57913
3. KRISHNA THARU — Student ID: 57857
4. SHARAD KAFLE — Student ID: 56867

---

## 📝 Testing

### Test Credentials
- **Employee ID:** 1, 2, 3, ... (any valid employee ID from database)
- **Password:** abc@123

### Sample Test Scenarios

1. **Add Movie:** Add "Inception" - Action - 2010 - $5.99
2. **Add Customer:** John Doe - 0412345678 - john@email.com
3. **Rent Movie:** Issue to customer with 7-day rental period
4. **Search:** Find all Action movies
5. **Return:** Process return with/without late fees
6. **Report:** Generate and verify Excel reports

---

## 🔄 Future Enhancements

- [ ] Advanced user roles (Admin, Manager, Employee)
- [ ] Payment processing integration
- [ ] Email notifications for due dates
- [ ] SMS reminders for overdue rentals
- [ ] Barcode scanning for movies
- [ ] Mobile app integration
- [ ] Online reservation system
- [ ] Loyalty rewards program

---

## 📄 License

This project is developed for educational purposes as part of the VIT curriculum.

---

## 📞 Support

For technical support or questions:
- Contact your course instructor
- Refer to VIT student portal
- Check project documentation

---

## 🙏 Acknowledgments

- Victorian Institute of Technology
- Course Instructor
- Python Community
- MySQL Documentation
- Tkinter Documentation

---

## 📚 References

1. Python Official Documentation: https://docs.python.org/3/
2. MySQL Documentation: https://dev.mysql.com/doc/
3. Tkinter Tutorial: https://docs.python.org/3/library/tkinter.html
4. Pandas Documentation: https://pandas.pydata.org/docs/
5. Matplotlib Documentation: https://matplotlib.org/stable/contents.html

---

**Last Updated:** November 3, 2025  
**Version:** 1.0.0  
**Status:** Production Ready

---

## 🎓 Academic Integrity

This project is submitted as part of academic coursework. All code is original work by the team members listed above. External libraries and frameworks are properly attributed.

---

*End of README*
