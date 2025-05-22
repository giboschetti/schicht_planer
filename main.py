import tkinter as tk
from app import SchichtplanerApp

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = SchichtplanerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 