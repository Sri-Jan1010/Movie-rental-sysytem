"""
Rental Management Module
Handles rental transactions: Issue, Return, View, Search
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from reports import ReportGenerator

class RentalManagement:
    """Rental Management GUI and Logic"""
    
    def __init__(self, parent, db, back_callback=None):
        self.parent = parent
        self.db = db
        self.back_callback = back_callback
        self.current_view = "view"
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup Rental Management interface"""
        # Header Frame
        header_frame = tk.Frame(self.parent, bg='#ecf0f1')
        header_frame.pack(fill=tk.X, pady=10)
        
        # Back Button (if callback provided)
        if self.back_callback:
            tk.Button(
                header_frame,
                text="← Back to Menu",
                font=('Arial', 10),
                bg='#95a5a6',
                fg='white',
                command=self.back_callback,
                cursor='hand2',
                padx=15,
                pady=5
            ).pack(side=tk.LEFT, padx=20)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Rental Management",
            font=('Arial', 20, 'bold'),
            bg='#ecf0f1'
        )
        title_label.pack(side=tk.LEFT, expand=True)
        
        # Toggle Buttons Frame
        toggle_frame = tk.Frame(self.parent, bg='#ecf0f1')
        toggle_frame.pack(pady=10)
        
        self.view_btn = tk.Button(
            toggle_frame,
            text="View Rentals",
            font=('Arial', 11),
            bg='#4CAF50',
            fg='white',
            width=18,
            height=2,
            command=self.show_view_rentals,
            cursor='hand2',
            relief=tk.SUNKEN
        )
        self.view_btn.pack(side=tk.LEFT, padx=5)
        
        self.rent_btn = tk.Button(
            toggle_frame,
            text="Rent a Movie",
            font=('Arial', 11),
            bg='#2196F3',
            fg='white',
            width=18,
            height=2,
            command=self.show_rent_movie,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.rent_btn.pack(side=tk.LEFT, padx=5)
        
        self.return_btn = tk.Button(
            toggle_frame,
            text="Return a Movie",
            font=('Arial', 11),
            bg='#FF9800',
            fg='white',
            width=18,
            height=2,
            command=self.show_return_movie,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.return_btn.pack(side=tk.LEFT, padx=5)
        
        # Content Frame
        self.content_frame = tk.Frame(self.parent, bg='#ecf0f1')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Show default view
        self.show_view_rentals()
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def highlight_button(self, active_btn):
        """Highlight active button"""
        for btn in [self.view_btn, self.rent_btn, self.return_btn]:
            btn.config(relief=tk.RAISED)
        active_btn.config(relief=tk.SUNKEN)
    
    def show_view_rentals(self):
        """Show all rentals with search functionality"""
        self.clear_content()
        self.highlight_button(self.view_btn)
        self.current_view = "view"
        
        # Search Frame
        search_frame = tk.LabelFrame(
            self.content_frame,
            text="Search Rentals",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=15,
            pady=15
        )
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search fields
        search_row1 = tk.Frame(search_frame, bg='white')
        search_row1.pack(fill=tk.X, pady=5)
        
        tk.Label(search_row1, text="Customer Name:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_customer = tk.Entry(search_row1, font=('Arial', 10), width=20)
        self.search_customer.pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_row1, text="Movie Title:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_movie = tk.Entry(search_row1, font=('Arial', 10), width=20)
        self.search_movie.pack(side=tk.LEFT, padx=5)
        
        search_row2 = tk.Frame(search_frame, bg='white')
        search_row2.pack(fill=tk.X, pady=5)
        
        tk.Label(search_row2, text="Issue Date:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_issue_date = tk.Entry(search_row2, font=('Arial', 10), width=15)
        self.search_issue_date.pack(side=tk.LEFT, padx=5)
        tk.Label(search_row2, text="(YYYY-MM-DD)", font=('Arial', 8, 'italic'), bg='white', fg='gray').pack(side=tk.LEFT)
        
        tk.Label(search_row2, text="Status:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_status = ttk.Combobox(
            search_row2,
            font=('Arial', 10),
            width=15,
            values=["All", "Active", "Returned", "Overdue"],
            state='readonly'
        )
        self.search_status.set("All")
        self.search_status.pack(side=tk.LEFT, padx=5)
        
        # Search buttons
        search_btn_frame = tk.Frame(search_frame, bg='white')
        search_btn_frame.pack(pady=10)
        
        tk.Button(
            search_btn_frame,
            text="Search",
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            width=12,
            command=self.search_rentals,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_btn_frame,
            text="Reset",
            font=('Arial', 10),
            bg='#9E9E9E',
            fg='white',
            width=12,
            command=self.reset_rental_search,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_btn_frame,
            text="Generate Report",
            font=('Arial', 10),
            bg='#FF9800',
            fg='white',
            width=12,
            command=self.generate_rental_report,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        # Rentals List Frame
        list_frame = tk.LabelFrame(
            self.content_frame,
            text="Rentals List",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        tree_scroll_y = tk.Scrollbar(list_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.rentals_tree = ttk.Treeview(
            list_frame,
            columns=("IssueID", "Customer", "Movie", "IssueDate", "DueDate", "ReturnDate", "Status", "LateFee"),
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            height=15
        )
        
        tree_scroll_y.config(command=self.rentals_tree.yview)
        tree_scroll_x.config(command=self.rentals_tree.xview)
        
        # Define columns
        self.rentals_tree.heading("IssueID", text="Rental ID")
        self.rentals_tree.heading("Customer", text="Customer")
        self.rentals_tree.heading("Movie", text="Movie")
        self.rentals_tree.heading("IssueDate", text="Issue Date")
        self.rentals_tree.heading("DueDate", text="Due Date")
        self.rentals_tree.heading("ReturnDate", text="Return Date")
        self.rentals_tree.heading("Status", text="Status")
        self.rentals_tree.heading("LateFee", text="Late Fee")
        
        self.rentals_tree.column("IssueID", width=80, anchor='center')
        self.rentals_tree.column("Customer", width=150)
        self.rentals_tree.column("Movie", width=200)
        self.rentals_tree.column("IssueDate", width=100, anchor='center')
        self.rentals_tree.column("DueDate", width=100, anchor='center')
        self.rentals_tree.column("ReturnDate", width=100, anchor='center')
        self.rentals_tree.column("Status", width=80, anchor='center')
        self.rentals_tree.column("LateFee", width=80, anchor='center')
        
        self.rentals_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load rentals
        self.load_rentals()
    
    def show_rent_movie(self):
        """Show interface to rent a movie"""
        self.clear_content()
        self.highlight_button(self.rent_btn)
        self.current_view = "rent"
        
        # Form Frame
        form_frame = tk.LabelFrame(
            self.content_frame,
            text="Rent a Movie",
            font=('Arial', 14, 'bold'),
            bg='white',
            padx=30,
            pady=30
        )
        form_frame.pack(pady=50)
        
        # Customer Selection
        tk.Label(
            form_frame,
            text="Select Customer:",
            font=('Arial', 12),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=15, padx=10)
        
        self.rent_customer = ttk.Combobox(
            form_frame,
            font=('Arial', 11),
            width=40,
            state='readonly'
        )
        self.rent_customer.grid(row=0, column=1, pady=15, padx=10)
        
        # Movie Selection
        tk.Label(
            form_frame,
            text="Select Movie:",
            font=('Arial', 12),
            bg='white'
        ).grid(row=1, column=0, sticky='w', pady=15, padx=10)
        
        self.rent_movie = ttk.Combobox(
            form_frame,
            font=('Arial', 11),
            width=40,
            state='readonly'
        )
        self.rent_movie.grid(row=1, column=1, pady=15, padx=10)
        
        # Rental Period
        tk.Label(
            form_frame,
            text="Rental Period (days):",
            font=('Arial', 12),
            bg='white'
        ).grid(row=2, column=0, sticky='w', pady=15, padx=10)
        
        self.rent_period = tk.Spinbox(
            form_frame,
            from_=1,
            to=30,
            font=('Arial', 11),
            width=39
        )
        self.rent_period.delete(0, tk.END)
        self.rent_period.insert(0, "7")
        self.rent_period.grid(row=2, column=1, pady=15, padx=10)
        
        # Issue Button
        tk.Button(
            form_frame,
            text="Issue Movie",
            font=('Arial', 11),
            bg='#4CAF50',
            fg='white',
            width=20,
            height=2,
            command=self.issue_movie,
            cursor='hand2'
        ).grid(row=3, column=0, columnspan=2, pady=30)
        
        # Load customers and movies
        self.load_customers_for_rental()
        self.load_movies_for_rental()
    
    def show_return_movie(self):
        """Show interface to return a movie"""
        self.clear_content()
        self.highlight_button(self.return_btn)
        self.current_view = "return"
        
        # Return Frame
        return_frame = tk.LabelFrame(
            self.content_frame,
            text="Return a Movie",
            font=('Arial', 14, 'bold'),
            bg='white',
            padx=30,
            pady=30
        )
        return_frame.pack(pady=50)
        
        # Active Rentals Selection
        tk.Label(
            return_frame,
            text="Select Active Rental:",
            font=('Arial', 12),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=15, padx=10)
        
        self.return_rental = ttk.Combobox(
            return_frame,
            font=('Arial', 11),
            width=50,
            state='readonly'
        )
        self.return_rental.grid(row=0, column=1, pady=15, padx=10)
        
        # Info Labels
        self.return_info_frame = tk.Frame(return_frame, bg='white')
        self.return_info_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Return Button
        tk.Button(
            return_frame,
            text="Process Return",
            font=('Arial', 11),
            bg='#FF9800',
            fg='white',
            width=20,
            height=2,
            command=self.process_return,
            cursor='hand2'
        ).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Load active rentals
        self.load_active_rentals()
        self.return_rental.bind('<<ComboboxSelected>>', self.on_rental_select)
    
    def load_customers_for_rental(self):
        """Load customers into dropdown"""
        query = "SELECT CustomerID, FirstName, LastName FROM customer ORDER BY FirstName"
        customers = self.db.fetch_data(query)
        
        customer_list = [f"{c['CustomerID']} - {c['FirstName']} {c['LastName']}" for c in customers]
        self.rent_customer['values'] = customer_list
    
    def load_movies_for_rental(self):
        """Load available movies into dropdown"""
        # Movies not currently rented out
        query = """
            SELECT m.MovieID, m.Title, m.RentalPrice
            FROM movies m
            WHERE m.MovieID NOT IN (
                SELECT MovieID FROM issuetran WHERE ReturnDate IS NULL
            )
            ORDER BY m.Title
        """
        movies = self.db.fetch_data(query)
        
        movie_list = [f"{m['MovieID']} - {m['Title']} (${m['RentalPrice']:.2f})" for m in movies]
        self.rent_movie['values'] = movie_list
    
    def load_active_rentals(self):
        """Load active rentals for return"""
        query = """
            SELECT i.IssueID, c.FirstName, c.LastName, m.Title, i.IssueDate, i.dueDate
            FROM issuetran i
            JOIN customer c ON i.CustomerID = c.CustomerID
            JOIN movies m ON i.MovieID = m.MovieID
            WHERE i.ReturnDate IS NULL
            ORDER BY i.IssueDate
        """
        rentals = self.db.fetch_data(query)
        
        rental_list = [
            f"{r['IssueID']} - {r['FirstName']} {r['LastName']} - {r['Title']} (Due: {r['dueDate']})"
            for r in rentals
        ]
        self.return_rental['values'] = rental_list
    
    def on_rental_select(self, event):
        """Show rental details when selected"""
        # Clear previous info
        for widget in self.return_info_frame.winfo_children():
            widget.destroy()
        
        if self.return_rental.get():
            rental_str = self.return_rental.get()
            rental_id = int(rental_str.split(' - ')[0])
            
            # Get rental details
            query = """
                SELECT i.*, c.FirstName, c.LastName, m.Title, m.RentalPrice
                FROM issuetran i
                JOIN customer c ON i.CustomerID = c.CustomerID
                JOIN movies m ON i.MovieID = m.MovieID
                WHERE i.IssueID = %s
            """
            rental = self.db.fetch_one(query, (rental_id,))
            
            if rental:
                # Calculate late fee
                due_date = rental['dueDate']
                today = datetime.now().date()
                late_days = max(0, (today - due_date).days)
                late_fee = late_days * 2.0  # $2 per day late
                
                # Display info
                info_text = tk.Label(
                    self.return_info_frame,
                    text=f"Customer: {rental['FirstName']} {rental['LastName']}\n"
                         f"Movie: {rental['Title']}\n"
                         f"Issue Date: {rental['IssueDate']}\n"
                         f"Due Date: {rental['dueDate']}\n"
                         f"Days Late: {late_days}\n"
                         f"Late Fee: ${late_fee:.2f}",
                    font=('Arial', 11),
                    bg='white',
                    justify=tk.LEFT
                )
                info_text.pack(pady=10)
                
                if late_days > 0:
                    warning = tk.Label(
                        self.return_info_frame,
                        text=f"⚠️ OVERDUE by {late_days} days!",
                        font=('Arial', 11, 'bold'),
                        bg='white',
                        fg='red'
                    )
                    warning.pack(pady=5)
    
    def issue_movie(self):
        """Issue a movie to customer"""
        if not self.rent_customer.get():
            messagebox.showerror("Error", "Please select a customer")
            return
        
        if not self.rent_movie.get():
            messagebox.showerror("Error", "Please select a movie")
            return
        
        try:
            rental_days = int(self.rent_period.get())
            if rental_days < 1:
                raise ValueError()
        except:
            messagebox.showerror("Error", "Invalid rental period")
            return
        
        # Extract IDs
        customer_id = int(self.rent_customer.get().split(' - ')[0])
        movie_id = int(self.rent_movie.get().split(' - ')[0])
        
        # Get next issue ID
        query = "SELECT COALESCE(MAX(IssueID), 0) + 1 as NextID FROM issuetran"
        result = self.db.fetch_one(query)
        next_id = result['NextID']
        
        # Calculate dates
        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=rental_days)
        
        # Insert rental
        query = """
            INSERT INTO issuetran (IssueID, CustomerID, MovieID, IssueDate, dueDate, ReturnDate)
            VALUES (%s, %s, %s, %s, %s, NULL)
        """
        params = (next_id, customer_id, movie_id, issue_date, due_date)
        
        if self.db.execute_query(query, params):
            messagebox.showinfo(
                "Success",
                f"Movie rented successfully!\nDue Date: {due_date}"
            )
            # Reset form
            self.rent_customer.set('')
            self.rent_movie.set('')
            self.load_movies_for_rental()  # Refresh available movies
        else:
            messagebox.showerror("Error", "Failed to issue movie")
    
    def process_return(self):
        """Process movie return with late fee calculation"""
        if not self.return_rental.get():
            messagebox.showerror("Error", "Please select a rental to return")
            return
        
        rental_str = self.return_rental.get()
        rental_id = int(rental_str.split(' - ')[0])
        
        # Get rental details
        query = """
            SELECT i.*, m.Title, m.RentalPrice
            FROM issuetran i
            JOIN movies m ON i.MovieID = m.MovieID
            WHERE i.IssueID = %s
        """
        rental = self.db.fetch_one(query, (rental_id,))
        
        if rental:
            # Calculate late fee
            due_date = rental['dueDate']
            return_date = datetime.now().date()
            late_days = max(0, (return_date - due_date).days)
            late_fee = late_days * 2.0
            
            # Update rental
            query = "UPDATE issuetran SET ReturnDate = %s WHERE IssueID = %s"
            if self.db.execute_query(query, (return_date, rental_id)):
                message = f"Movie returned successfully!\n\n"
                message += f"Return Date: {return_date}\n"
                if late_days > 0:
                    message += f"Days Late: {late_days}\n"
                    message += f"Late Fee: ${late_fee:.2f}\n"
                    message += f"\n⚠️ Please collect late fee from customer."
                else:
                    message += "Returned on time. No late fees."
                
                messagebox.showinfo("Return Processed", message)
                
                # Reset and reload
                self.return_rental.set('')
                for widget in self.return_info_frame.winfo_children():
                    widget.destroy()
                self.load_active_rentals()
            else:
                messagebox.showerror("Error", "Failed to process return")
    
    def load_rentals(self):
        """Load all rentals into treeview"""
        # Clear existing
        for item in self.rentals_tree.get_children():
            self.rentals_tree.delete(item)
        
        # Fetch rentals
        query = """
            SELECT 
                i.IssueID,
                CONCAT(c.FirstName, ' ', c.LastName) as Customer,
                m.Title as Movie,
                i.IssueDate,
                i.dueDate,
                i.ReturnDate
            FROM issuetran i
            JOIN customer c ON i.CustomerID = c.CustomerID
            JOIN movies m ON i.MovieID = m.MovieID
            ORDER BY i.IssueDate DESC
        """
        rentals = self.db.fetch_data(query)
        
        today = datetime.now().date()
        
        for rental in rentals:
            due_date = rental['dueDate']
            return_date = rental['ReturnDate']
            
            # Determine status and late fee
            if return_date:
                status = "Returned"
                late_days = max(0, (return_date - due_date).days)
                late_fee = f"${late_days * 2.0:.2f}" if late_days > 0 else "$0.00"
            else:
                late_days = max(0, (today - due_date).days)
                if late_days > 0:
                    status = "Overdue"
                    late_fee = f"${late_days * 2.0:.2f}"
                else:
                    status = "Active"
                    late_fee = "$0.00"
            
            return_date_str = str(return_date) if return_date else "Not Returned"
            
            self.rentals_tree.insert('', tk.END, values=(
                rental['IssueID'],
                rental['Customer'],
                rental['Movie'],
                rental['IssueDate'],
                rental['dueDate'],
                return_date_str,
                status,
                late_fee
            ))
    
    def search_rentals(self):
        """Search rentals based on filters"""
        # Clear existing
        for item in self.rentals_tree.get_children():
            self.rentals_tree.delete(item)
        
        # Build query
        query = """
            SELECT 
                i.IssueID,
                CONCAT(c.FirstName, ' ', c.LastName) as Customer,
                m.Title as Movie,
                i.IssueDate,
                i.dueDate,
                i.ReturnDate
            FROM issuetran i
            JOIN customer c ON i.CustomerID = c.CustomerID
            JOIN movies m ON i.MovieID = m.MovieID
            WHERE 1=1
        """
        params = []
        
        # Customer name filter
        if self.search_customer.get().strip():
            query += " AND (c.FirstName LIKE %s OR c.LastName LIKE %s)"
            search_term = f"%{self.search_customer.get().strip()}%"
            params.extend([search_term, search_term])
        
        # Movie title filter
        if self.search_movie.get().strip():
            query += " AND m.Title LIKE %s"
            params.append(f"%{self.search_movie.get().strip()}%")
        
        # Issue date filter
        if self.search_issue_date.get().strip():
            query += " AND i.IssueDate = %s"
            params.append(self.search_issue_date.get().strip())
        
        # Status filter
        status = self.search_status.get()
        if status == "Active":
            query += " AND i.ReturnDate IS NULL AND i.dueDate >= CURDATE()"
        elif status == "Returned":
            query += " AND i.ReturnDate IS NOT NULL"
        elif status == "Overdue":
            query += " AND i.ReturnDate IS NULL AND i.dueDate < CURDATE()"
        
        query += " ORDER BY i.IssueDate DESC"
        
        rentals = self.db.fetch_data(query, params if params else None)
        
        today = datetime.now().date()
        
        for rental in rentals:
            due_date = rental['dueDate']
            return_date = rental['ReturnDate']
            
            if return_date:
                status = "Returned"
                late_days = max(0, (return_date - due_date).days)
                late_fee = f"${late_days * 2.0:.2f}" if late_days > 0 else "$0.00"
            else:
                late_days = max(0, (today - due_date).days)
                if late_days > 0:
                    status = "Overdue"
                    late_fee = f"${late_days * 2.0:.2f}"
                else:
                    status = "Active"
                    late_fee = "$0.00"
            
            return_date_str = str(return_date) if return_date else "Not Returned"
            
            self.rentals_tree.insert('', tk.END, values=(
                rental['IssueID'],
                rental['Customer'],
                rental['Movie'],
                rental['IssueDate'],
                rental['dueDate'],
                return_date_str,
                status,
                late_fee
            ))
        
        messagebox.showinfo("Search", f"Found {len(rentals)} rentals")
    
    def reset_rental_search(self):
        """Reset search and reload all rentals"""
        self.search_customer.delete(0, tk.END)
        self.search_movie.delete(0, tk.END)
        self.search_issue_date.delete(0, tk.END)
        self.search_status.set("All")
        self.load_rentals()
    
    def generate_rental_report(self):
        """Generate rental reports"""
        ReportGenerator.generate_rental_report(self.db)
