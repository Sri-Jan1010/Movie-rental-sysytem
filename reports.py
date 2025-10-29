"""
Reports Module
Generate Excel reports and data visualizations
"""

import os
from datetime import datetime
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class ReportGenerator:
    """Generate various reports and visualizations"""
    
    @staticmethod
    def ensure_reports_directory():
        """Ensure reports directory exists"""
        if not os.path.exists('reports'):
            os.makedirs('reports')
    
    @staticmethod
    def generate_movie_report(db):
        """Generate movie statistics report"""
        ReportGenerator.ensure_reports_directory()
        
        try:
            # Fetch movie data
            query = """
                SELECT 
                    m.MovieID,
                    m.Title,
                    m.ReleaseYear,
                    m.Genre,
                    m.RentalPrice,
                    p.Name as Producer,
                    COUNT(i.IssueID) as TotalRentals,
                    SUM(CASE WHEN i.ReturnDate IS NULL THEN 1 ELSE 0 END) as CurrentlyRented
                FROM movies m
                LEFT JOIN producers p ON m.ProducerID = p.ProducerID
                LEFT JOIN issuetran i ON m.MovieID = i.MovieID
                GROUP BY m.MovieID
                ORDER BY TotalRentals DESC
            """
            movies = db.fetch_data(query)
            
            if not movies:
                messagebox.showwarning("Warning", "No movie data available")
                return
            
            # Create DataFrame
            df = pd.DataFrame(movies)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/Movie_Report_{timestamp}.xlsx"
            
            # Create Excel writer
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Movies sheet
                df.to_excel(writer, sheet_name='Movies', index=False)
                
                # Genre statistics
                genre_stats = df.groupby('Genre').agg({
                    'MovieID': 'count',
                    'TotalRentals': 'sum',
                    'RentalPrice': 'mean'
                }).rename(columns={
                    'MovieID': 'Total Movies',
                    'TotalRentals': 'Total Rentals',
                    'RentalPrice': 'Avg Price'
                })
                genre_stats.to_excel(writer, sheet_name='Genre Statistics')
                
                # Top 10 most rented
                top_movies = df.nlargest(10, 'TotalRentals')[['Title', 'Genre', 'TotalRentals']]
                top_movies.to_excel(writer, sheet_name='Top 10 Movies', index=False)
            
            messagebox.showinfo(
                "Success",
                f"Movie report generated successfully!\n\nSaved to: {filename}"
            )
            
            # Show visualization
            ReportGenerator.show_movie_visualization(df)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")
    
    @staticmethod
    def generate_customer_report(db):
        """Generate customer statistics report"""
        ReportGenerator.ensure_reports_directory()
        
        try:
            # Fetch customer data
            query = """
                SELECT 
                    c.CustomerID,
                    c.Title,
                    CONCAT(c.FirstName, ' ', c.LastName) as FullName,
                    c.Phone,
                    c.Email,
                    COUNT(i.IssueID) as TotalRentals,
                    SUM(CASE WHEN i.ReturnDate IS NULL THEN 1 ELSE 0 END) as ActiveRentals,
                    SUM(CASE 
                        WHEN i.ReturnDate IS NULL AND i.dueDate < CURDATE() 
                        THEN DATEDIFF(CURDATE(), i.dueDate) * 2.0 
                        ELSE 0 
                    END) as PendingLateFees
                FROM customer c
                LEFT JOIN issuetran i ON c.CustomerID = i.CustomerID
                GROUP BY c.CustomerID
                ORDER BY TotalRentals DESC
            """
            customers = db.fetch_data(query)
            
            if not customers:
                messagebox.showwarning("Warning", "No customer data available")
                return
            
            # Create DataFrame
            df = pd.DataFrame(customers)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/Customer_Report_{timestamp}.xlsx"
            
            # Create Excel writer
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Customers sheet
                df.to_excel(writer, sheet_name='Customers', index=False)
                
                # Top customers
                top_customers = df.nlargest(10, 'TotalRentals')[['FullName', 'TotalRentals', 'ActiveRentals']]
                top_customers.to_excel(writer, sheet_name='Top 10 Customers', index=False)
                
                # Customers with late fees
                late_fees = df[df['PendingLateFees'] > 0][['FullName', 'Phone', 'PendingLateFees']]
                late_fees.to_excel(writer, sheet_name='Pending Late Fees', index=False)
            
            messagebox.showinfo(
                "Success",
                f"Customer report generated successfully!\n\nSaved to: {filename}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")
    
    @staticmethod
    def generate_rental_report(db):
        """Generate rental statistics report with overdue tracking"""
        ReportGenerator.ensure_reports_directory()
        
        try:
            # Currently rented movies
            query1 = """
                SELECT 
                    i.IssueID,
                    CONCAT(c.FirstName, ' ', c.LastName) as CustomerName,
                    c.Phone,
                    m.Title as MovieTitle,
                    m.Genre,
                    i.IssueDate,
                    i.dueDate,
                    DATEDIFF(CURDATE(), i.dueDate) as DaysOverdue,
                    CASE 
                        WHEN DATEDIFF(CURDATE(), i.dueDate) > 0 
                        THEN DATEDIFF(CURDATE(), i.dueDate) * 2.0 
                        ELSE 0 
                    END as LateFee
                FROM issuetran i
                JOIN customer c ON i.CustomerID = c.CustomerID
                JOIN movies m ON i.MovieID = m.MovieID
                WHERE i.ReturnDate IS NULL
                ORDER BY i.dueDate
            """
            currently_rented = db.fetch_data(query1)
            
            # Overdue rentals
            query2 = """
                SELECT 
                    i.IssueID,
                    CONCAT(c.FirstName, ' ', c.LastName) as CustomerName,
                    c.Phone,
                    c.Email,
                    m.Title as MovieTitle,
                    i.IssueDate,
                    i.dueDate,
                    DATEDIFF(CURDATE(), i.dueDate) as DaysOverdue,
                    DATEDIFF(CURDATE(), i.dueDate) * 2.0 as LateFee
                FROM issuetran i
                JOIN customer c ON i.CustomerID = c.CustomerID
                JOIN movies m ON i.MovieID = m.MovieID
                WHERE i.ReturnDate IS NULL AND i.dueDate < CURDATE()
                ORDER BY DaysOverdue DESC
            """
            overdue_rentals = db.fetch_data(query2)
            
            # Rental statistics by genre
            query3 = """
                SELECT 
                    m.Genre,
                    COUNT(i.IssueID) as TotalRentals,
                    SUM(CASE WHEN i.ReturnDate IS NULL THEN 1 ELSE 0 END) as ActiveRentals,
                    SUM(CASE WHEN i.ReturnDate IS NOT NULL THEN 1 ELSE 0 END) as CompletedRentals,
                    AVG(m.RentalPrice) as AvgRentalPrice
                FROM movies m
                LEFT JOIN issuetran i ON m.MovieID = i.MovieID
                GROUP BY m.Genre
                ORDER BY TotalRentals DESC
            """
            genre_stats = db.fetch_data(query3)
            
            # Rental statistics by producer
            query4 = """
                SELECT 
                    p.Name as Producer,
                    COUNT(i.IssueID) as TotalRentals,
                    SUM(m.RentalPrice) as TotalRevenue
                FROM producers p
                JOIN movies m ON p.ProducerID = m.ProducerID
                LEFT JOIN issuetran i ON m.MovieID = i.MovieID
                GROUP BY p.ProducerID
                ORDER BY TotalRentals DESC
                LIMIT 20
            """
            producer_stats = db.fetch_data(query4)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/Rental_Report_{timestamp}.xlsx"
            
            # Create Excel writer
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Currently rented
                if currently_rented:
                    df1 = pd.DataFrame(currently_rented)
                    # Ensure date columns are included and properly formatted
                    if 'IssueDate' in df1.columns:
                        df1['IssueDate'] = pd.to_datetime(df1['IssueDate']).dt.strftime('%Y-%m-%d')
                    if 'dueDate' in df1.columns:
                        df1['dueDate'] = pd.to_datetime(df1['dueDate']).dt.strftime('%Y-%m-%d')
                    df1.to_excel(writer, sheet_name='Currently Rented', index=False)
                
                # Overdue rentals
                if overdue_rentals:
                    df2 = pd.DataFrame(overdue_rentals)
                    # Ensure date columns are included and properly formatted
                    if 'IssueDate' in df2.columns:
                        df2['IssueDate'] = pd.to_datetime(df2['IssueDate']).dt.strftime('%Y-%m-%d')
                    if 'dueDate' in df2.columns:
                        df2['dueDate'] = pd.to_datetime(df2['dueDate']).dt.strftime('%Y-%m-%d')
                    df2.to_excel(writer, sheet_name='Overdue Rentals', index=False)
                
                # Genre statistics
                if genre_stats:
                    df3 = pd.DataFrame(genre_stats)
                    df3.to_excel(writer, sheet_name='Statistics by Genre', index=False)
                
                # Producer statistics
                if producer_stats:
                    df4 = pd.DataFrame(producer_stats)
                    df4.to_excel(writer, sheet_name='Top Producers', index=False)
            
            # Show summary
            summary = f"Rental Report Generated!\n\n"
            summary += f"Currently Rented: {len(currently_rented)}\n"
            summary += f"Overdue Rentals: {len(overdue_rentals)}\n"
            summary += f"\nSaved to: {filename}"
            
            messagebox.showinfo("Success", summary)
            
            # Show visualization
            if genre_stats:
                ReportGenerator.show_rental_visualization(genre_stats)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")
    
    @staticmethod
    def show_movie_visualization(df):
        """Show movie statistics visualization"""
        # Create visualization window
        viz_window = tk.Toplevel()
        viz_window.title("Movie Statistics Visualization")
        viz_window.geometry("1000x600")
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Movie Rental Statistics', fontsize=16, fontweight='bold')
        
        # 1. Movies by Genre
        genre_counts = df['Genre'].value_counts()
        ax1.pie(genre_counts.values, labels=genre_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Movies Distribution by Genre')
        
        # 2. Rentals by Genre
        genre_rentals = df.groupby('Genre')['TotalRentals'].sum().sort_values(ascending=False)
        ax2.bar(genre_rentals.index, genre_rentals.values, color=['#3498db', '#e74c3c', '#2ecc71'])
        ax2.set_title('Total Rentals by Genre')
        ax2.set_xlabel('Genre')
        ax2.set_ylabel('Total Rentals')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Top 10 Most Rented Movies
        top_10 = df.nlargest(10, 'TotalRentals')
        ax3.barh(range(len(top_10)), top_10['TotalRentals'].values, color='#9b59b6')
        ax3.set_yticks(range(len(top_10)))
        ax3.set_yticklabels(top_10['Title'].values, fontsize=8)
        ax3.set_title('Top 10 Most Rented Movies')
        ax3.set_xlabel('Number of Rentals')
        ax3.invert_yaxis()
        
        # 4. Average Price by Genre
        avg_price = df.groupby('Genre')['RentalPrice'].mean()
        ax4.bar(avg_price.index, avg_price.values, color=['#f39c12', '#1abc9c', '#e67e22'])
        ax4.set_title('Average Rental Price by Genre')
        ax4.set_xlabel('Genre')
        ax4.set_ylabel('Average Price ($)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Embed in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Close button
        close_btn = tk.Button(
            viz_window,
            text="Close",
            command=viz_window.destroy,
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            cursor='hand2'
        )
        close_btn.pack(pady=10)
    
    @staticmethod
    def show_rental_visualization(genre_stats):
        """Show rental statistics visualization"""
        # Create visualization window
        viz_window = tk.Toplevel()
        viz_window.title("Rental Statistics Visualization")
        viz_window.geometry("1000x600")
        
        # Convert to DataFrame
        df = pd.DataFrame(genre_stats)
        
        # Create figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Rental Statistics by Genre', fontsize=16, fontweight='bold')
        
        # 1. Total Rentals by Genre
        ax1.bar(df['Genre'], df['TotalRentals'], color='#3498db')
        ax1.set_title('Total Rentals per Genre')
        ax1.set_xlabel('Genre')
        ax1.set_ylabel('Total Rentals')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Active vs Completed Rentals
        x = range(len(df))
        width = 0.35
        ax2.bar([i - width/2 for i in x], df['ActiveRentals'], width, label='Active', color='#e74c3c')
        ax2.bar([i + width/2 for i in x], df['CompletedRentals'], width, label='Completed', color='#2ecc71')
        ax2.set_title('Active vs Completed Rentals')
        ax2.set_xlabel('Genre')
        ax2.set_ylabel('Number of Rentals')
        ax2.set_xticks(x)
        ax2.set_xticklabels(df['Genre'])
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Rental Distribution Pie Chart
        ax3.pie(df['TotalRentals'], labels=df['Genre'], autopct='%1.1f%%', startangle=90)
        ax3.set_title('Rental Distribution by Genre')
        
        # 4. Average Rental Price by Genre
        ax4.bar(df['Genre'], df['AvgRentalPrice'], color='#9b59b6')
        ax4.set_title('Average Rental Price by Genre')
        ax4.set_xlabel('Genre')
        ax4.set_ylabel('Average Price ($)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Embed in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Close button
        close_btn = tk.Button(
            viz_window,
            text="Close",
            command=viz_window.destroy,
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            cursor='hand2'
        )
        close_btn.pack(pady=10)
