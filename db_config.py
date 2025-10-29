"""
Database Configuration Module
"""

import mysql.connector
from mysql.connector import Error
import hashlib

class DatabaseConfig:
    
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'Sri@@jan1-1'
        self.database = 'movierental'
        
    def get_connection(self):
        """Create database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def execute_query(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries"""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
                return True
            except Error as e:
                print(f"Error executing query: {e}")
                connection.rollback()
                return False
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return False
    
    def fetch_data(self, query, params=None):
        """Execute SELECT query"""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"Error fetching data: {e}")
                return []
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return []
    
    def fetch_one(self, query, params=None):
        """Fetch single row"""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchone()
                return result
            except Error as e:
                print(f"Error fetching data: {e}")
                return None
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return None
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, employee_id, password):
        """Authenticate employee login"""
        hashed_password = self.hash_password(password)
        
        # Query database with hashed password
        query = "SELECT * FROM employees WHERE EmployeeID = %s AND Password = %s"
        result = self.fetch_one(query, (employee_id, hashed_password))
        
        # If no result with hashed password, try plain text (backward compatibility)
        if result is None:
            result = self.fetch_one(query, (employee_id, password))
        
        return result is not None, result
