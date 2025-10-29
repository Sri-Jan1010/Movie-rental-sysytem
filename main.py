"""
Movie Rental Management System - Main Application
Victorian Institute of Technology
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db_config import DatabaseConfig
from movie_management import MovieManagement
from customer_management import CustomerManagement
from rental_management import RentalManagement

class LoginWindow:
    """User authentication window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Movie Rental System - Login")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self.center_window()
        
        self.db = DatabaseConfig()
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup login interface"""
        self.root.configure(bg='#3d5a6b')
        
        login_frame = tk.Frame(self.root, bg='#3d5a6b')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = tk.Label(login_frame, text="Login", font=('Arial', 28, 'bold'), 
                              bg='#3d5a6b', fg='white')
        title_label.pack(pady=(0, 30))
        
        # Employee ID
        tk.Label(login_frame, text="Employee ID:", font=('Arial', 14, 'bold'),
                bg='#3d5a6b', fg='white').pack(pady=(10, 5))
        
        self.employee_id_entry = tk.Entry(login_frame, font=('Arial', 12), width=35, bg='#b8c6d0')
        self.employee_id_entry.pack(pady=(0, 15))
        
        # Password
        tk.Label(login_frame, text="Password:", font=('Arial', 14, 'bold'),
                bg='#3d5a6b', fg='white').pack(pady=(10, 5))
        
        self.password_entry = tk.Entry(login_frame, font=('Arial', 12), width=35, show='*', bg='#b8c6d0')
        self.password_entry.pack(pady=(0, 25))
        
        # Login Button
        login_btn = tk.Button(
            login_frame,
            text="Login",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            width=25,
            height=1,
            command=self.login,
            cursor='hand2',
            relief=tk.FLAT
        )
        login_btn.pack(pady=10)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())
        
    def login(self):
        """Handle login authentication"""
        employee_id = self.employee_id_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not employee_id or not password:
            messagebox.showerror("Error", "Please enter both Employee ID and Password")
            return
        
        # Authenticate
        is_authenticated, user_data = self.db.authenticate_user(employee_id, password)
        
        if is_authenticated:
            self.root.destroy()
            # Open management options window
            ManagementOptions(user_data)
        else:
            messagebox.showerror("Error", "Invalid Employee ID or Password")
            self.password_entry.delete(0, tk.END)
    
    def run(self):
        """Start the login window"""
        self.root.mainloop()


class ManagementOptions:
    """Management options selection window"""
    
    def __init__(self, user_data):
        self.user_data = user_data
        self.root = tk.Tk()
        self.root.title("Management Options")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Database connection
        self.db = DatabaseConfig()
        
        # Setup UI
        self.setup_ui()
        
        self.root.mainloop()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup management options interface"""
        # Background
        self.root.configure(bg='#3d5a6b')
        
        # Container
        container = tk.Frame(self.root, bg='#3d5a6b')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = tk.Label(
            container,
            text="Select Management Option",
            font=('Arial', 20, 'bold'),
            bg='#3d5a6b',
            fg='white'
        )
        title_label.pack(pady=(0, 30))
        
        # Button style
        btn_width = 25
        btn_height = 2
        btn_pady = 8
        
        # Movie Management Button
        movie_btn = tk.Button(
            container,
            text="Movie Management",
            font=('Arial', 12),
            bg='white',
            fg='black',
            width=btn_width,
            height=btn_height,
            command=self.open_movie_management,
            cursor='hand2',
            relief=tk.RAISED,
            bd=2
        )
        movie_btn.pack(pady=btn_pady)
        
        # Customer Management Button
        customer_btn = tk.Button(
            container,
            text="Customer Management",
            font=('Arial', 12),
            bg='white',
            fg='black',
            width=btn_width,
            height=btn_height,
            command=self.open_customer_management,
            cursor='hand2',
            relief=tk.RAISED,
            bd=2
        )
        customer_btn.pack(pady=btn_pady)
        
        # Rental Management Button
        rental_btn = tk.Button(
            container,
            text="Rental Management",
            font=('Arial', 12),
            bg='white',
            fg='black',
            width=btn_width,
            height=btn_height,
            command=self.open_rental_management,
            cursor='hand2',
            relief=tk.RAISED,
            bd=2
        )
        rental_btn.pack(pady=btn_pady)
        
        # Logout Button
        logout_btn = tk.Button(
            container,
            text="Logout",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            width=btn_width,
            height=2,
            command=self.logout,
            cursor='hand2',
            relief=tk.RAISED,
            bd=2
        )
        logout_btn.pack(pady=30)
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            LoginWindow().run()
    
    def open_movie_management(self):
        """Open Movie Management window"""
        self.root.destroy()
        MainApplication(self.user_data, "movie")
    
    def open_customer_management(self):
        """Open Customer Management window"""
        self.root.destroy()
        MainApplication(self.user_data, "customer")
    
    def open_rental_management(self):
        """Open Rental Management window"""
        self.root.destroy()
        MainApplication(self.user_data, "rental")


class MainApplication:
    """Main application window with navigation"""
    
    def __init__(self, user_data, module="movie"):
        self.user_data = user_data
        self.current_module = module
        self.root = tk.Tk()
        
        # Set title based on module
        titles = {
            "movie": "Movies - Movie Management",
            "customer": "Movies - Customer Management", 
            "rental": "Movies - Rental Management"
        }
        self.root.title(titles.get(module, "Movie Management"))
        self.root.geometry("1200x700")
        self.root.state('zoomed')  # Maximize window
        
        # Database connection
        self.db = DatabaseConfig()
        
        # Setup UI
        self.setup_ui()
        
        # Show initial module
        if module == "movie":
            self.show_movie_management()
        elif module == "customer":
            self.show_customer_management()
        elif module == "rental":
            self.show_rental_management()
        
        self.root.mainloop()
    
    def setup_ui(self):
        """Setup main application interface"""
        # Content Frame - this will be filled by management modules
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
    def back_to_menu(self):
        """Go back to management options menu"""
        self.root.destroy()
        ManagementOptions(self.user_data)
        
    def show_movie_management(self):
        """Show Movie Management interface"""
        MovieManagement(self.content_frame, self.db, self.back_to_menu)
    
    def show_customer_management(self):
        """Show Customer Management interface"""
        CustomerManagement(self.content_frame, self.db, self.back_to_menu)
    
    def show_rental_management(self):
        """Show Rental Management interface"""
        RentalManagement(self.content_frame, self.db, self.back_to_menu)
    
    def switch_module(self, module):
        """Switch to different management module"""
        self.root.destroy()
        MainApplication(self.user_data, module)


if __name__ == "__main__":
    # Start with login window
    LoginWindow().run()
