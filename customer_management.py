"""
Customer Management Module
Handles all customer-related operations: Add, Update, Delete, Search
"""

import tkinter as tk
from tkinter import ttk, messagebox
from reports import ReportGenerator

class CustomerManagement:
    """Customer Management GUI and Logic"""
    
    def __init__(self, parent, db, back_callback=None):
        self.parent = parent
        self.db = db
        self.back_callback = back_callback
        self.selected_customer_id = None
        
        # Setup UI
        self.setup_ui()
        self.load_customers()
    
    def setup_ui(self):
        """Setup Customer Management interface"""
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
            text="Customer Management",
            font=('Arial', 20, 'bold'),
            bg='#ecf0f1'
        )
        title_label.pack(side=tk.LEFT, expand=True)
        
        # Main Container
        main_container = tk.Frame(self.parent, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left Panel - Form
        left_panel = tk.LabelFrame(
            main_container,
            text="Customer Details",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=20,
            pady=20
        )
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), expand=False)
        
        # Form Fields
        fields = [
            ("Customer ID:", "customer_id"),
            ("Title:", "title"),
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Phone:", "phone"),
            ("Email:", "email")
        ]
        
        self.entries = {}
        row = 0
        
        for label_text, field_name in fields:
            tk.Label(
                left_panel,
                text=label_text,
                font=('Arial', 11),
                bg='white'
            ).grid(row=row, column=0, sticky='w', pady=8)
            
            if field_name == "title":
                # Title dropdown
                self.entries[field_name] = ttk.Combobox(
                    left_panel,
                    font=('Arial', 11),
                    width=22,
                    values=["Mr", "Mrs", "Ms", "Dr", "Prof"],
                    state='readonly'
                )
                self.entries[field_name].grid(row=row, column=1, pady=8)
            else:
                self.entries[field_name] = tk.Entry(left_panel, font=('Arial', 11), width=25)
                self.entries[field_name].grid(row=row, column=1, pady=8)
            
            row += 1
        
        # Buttons Frame
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        # Add Button
        tk.Button(
            button_frame,
            text="Add Customer",
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            width=15,
            height=2,
            command=self.add_customer,
            cursor='hand2'
        ).grid(row=0, column=0, padx=5, pady=5)
        
        # Update Button
        tk.Button(
            button_frame,
            text="Update Customer",
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            width=15,
            height=2,
            command=self.update_customer,
            cursor='hand2'
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Delete Button
        tk.Button(
            button_frame,
            text="Delete Customer",
            font=('Arial', 10),
            bg='#f44336',
            fg='white',
            width=15,
            height=2,
            command=self.delete_customer,
            cursor='hand2'
        ).grid(row=1, column=0, padx=5, pady=5)
        
        # Clear Button
        tk.Button(
            button_frame,
            text="Clear Form",
            font=('Arial', 10),
            bg='#9E9E9E',
            fg='white',
            width=15,
            height=2,
            command=self.clear_form,
            cursor='hand2'
        ).grid(row=1, column=1, padx=5, pady=5)
        
        # Right Panel - List and Search
        right_panel = tk.Frame(main_container, bg='#ecf0f1')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Search Frame
        search_frame = tk.LabelFrame(
            right_panel,
            text="Search Customers",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search fields
        search_row = tk.Frame(search_frame, bg='white')
        search_row.pack(fill=tk.X, pady=5)
        
        tk.Label(search_row, text="Name:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_name = tk.Entry(search_row, font=('Arial', 10), width=20)
        self.search_name.pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_row, text="Customer ID:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_id = tk.Entry(search_row, font=('Arial', 10), width=15)
        self.search_id.pack(side=tk.LEFT, padx=5)
        
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
            command=self.search_customers,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_btn_frame,
            text="Reset",
            font=('Arial', 10),
            bg='#9E9E9E',
            fg='white',
            width=12,
            command=self.reset_search,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_btn_frame,
            text="Generate Report",
            font=('Arial', 10),
            bg='#FF9800',
            fg='white',
            width=12,
            command=self.generate_report,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        # Customers List Frame
        list_frame = tk.LabelFrame(
            right_panel,
            text="Customers List",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for customers
        tree_scroll_y = tk.Scrollbar(list_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.customers_tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Title", "FirstName", "LastName", "Phone", "Email"),
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            height=15
        )
        
        tree_scroll_y.config(command=self.customers_tree.yview)
        tree_scroll_x.config(command=self.customers_tree.xview)
        
        # Define columns
        self.customers_tree.heading("ID", text="ID")
        self.customers_tree.heading("Title", text="Title")
        self.customers_tree.heading("FirstName", text="First Name")
        self.customers_tree.heading("LastName", text="Last Name")
        self.customers_tree.heading("Phone", text="Phone")
        self.customers_tree.heading("Email", text="Email")
        
        self.customers_tree.column("ID", width=60, anchor='center')
        self.customers_tree.column("Title", width=60, anchor='center')
        self.customers_tree.column("FirstName", width=150)
        self.customers_tree.column("LastName", width=150)
        self.customers_tree.column("Phone", width=120, anchor='center')
        self.customers_tree.column("Email", width=200)
        
        self.customers_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection
        self.customers_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
    
    def load_customers(self):
        """Load all customers into treeview"""
        # Clear existing
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        # Fetch customers
        query = """
            SELECT CustomerID, Title, FirstName, LastName, Phone, Email
            FROM customer
            ORDER BY CustomerID
        """
        customers = self.db.fetch_data(query)
        
        for customer in customers:
            self.customers_tree.insert('', tk.END, values=(
                customer['CustomerID'],
                customer['Title'],
                customer['FirstName'],
                customer['LastName'],
                customer['Phone'],
                customer['Email']
            ))
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')
            else:
                entry.delete(0, tk.END)
        self.selected_customer_id = None
        self.entries['customer_id'].config(state='normal')
    
    def on_customer_select(self, event):
        """Handle customer selection from treeview"""
        selection = self.customers_tree.selection()
        if selection:
            item = self.customers_tree.item(selection[0])
            values = item['values']
            
            # Fill form
            self.clear_form()
            self.entries['customer_id'].insert(0, values[0])
            self.entries['customer_id'].config(state='disabled')
            self.entries['title'].set(values[1])
            self.entries['first_name'].insert(0, values[2])
            self.entries['last_name'].insert(0, values[3])
            self.entries['phone'].insert(0, values[4])
            self.entries['email'].insert(0, values[5])
            
            self.selected_customer_id = values[0]
    
    def validate_phone(self, phone):
        """Validate phone number (10 digits)"""
        return phone.isdigit() and len(phone) == 10
    
    def validate_email(self, email):
        """Basic email validation"""
        return '@' in email and '.' in email
    
    def add_customer(self):
        """Add new customer"""
        # Validate inputs
        if not self.entries['first_name'].get().strip():
            messagebox.showerror("Error", "Please enter first name")
            return
        
        if not self.entries['last_name'].get().strip():
            messagebox.showerror("Error", "Please enter last name")
            return
        
        if not self.entries['title'].get():
            messagebox.showerror("Error", "Please select a title")
            return
        
        phone = self.entries['phone'].get().strip()
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Phone must be 10 digits")
            return
        
        email = self.entries['email'].get().strip()
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Get next customer ID
        query = "SELECT COALESCE(MAX(CustomerID), 0) + 1 as NextID FROM customer"
        result = self.db.fetch_one(query)
        next_id = result['NextID']
        
        # Insert customer
        query = """
            INSERT INTO customer (CustomerID, Title, FirstName, LastName, Phone, Email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            next_id,
            self.entries['title'].get(),
            self.entries['first_name'].get().strip(),
            self.entries['last_name'].get().strip(),
            phone,
            email
        )
        
        if self.db.execute_query(query, params):
            messagebox.showinfo("Success", "Customer added successfully!")
            self.clear_form()
            self.load_customers()
        else:
            messagebox.showerror("Error", "Failed to add customer")
    
    def update_customer(self):
        """Update existing customer"""
        if not self.selected_customer_id:
            messagebox.showerror("Error", "Please select a customer to update")
            return
        
        # Validate inputs
        if not self.entries['first_name'].get().strip():
            messagebox.showerror("Error", "Please enter first name")
            return
        
        if not self.entries['last_name'].get().strip():
            messagebox.showerror("Error", "Please enter last name")
            return
        
        phone = self.entries['phone'].get().strip()
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Phone must be 10 digits")
            return
        
        email = self.entries['email'].get().strip()
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Update customer
        query = """
            UPDATE customer 
            SET Title = %s, FirstName = %s, LastName = %s, Phone = %s, Email = %s
            WHERE CustomerID = %s
        """
        params = (
            self.entries['title'].get(),
            self.entries['first_name'].get().strip(),
            self.entries['last_name'].get().strip(),
            phone,
            email,
            self.selected_customer_id
        )
        
        if self.db.execute_query(query, params):
            messagebox.showinfo("Success", "Customer updated successfully!")
            self.clear_form()
            self.load_customers()
        else:
            messagebox.showerror("Error", "Failed to update customer")
    
    def delete_customer(self):
        """Delete customer with rental check"""
        if not self.selected_customer_id:
            messagebox.showerror("Error", "Please select a customer to delete")
            return
        
        # Check for existing rentals
        query = "SELECT COUNT(*) as count FROM issuetran WHERE CustomerID = %s AND ReturnDate IS NULL"
        result = self.db.fetch_one(query, (self.selected_customer_id,))
        
        if result['count'] > 0:
            messagebox.showerror(
                "Error",
                "Cannot delete customer. They have active rentals."
            )
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            query = "DELETE FROM customer WHERE CustomerID = %s"
            if self.db.execute_query(query, (self.selected_customer_id,)):
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.clear_form()
                self.load_customers()
            else:
                messagebox.showerror("Error", "Failed to delete customer")
    
    def search_customers(self):
        """Search customers based on filters"""
        # Clear existing
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        # Build query
        query = """
            SELECT CustomerID, Title, FirstName, LastName, Phone, Email
            FROM customer
            WHERE 1=1
        """
        params = []
        
        # Name filter (search in both first and last name)
        if self.search_name.get().strip():
            query += " AND (FirstName LIKE %s OR LastName LIKE %s)"
            search_term = f"%{self.search_name.get().strip()}%"
            params.extend([search_term, search_term])
        
        # ID filter
        if self.search_id.get().strip():
            query += " AND CustomerID = %s"
            params.append(int(self.search_id.get()))
        
        query += " ORDER BY CustomerID"
        
        customers = self.db.fetch_data(query, params if params else None)
        
        for customer in customers:
            self.customers_tree.insert('', tk.END, values=(
                customer['CustomerID'],
                customer['Title'],
                customer['FirstName'],
                customer['LastName'],
                customer['Phone'],
                customer['Email']
            ))
        
        messagebox.showinfo("Search", f"Found {len(customers)} customers")
    
    def reset_search(self):
        """Reset search filters and reload all customers"""
        self.search_name.delete(0, tk.END)
        self.search_id.delete(0, tk.END)
        self.load_customers()
    
    def generate_report(self):
        """Generate customer report"""
        ReportGenerator.generate_customer_report(self.db)
