import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv
import os

from connectors.excel_connector import ExcelConnector
from connectors.supabase_connector import SupabaseConnector
from ui.new_shifts_tab import NewShiftsTab
from ui.view_shifts_tab import ViewShiftsTab
from ui.project_data_tab import ProjectDataTab

class SchichtplanerApp:
    def __init__(self, root):
        """Initialize the main application"""
        self.root = root
        self.root.title("Schichtplaner")
        self.root.geometry("1200x800")
        
        # Configure ttk styles
        self.configure_styles()
        
        # Load environment variables
        load_dotenv()
        
        # Main tab control
        self.tab_control = ttk.Notebook(root)
        
        # Create tabs
        self.new_shifts_tab = ttk.Frame(self.tab_control)
        self.view_shifts_tab = ttk.Frame(self.tab_control)
        self.project_data_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.new_shifts_tab, text="Neue Schichten")
        self.tab_control.add(self.view_shifts_tab, text="Schichten")
        self.tab_control.add(self.project_data_tab, text="Projektdata")
        self.tab_control.pack(expand=1, fill="both")
        
        # Initialize connectors
        self.excel_connector = ExcelConnector()
        
        try:
            self.supabase_connector = SupabaseConnector()
            self.is_supabase_connected = True
        except Exception as e:
            self.is_supabase_connected = False
            messagebox.showwarning(
                "Supabase Verbindung", 
                f"Konnte nicht mit Supabase verbinden. Lokale Daten werden verwendet.\nFehler: {str(e)}"
            )
        
        # Sample data for dropdowns - will be loaded from Excel/Supabase
        self.dropdown_data = {
            "abschnitt": ["Abschnitt 1", "Abschnitt 2", "Abschnitt 3"],
            "baufuhrer": ["Bauführer 1", "Bauführer 2", "Bauführer 3"],
            "arbeitsleiter": ["Arbeitsleiter 1", "Arbeitsleiter 2", "Arbeitsleiter 3"],
            "zeit": ["Tag", "Nacht", "Spät"],
            "personal": ["Mitarbeiter 1", "Mitarbeiter 2", "Mitarbeiter 3"],
        }
        
        # Try to load dropdown data from Supabase
        self.load_dropdown_data()
        
        # Initialize tab UI components
        self.new_shifts_ui = NewShiftsTab(self.new_shifts_tab, self)
        self.view_shifts_ui = ViewShiftsTab(self.view_shifts_tab, self)
        self.project_data_ui = ProjectDataTab(self.project_data_tab, self)
        
        # Create menu bar with Excel import
        self.create_menu()
        
    def configure_styles(self):
        """Configure ttk styles for consistent theming"""
        style = ttk.Style()
        
        # Configure Treeview
        style.configure("Treeview",
                       rowheight=25,
                       fieldbackground="white")
        style.configure("Treeview.Heading",
                       font=('TkDefaultFont', 9, 'bold'))
        
        # Configure Buttons
        style.configure("TButton",
                       padding=5)
        
        # Configure Entry fields
        style.configure("TEntry",
                       padding=5)
        
        # Configure Combobox
        style.configure("TCombobox",
                       padding=5)
        
        # Configure Notebook (Tabs)
        style.configure("TNotebook",
                       tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab",
                       padding=[10, 2])
        
    def load_dropdown_data(self):
        """Load dropdown data from Supabase if connected"""
        if self.is_supabase_connected:
            try:
                self.dropdown_data = self.supabase_connector.get_dropdown_data()
                print("Dropdown data loaded from Supabase")
            except Exception as e:
                print(f"Error loading dropdown data from Supabase: {str(e)}")
        
    def create_menu(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root, relief='flat', background='#f0f0f0', activebackground='#e0e0e0')
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, relief='flat', background='#f0f0f0', activebackground='#e0e0e0')
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Excel-Datei laden", command=self.load_excel_file)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.quit)
        
        # Supabase menu
        supabase_menu = tk.Menu(menubar, tearoff=0, relief='flat', background='#f0f0f0', activebackground='#e0e0e0')
        menubar.add_cascade(label="Datenbank", menu=supabase_menu)
        supabase_menu.add_command(label="Daten von Supabase aktualisieren", 
                                 command=self.refresh_data_from_supabase)
    
    def load_excel_file(self):
        """Open file dialog to select and load Excel file"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Excel-Datei auswählen",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        
        if file_path:
            if self.excel_connector.set_excel_path(file_path):
                try:
                    if self.excel_connector.load_all_sheets():
                        # Update dropdown data and refresh UI
                        self.dropdown_data = self.excel_connector.get_dropdown_data()
                        self.update_dropdown_values()
                        messagebox.showinfo("Excel geladen", 
                                           f"Excel-Daten wurden erfolgreich aus {os.path.basename(file_path)} geladen.")
                    else:
                        messagebox.showerror("Fehler", "Fehler beim Laden der Excel-Daten.")
                except Exception as e:
                    messagebox.showerror("Excel-Fehler", f"Fehler: {str(e)}")
            else:
                messagebox.showerror("Dateifehler", "Die ausgewählte Datei existiert nicht.")
    
    def update_dropdown_values(self):
        """Update all dropdown values with loaded data"""
        # Forward update to tab UIs
        self.new_shifts_ui.update_dropdown_values(self.dropdown_data)
        self.view_shifts_ui.update_dropdown_values(self.dropdown_data)
        self.project_data_ui.update_dropdown_values(self.dropdown_data)
    
    def refresh_data_from_supabase(self):
        """Refresh all data from Supabase"""
        if not self.is_supabase_connected:
            messagebox.showwarning("Keine Verbindung", "Keine Verbindung zu Supabase.")
            return
        
        try:
            # Refresh dropdown data
            self.load_dropdown_data()
            
            # Update dropdowns in UI
            self.update_dropdown_values()
            
            # Refresh project data tab
            self.project_data_ui.refresh_all_project_data()
            
            # Refresh shifts view using the view_shifts_ui instance
            self.view_shifts_ui.refresh_data()
            
            messagebox.showinfo("Daten aktualisiert", "Daten wurden erfolgreich von Supabase aktualisiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Daten: {str(e)}")
            # Re-raise the exception for debugging
            raise 