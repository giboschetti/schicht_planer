import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from app import SchichtplanerApp

def main():
    """Main entry point for the application"""
    root = ThemedTk(theme="yaru")  # Use ThemedTk instead of Tk and set yaru theme
    root.title("Schichtplaner")  # Set window title
    
    # Configure the theme colors for better visibility
    style = ttk.Style(root)  # Create style object properly
    style.configure("Treeview", rowheight=25)  # Adjust row height for better readability
    
    app = SchichtplanerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 