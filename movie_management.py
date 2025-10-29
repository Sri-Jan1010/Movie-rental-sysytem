"""
Movie Management Module
Handles all movie-related operations: Add, Update, Delete, Search
"""

import tkinter as tk
from tkinter import ttk, messagebox
from reports import ReportGenerator

class MovieManagement:
    """Movie Management GUI and Logic"""
    
    def __init__(self, parent, db, back_callback=None):
        self.parent = parent
        self.db = db
        self.back_callback = back_callback
        self.selected_movie_id = None
        
        # Setup UI
        self.setup_ui()
        self.load_producers()
        self.load_movies()
    
    def setup_ui(self):
        """Setup Movie Management interface"""
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
            text="Movie Management",
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
            text="Movie Details",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=20,
            pady=20
        )
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), expand=False)
        
        # Form Fields
        fields = [
            ("Movie ID:", "movie_id"),
            ("Title:", "title"),
            ("Release Year:", "year"),
            ("Genre:", "genre"),
            ("Rental Price ($):", "price"),
            ("Producer:", "producer")
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
            
            if field_name == "genre":
                # Genre dropdown
                self.entries[field_name] = ttk.Combobox(
                    left_panel,
                    font=('Arial', 11),
                    width=22,
                    values=["Action", "Comedy", "Drama"],
                    state='readonly'
                )
                self.entries[field_name].grid(row=row, column=1, pady=8)
            elif field_name == "producer":
                # Producer dropdown
                self.entries[field_name] = ttk.Combobox(
                    left_panel,
                    font=('Arial', 11),
                    width=22,
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
            text="Add Movie",
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            width=15,
            height=2,
            command=self.add_movie,
            cursor='hand2'
        ).grid(row=0, column=0, padx=5, pady=5)
        
        # Update Button
        tk.Button(
            button_frame,
            text="Update Movie",
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            width=15,
            height=2,
            command=self.update_movie,
            cursor='hand2'
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Delete Button
        tk.Button(
            button_frame,
            text="Delete Movie",
            font=('Arial', 10),
            bg='#f44336',
            fg='white',
            width=15,
            height=2,
            command=self.delete_movie,
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
            text="Search Movies",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search fields
        search_row1 = tk.Frame(search_frame, bg='white')
        search_row1.pack(fill=tk.X, pady=5)
        
        tk.Label(search_row1, text="Title:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_title = tk.Entry(search_row1, font=('Arial', 10), width=15)
        self.search_title.pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_row1, text="Genre:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_genre = ttk.Combobox(
            search_row1,
            font=('Arial', 10),
            width=12,
            values=["All", "Action", "Comedy", "Drama"],
            state='readonly'
        )
        self.search_genre.set("All")
        self.search_genre.pack(side=tk.LEFT, padx=5)
        
        search_row2 = tk.Frame(search_frame, bg='white')
        search_row2.pack(fill=tk.X, pady=5)
        
        tk.Label(search_row2, text="Year:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_year = tk.Entry(search_row2, font=('Arial', 10), width=15)
        self.search_year.pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_row2, text="Price Min:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_price_min = tk.Entry(search_row2, font=('Arial', 10), width=10)
        self.search_price_min.pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_row2, text="Max:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        self.search_price_max = tk.Entry(search_row2, font=('Arial', 10), width=10)
        self.search_price_max.pack(side=tk.LEFT, padx=5)
        
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
            command=self.search_movies,
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
        
        # Movies List Frame
        list_frame = tk.LabelFrame(
            right_panel,
            text="Movies List",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for movies
        tree_scroll_y = tk.Scrollbar(list_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.movies_tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Title", "Year", "Genre", "Price", "Producer"),
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            height=15
        )
        
        tree_scroll_y.config(command=self.movies_tree.yview)
        tree_scroll_x.config(command=self.movies_tree.xview)
        
        # Define columns
        self.movies_tree.heading("ID", text="ID")
        self.movies_tree.heading("Title", text="Title")
        self.movies_tree.heading("Year", text="Year")
        self.movies_tree.heading("Genre", text="Genre")
        self.movies_tree.heading("Price", text="Price ($)")
        self.movies_tree.heading("Producer", text="Producer")
        
        self.movies_tree.column("ID", width=50, anchor='center')
        self.movies_tree.column("Title", width=200)
        self.movies_tree.column("Year", width=80, anchor='center')
        self.movies_tree.column("Genre", width=100, anchor='center')
        self.movies_tree.column("Price", width=80, anchor='center')
        self.movies_tree.column("Producer", width=200)
        
        self.movies_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection
        self.movies_tree.bind('<<TreeviewSelect>>', self.on_movie_select)
    
    def load_producers(self):
        """Load producers into dropdown"""
        query = "SELECT ProducerID, Name FROM producers ORDER BY Name"
        producers = self.db.fetch_data(query)
        
        producer_list = [f"{p['ProducerID']} - {p['Name']}" for p in producers]
        self.entries['producer']['values'] = producer_list
    
    def load_movies(self):
        """Load all movies into treeview"""
        # Clear existing
        for item in self.movies_tree.get_children():
            self.movies_tree.delete(item)
        
        # Fetch movies with producer names
        query = """
            SELECT m.MovieID, m.Title, m.ReleaseYear, m.Genre, m.RentalPrice, p.Name as ProducerName
            FROM movies m
            LEFT JOIN producers p ON m.ProducerID = p.ProducerID
            ORDER BY m.MovieID
        """
        movies = self.db.fetch_data(query)
        
        for movie in movies:
            self.movies_tree.insert('', tk.END, values=(
                movie['MovieID'],
                movie['Title'],
                movie['ReleaseYear'],
                movie['Genre'],
                f"${movie['RentalPrice']:.2f}",
                movie['ProducerName']
            ))
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')
            else:
                entry.delete(0, tk.END)
        self.selected_movie_id = None
    
    def on_movie_select(self, event):
        """Handle movie selection from treeview"""
        selection = self.movies_tree.selection()
        if selection:
            item = self.movies_tree.item(selection[0])
            values = item['values']
            
            # Fill form
            self.clear_form()
            self.entries['movie_id'].insert(0, values[0])
            self.entries['movie_id'].config(state='disabled')
            self.entries['title'].insert(0, values[1])
            self.entries['year'].insert(0, values[2])
            self.entries['genre'].set(values[3])
            
            # Parse price
            price = str(values[4]).replace('$', '')
            self.entries['price'].insert(0, price)
            
            # Set producer
            producer_name = values[5]
            for val in self.entries['producer']['values']:
                if producer_name in val:
                    self.entries['producer'].set(val)
                    break
            
            self.selected_movie_id = values[0]
    
    def add_movie(self):
        """Add new movie"""
        # Validate inputs
        if not self.entries['title'].get().strip():
            messagebox.showerror("Error", "Please enter movie title")
            return
        
        try:
            year = int(self.entries['year'].get())
            price = float(self.entries['price'].get())
        except ValueError:
            messagebox.showerror("Error", "Invalid year or price format")
            return
        
        if not self.entries['genre'].get():
            messagebox.showerror("Error", "Please select a genre")
            return
        
        if not self.entries['producer'].get():
            messagebox.showerror("Error", "Please select a producer")
            return
        
        # Extract producer ID
        producer_str = self.entries['producer'].get()
        producer_id = int(producer_str.split(' - ')[0])
        
        # Get next movie ID
        query = "SELECT COALESCE(MAX(MovieID), 0) + 1 as NextID FROM movies"
        result = self.db.fetch_one(query)
        next_id = result['NextID']
        
        # Insert movie
        query = """
            INSERT INTO movies (MovieID, Title, ReleaseYear, Genre, RentalPrice, ProducerID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            next_id,
            self.entries['title'].get().strip(),
            year,
            self.entries['genre'].get(),
            price,
            producer_id
        )
        
        if self.db.execute_query(query, params):
            messagebox.showinfo("Success", "Movie added successfully!")
            self.clear_form()
            self.load_movies()
        else:
            messagebox.showerror("Error", "Failed to add movie")
    
    def update_movie(self):
        """Update existing movie"""
        if not self.selected_movie_id:
            messagebox.showerror("Error", "Please select a movie to update")
            return
        
        # Validate inputs
        if not self.entries['title'].get().strip():
            messagebox.showerror("Error", "Please enter movie title")
            return
        
        try:
            year = int(self.entries['year'].get())
            price = float(self.entries['price'].get())
        except ValueError:
            messagebox.showerror("Error", "Invalid year or price format")
            return
        
        # Extract producer ID
        producer_str = self.entries['producer'].get()
        producer_id = int(producer_str.split(' - ')[0])
        
        # Update movie
        query = """
            UPDATE movies 
            SET Title = %s, ReleaseYear = %s, Genre = %s, RentalPrice = %s, ProducerID = %s
            WHERE MovieID = %s
        """
        params = (
            self.entries['title'].get().strip(),
            year,
            self.entries['genre'].get(),
            price,
            producer_id,
            self.selected_movie_id
        )
        
        if self.db.execute_query(query, params):
            messagebox.showinfo("Success", "Movie updated successfully!")
            self.clear_form()
            self.load_movies()
        else:
            messagebox.showerror("Error", "Failed to update movie")
    
    def delete_movie(self):
        """Delete movie with rental check"""
        if not self.selected_movie_id:
            messagebox.showerror("Error", "Please select a movie to delete")
            return
        
        # Check for existing rentals
        query = "SELECT COUNT(*) as count FROM issuetran WHERE MovieID = %s AND ReturnDate IS NULL"
        result = self.db.fetch_one(query, (self.selected_movie_id,))
        
        if result['count'] > 0:
            messagebox.showerror(
                "Error",
                "Cannot delete movie. It has active rentals."
            )
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this movie?"):
            query = "DELETE FROM movies WHERE MovieID = %s"
            if self.db.execute_query(query, (self.selected_movie_id,)):
                messagebox.showinfo("Success", "Movie deleted successfully!")
                self.clear_form()
                self.load_movies()
            else:
                messagebox.showerror("Error", "Failed to delete movie")
    
    def search_movies(self):
        """Search movies based on filters"""
        # Clear existing
        for item in self.movies_tree.get_children():
            self.movies_tree.delete(item)
        
        # Build query
        query = """
            SELECT m.MovieID, m.Title, m.ReleaseYear, m.Genre, m.RentalPrice, p.Name as ProducerName
            FROM movies m
            LEFT JOIN producers p ON m.ProducerID = p.ProducerID
            WHERE 1=1
        """
        params = []
        
        # Title filter
        if self.search_title.get().strip():
            query += " AND m.Title LIKE %s"
            params.append(f"%{self.search_title.get().strip()}%")
        
        # Genre filter
        if self.search_genre.get() and self.search_genre.get() != "All":
            query += " AND m.Genre = %s"
            params.append(self.search_genre.get())
        
        # Year filter
        if self.search_year.get().strip():
            query += " AND m.ReleaseYear = %s"
            params.append(int(self.search_year.get()))
        
        # Price range
        if self.search_price_min.get().strip():
            query += " AND m.RentalPrice >= %s"
            params.append(float(self.search_price_min.get()))
        
        if self.search_price_max.get().strip():
            query += " AND m.RentalPrice <= %s"
            params.append(float(self.search_price_max.get()))
        
        query += " ORDER BY m.MovieID"
        
        movies = self.db.fetch_data(query, params if params else None)
        
        for movie in movies:
            self.movies_tree.insert('', tk.END, values=(
                movie['MovieID'],
                movie['Title'],
                movie['ReleaseYear'],
                movie['Genre'],
                f"${movie['RentalPrice']:.2f}",
                movie['ProducerName']
            ))
        
        messagebox.showinfo("Search", f"Found {len(movies)} movies")
    
    def reset_search(self):
        """Reset search filters and reload all movies"""
        self.search_title.delete(0, tk.END)
        self.search_genre.set("All")
        self.search_year.delete(0, tk.END)
        self.search_price_min.delete(0, tk.END)
        self.search_price_max.delete(0, tk.END)
        self.load_movies()
    
    def generate_report(self):
        """Generate movie report"""
        ReportGenerator.generate_movie_report(self.db)
