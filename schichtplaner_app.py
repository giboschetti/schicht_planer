import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import datetime
from tkcalendar import Calendar
import pandas as pd
import os
import uuid
from excel_connector import ExcelConnector
from supabase_connector import SupabaseConnector
from dotenv import load_dotenv
from multiselect_dropdown import MultiSelectDropdown

class SchichtplanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schichtplaner")
        self.root.geometry("1200x800")
        
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
        
        # Set up the UI for each tab
        self.setup_new_shifts_tab()
        self.setup_view_shifts_tab()
        self.setup_project_data_tab()
        
        # Dictionary to store selected dates
        self.selected_dates = set()
        
        # Create menu bar with Excel import
        self.create_menu()
        
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
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Excel-Datei laden", command=self.load_excel_file)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.quit)
        
        # Supabase menu
        supabase_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datenbank", menu=supabase_menu)
        supabase_menu.add_command(label="Daten von Supabase aktualisieren", 
                                 command=self.refresh_data_from_supabase)
        
    def load_excel_file(self):
        """Open file dialog to select and load Excel file"""
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
        # Update Zeit dropdown
        self.zeit_combo['values'] = self.dropdown_data["zeit"]
        
        # Update Abschnitt dropdown
        self.abschnitt_combo['values'] = self.dropdown_data["abschnitt"]
        
        # Update Bauführer dropdown
        self.baufuhrer_combo['values'] = self.dropdown_data["baufuhrer"]
        
        # Update Arbeitsleiter dropdown
        self.arbeitsleiter_combo['values'] = self.dropdown_data["arbeitsleiter"]
        
        # Update multi-select dropdowns if they exist
        if hasattr(self, 'staff_multi'):
            self.staff_multi.set_values(self.dropdown_data["personal"])
            self.logistik_multi.set_values(self.dropdown_data.get("logistik_personal", []))
            self.ako_multi.set_values(self.dropdown_data.get("ako_personal", []))
            self.sc_multi.set_values(self.dropdown_data.get("sc_personal", []))
            self.siwa_multi.set_values(self.dropdown_data.get("siwa_personal", []))
            self.machine_multi.set_values(self.dropdown_data.get("inventar", []))
            self.gbm_multi.set_values(self.dropdown_data.get("gbm_machines", []))
    
    def setup_new_shifts_tab(self):
        """Set up the UI for adding new shifts"""
        # Split the tab into left (calendar) and right (form) sections
        left_frame = ttk.Frame(self.new_shifts_tab)
        right_frame = ttk.Frame(self.new_shifts_tab)
        
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Calendar section (left side)
        calendar_frame = ttk.LabelFrame(left_frame, text="Kalender")
        calendar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add calendar control
        # We'll use tkcalendar for a more advanced calendar widget
        today = datetime.date.today()
        
        # Create a calendar for date selection
        self.cal = Calendar(calendar_frame, selectmode='day', 
                           year=today.year, month=today.month, 
                           locale='de_DE', showweeknumbers=True,
                           background='white', foreground='black',
                           selectbackground='#ADD8E6')  # Light blue for selection
        self.cal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add labels to display selected dates
        dates_info_frame = ttk.Frame(calendar_frame)
        dates_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.selected_dates_label = ttk.Label(dates_info_frame, text="Ausgewählte Termine: 0")
        self.selected_dates_label.pack(anchor=tk.W)
        
        self.selected_dates_display = ttk.Label(dates_info_frame, text="Keine Daten ausgewählt", 
                                              wraplength=300, justify=tk.LEFT)
        self.selected_dates_display.pack(anchor=tk.W, pady=5)
        
        # Store selected dates
        self.selected_dates = set()
        
        # Bind click event to handle multiple date selection
        self.cal.bind("<<CalendarSelected>>", self.on_date_click)
        
        # Bind month change event to redraw our selections
        self.cal.bind("<<CalendarMonthChanged>>", self.on_month_changed)
        
        # Button to clear calendar selection
        clear_btn = ttk.Button(calendar_frame, text="Auswahl löschen", 
                              command=self.clear_calendar_selection)
        clear_btn.pack(pady=10)
        
        # Form section (right side)
        # Create a scrollable canvas for the form section
        form_canvas = tk.Canvas(right_frame)
        form_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=form_canvas.yview)
        
        form_frame = ttk.LabelFrame(form_canvas, text="Neue Schichten hinzufügen")
        
        # Configure the canvas scroll region when the form frame changes size
        def configure_scroll_region(event):
            form_canvas.configure(scrollregion=form_canvas.bbox("all"))
        
        form_frame.bind("<Configure>", configure_scroll_region)
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw", width=right_frame.winfo_width()-20)
        
        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        form_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        form_scrollbar.pack(side="right", fill="y", pady=10)
        
        # Bind mousewheel events for scrolling
        def _on_mousewheel(event):
            form_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        form_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Row counter for grid layout
        row = 0
        
        # Title
        ttk.Label(form_frame, text="Titel:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.title_entry = ttk.Entry(form_frame, width=40)
        self.title_entry.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Zeit (Time period)
        ttk.Label(form_frame, text="Zeit:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.zeit_combo = ttk.Combobox(form_frame, width=37, values=self.dropdown_data["zeit"])
        self.zeit_combo.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Abschnitt 
        ttk.Label(form_frame, text="Abschnitt:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.abschnitt_combo = ttk.Combobox(form_frame, width=37, values=self.dropdown_data["abschnitt"])
        self.abschnitt_combo.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Bauführer
        ttk.Label(form_frame, text="Bauführer:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.baufuhrer_combo = ttk.Combobox(form_frame, width=37, values=self.dropdown_data["baufuhrer"])
        self.baufuhrer_combo.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Arbeitsleiter
        ttk.Label(form_frame, text="Arbeitsleiter:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.arbeitsleiter_combo = ttk.Combobox(form_frame, width=37, values=self.dropdown_data["arbeitsleiter"])
        self.arbeitsleiter_combo.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Tätigkeit (Activity)
        ttk.Label(form_frame, text="Tätigkeit:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.activity_entry = ttk.Entry(form_frame, width=40)
        self.activity_entry.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Mitarbeiter (Staff) - Now a multi-select dropdown
        ttk.Label(form_frame, text="Mitarbeiter:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.staff_multi = MultiSelectDropdown(form_frame, width=37, 
                                             values=self.dropdown_data["personal"],
                                             placeholder="Mitarbeiter auswählen...")
        self.staff_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2  # Add 2 because MultiSelectDropdown adds a display row
        
        # Logistikpersonal
        ttk.Label(form_frame, text="Logistikpersonal:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        logistik_values = self.dropdown_data.get("logistik_personal", [])
        self.logistik_multi = MultiSelectDropdown(form_frame, width=37, 
                                                values=logistik_values,
                                                placeholder="Logistikpersonal auswählen...")
        self.logistik_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # AKO/Arbeitsstellenkoordinator
        ttk.Label(form_frame, text="AKO/Arbeitsstellenkoordinator:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        ako_values = self.dropdown_data.get("ako_personal", [])
        self.ako_multi = MultiSelectDropdown(form_frame, width=37, 
                                           values=ako_values,
                                           placeholder="AKO auswählen...")
        self.ako_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # Sicherheitschef
        ttk.Label(form_frame, text="Sicherheitschef:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        sc_values = self.dropdown_data.get("sc_personal", [])
        self.sc_multi = MultiSelectDropdown(form_frame, width=37, 
                                          values=sc_values,
                                          placeholder="Sicherheitschef auswählen...")
        self.sc_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # SiWä
        ttk.Label(form_frame, text="SiWä:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        siwa_values = self.dropdown_data.get("siwa_personal", [])
        self.siwa_multi = MultiSelectDropdown(form_frame, width=37, 
                                            values=siwa_values,
                                            placeholder="SiWä auswählen...")
        self.siwa_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # Maschinen (Now a multi-select)
        ttk.Label(form_frame, text="Maschinen:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        machine_values = self.dropdown_data.get("inventar", [])
        self.machine_multi = MultiSelectDropdown(form_frame, width=37, 
                                               values=machine_values,
                                               placeholder="Maschinen auswählen...")
        self.machine_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # GBM (Gleisbaumaschinen)
        ttk.Label(form_frame, text="GBM:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        gbm_values = self.dropdown_data.get("gbm_machines", [])
        self.gbm_multi = MultiSelectDropdown(form_frame, width=37, 
                                           values=gbm_values,
                                           placeholder="GBM auswählen...")
        self.gbm_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # Kommentare
        ttk.Label(form_frame, text="Kommentare:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.comments_text = tk.Text(form_frame, width=37, height=5)
        self.comments_text.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Submit button
        self.submit_btn = ttk.Button(form_frame, text="Hinzufügen", command=self.submit_shifts)
        self.submit_btn.grid(column=0, row=row, columnspan=2, pady=20)
    
    def setup_view_shifts_tab(self):
        """Set up the UI for viewing existing shifts"""
        # Use Treeview for table display
        columns = ("id", "datum", "titel", "zeit", "abschnitt", "baufuhrer", "arbeitsleiter", "tatigkeit")
        self.shifts_tree = ttk.Treeview(self.view_shifts_tab, columns=columns, show="headings")
        
        # Define column headings
        self.shifts_tree.heading("id", text="ID")
        self.shifts_tree.heading("datum", text="Datum")
        self.shifts_tree.heading("titel", text="Titel")
        self.shifts_tree.heading("zeit", text="Zeit")
        self.shifts_tree.heading("abschnitt", text="Abschnitt")
        self.shifts_tree.heading("baufuhrer", text="Bauführer")
        self.shifts_tree.heading("arbeitsleiter", text="Arbeitsleiter")
        self.shifts_tree.heading("tatigkeit", text="Tätigkeit")
        
        # Set column widths
        self.shifts_tree.column("id", width=50)
        self.shifts_tree.column("datum", width=100)
        self.shifts_tree.column("titel", width=150)
        self.shifts_tree.column("zeit", width=80)
        self.shifts_tree.column("abschnitt", width=120)
        self.shifts_tree.column("baufuhrer", width=120)
        self.shifts_tree.column("arbeitsleiter", width=120)
        self.shifts_tree.column("tatigkeit", width=200)
        
        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.view_shifts_tab, orient=tk.VERTICAL, command=self.shifts_tree.yview)
        self.shifts_tree.configure(yscroll=scrollbar.set)
        
        # Place the tree and scrollbar
        self.shifts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Load data from Supabase if connected
        if self.is_supabase_connected:
            self.refresh_shifts_view()
        else:
            # Add some test data if not connected
            self.populate_test_shifts()
    
    def on_date_click(self, event=None):
        """Handle date selection to support multiple dates"""
        try:
            # Get the currently selected date from the calendar
            selected_date = self.cal.selection_get()
            
            # Convert date to string for consistent comparison
            date_str = selected_date.strftime("%Y-%m-%d")
            
            # Toggle selection
            if date_str in [d.strftime("%Y-%m-%d") for d in self.selected_dates]:
                # Remove from selection
                self.selected_dates = {d for d in self.selected_dates 
                                    if d.strftime("%Y-%m-%d") != date_str}
            else:
                # Add to selection
                self.selected_dates.add(selected_date)
            
            # Immediately update visual selection (using Calendar built-in methods)
            self.update_calendar_marked_dates()
            
            # Update display of selected dates
            self.update_selected_dates_display()
            
        except Exception as e:
            print(f"Error in date selection: {e}")
    
    def update_calendar_marked_dates(self):
        """Update the calendar's marked dates"""
        try:
            # Clear all marks first
            try:
                self.cal.calevent_remove("all")
            except Exception:
                pass
            
            # Mark all our selected dates
            for date in self.selected_dates:
                # Add event tag for the selected date
                try:
                    # Mark the date (creates a colored box)
                    self.cal.calevent_create(date, "Selected", "selected_date")
                except Exception as e:
                    print(f"Error marking date {date}: {e}")
                
            # Configure the color for our "selected_date" tag
            try:
                self.cal.tag_config("selected_date", background="#ADD8E6", foreground="black")
            except Exception as e:
                print(f"Error configuring tag: {e}")
            
        except Exception as e:
            print(f"Error updating marked dates: {e}")
    
    def update_selected_dates_display(self):
        """Update display of selected dates"""
        # Sort dates for display
        sorted_dates = sorted(self.selected_dates)
        
        # Create formatted date string
        date_list = [d.strftime("%d.%m.%Y") for d in sorted_dates]
        count_text = f"Ausgewählte Termine: {len(sorted_dates)}"
        self.selected_dates_label.config(text=count_text)
        
        # Update the dates display
        if len(date_list) > 0:
            tooltip_text = "\n".join(date_list)
            date_str = ", ".join(date_list[:5])
            if len(date_list) > 5:
                date_str += f" ... (+{len(date_list) - 5} weitere)"
            self.selected_dates_display.config(text=date_str)
        else:
            self.selected_dates_display.config(text="Keine Daten ausgewählt")
    
    def clear_calendar_selection(self):
        """Clear all selected dates in the calendar"""
        # Clear our set of selected dates
        self.selected_dates.clear()
        
        # Reset calendar display
        try:
            self.cal.selection_set(None)
            
            # Clear all marks
            try:
                self.cal.calevent_remove("all")
            except Exception:
                pass
            
            # Update display
            self.update_selected_dates_display()
        except Exception as e:
            print(f"Error clearing selection: {e}")
    
    def submit_shifts(self):
        """Handle submission of new shifts for selected dates"""
        if not self.selected_dates:
            messagebox.showwarning("Keine Daten ausgewählt", "Bitte wählen Sie mindestens ein Datum aus.")
            return
        
        # Get form values
        title = self.title_entry.get()
        zeit = self.zeit_combo.get()
        abschnitt = self.abschnitt_combo.get()
        baufuhrer = self.baufuhrer_combo.get()
        arbeitsleiter = self.arbeitsleiter_combo.get()
        activity = self.activity_entry.get()
        
        # Get values from multi-select dropdowns
        staff = self.staff_multi.get()
        logistik_personal = self.logistik_multi.get()
        ako_personal = self.ako_multi.get()
        sc_personal = self.sc_multi.get()
        siwa_personal = self.siwa_multi.get()
        machines = self.machine_multi.get()
        gbm_machines = self.gbm_multi.get()
        comments = self.comments_text.get("1.0", tk.END).strip()
        
        # Validate required fields
        if not all([title, zeit, abschnitt]):
            messagebox.showwarning("Unvollständige Daten", 
                                 "Bitte füllen Sie mindestens Titel, Zeit und Abschnitt aus.")
            return
        
        # Prepare shifts for insertion
        success_count = 0
        for date in self.selected_dates:
            # Format date as ISO string
            date_iso = date.isoformat()
            
            # Prepare data for Supabase
            shift_data = {
                "titel": title,
                "datum_von": date_iso,
                "schichtzeit": zeit,
                "abschnitt": abschnitt,
                "tatigkeit": activity,
                "baufuhrer": [baufuhrer] if baufuhrer else None,
                "arbeitsleiter": [arbeitsleiter] if arbeitsleiter else None,
                "baugruppe": staff if staff else None,  # Personal (Mitarbeiter)
                "logistikpersonal": logistik_personal if logistik_personal else None,
                "ako": ako_personal if ako_personal else None,
                "sc_1": sc_personal if sc_personal else None,
                "siwa_1": siwa_personal if siwa_personal else None,
                "diverse_maschinen": machines if machines else None,
                "gleisbaumaschine": gbm_machines if gbm_machines else None,
                "kommentare": comments if comments else None
            }
            
            # Save to Supabase if connected
            if self.is_supabase_connected:
                try:
                    # Insert shift
                    result = self.supabase_connector.add_schichtplanung(shift_data)
                    if result:
                        success_count += 1
                except Exception as e:
                    messagebox.showerror("Fehler", f"Fehler beim Speichern der Schicht: {str(e)}")
                    continue
            else:
                # Just show success message when not connected
                success_count += 1
                
                # Add to tree view for demonstration
                date_str = date.strftime("%d.%m.%Y")
                next_id = str(uuid.uuid4())
                self.shifts_tree.insert("", tk.END, values=(
                    next_id, date_str, title, zeit, abschnitt, baufuhrer, arbeitsleiter, activity
                ))
        
        # Show confirmation
        if success_count > 0:
            if success_count == len(self.selected_dates):
                messagebox.showinfo("Schichten hinzugefügt", 
                                   f"Alle {success_count} Schichten wurden erfolgreich hinzugefügt.")
            else:
                messagebox.showinfo("Schichten hinzugefügt", 
                                   f"{success_count} von {len(self.selected_dates)} Schichten wurden hinzugefügt.")
            
            # Clear form and selection
            self.clear_form()
            self.clear_calendar_selection()
            
            # Refresh shifts view
            if self.is_supabase_connected:
                self.refresh_shifts_view()
    
    def clear_form(self):
        """Clear all form fields"""
        self.title_entry.delete(0, tk.END)
        self.zeit_combo.set("")
        self.abschnitt_combo.set("")
        self.baufuhrer_combo.set("")
        self.arbeitsleiter_combo.set("")
        self.activity_entry.delete(0, tk.END)
        
        # Clear multi-select dropdowns
        self.staff_multi.select_none()
        self.logistik_multi.select_none()
        self.ako_multi.select_none()
        self.sc_multi.select_none()
        self.siwa_multi.select_none()
        self.machine_multi.select_none()
        self.gbm_multi.select_none()
        
        # Clear comments
        self.comments_text.delete("1.0", tk.END)
    
    def populate_test_shifts(self):
        """Add some test data to the shifts view"""
        # Clear existing items
        for item in self.shifts_tree.get_children():
            self.shifts_tree.delete(item)
            
        # Add test data
        test_data = [
            (1, "01.05.2023", "Gleisbau West", "Tag", "Abschnitt 1", "Bauführer 1", "Arbeitsleiter 1", "Schienen verlegen"),
            (2, "02.05.2023", "Signaltechnik Ost", "Nacht", "Abschnitt 2", "Bauführer 2", "Arbeitsleiter 2", "Signale installieren"),
            (3, "03.05.2023", "Instandhaltung", "Tag", "Abschnitt 3", "Bauführer 1", "Arbeitsleiter 3", "Wartungsarbeiten")
        ]
        
        for item in test_data:
            self.shifts_tree.insert("", tk.END, values=item)
    
    def add_test_shifts(self, dates, title, zeit, abschnitt, baufuhrer, arbeitsleiter, activity):
        """Add test shifts to the view for the demo"""
        next_id = len(self.shifts_tree.get_children()) + 1
        
        for date in dates:
            date_str = date.strftime("%d.%m.%Y")
            self.shifts_tree.insert("", tk.END, values=(
                next_id, date_str, title, zeit, abschnitt, baufuhrer, arbeitsleiter, activity
            ))
            next_id += 1

    def load_dropdown_data_from_excel(self, excel_path):
        """Load dropdown values from Excel file"""
        try:
            # This would be implemented to read from the Excel file
            # For now, we're using sample data
            pass
        except Exception as e:
            messagebox.showerror("Excel-Fehler", f"Fehler beim Laden der Excel-Daten: {str(e)}")

    def on_month_changed(self, event=None):
        """Handle month change to reapply our selection highlights"""
        self.update_calendar_marked_dates()
        self.update_selected_dates_display()

    def redraw_calendar_with_selections(self):
        """Redraw the calendar with selected dates highlighted"""
        self.update_calendar_marked_dates()
        self.update_selected_dates_display()

    def setup_project_data_tab(self):
        """Set up the UI for the project data tab with 6 different sections"""
        # Create a notebook for the sections inside the project data tab
        self.project_notebook = ttk.Notebook(self.project_data_tab)
        self.project_notebook.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Create frames for each section
        self.abschnitte_frame = ttk.Frame(self.project_notebook)
        self.schichtzeiten_frame = ttk.Frame(self.project_notebook)
        self.arbeitsleiter_frame = ttk.Frame(self.project_notebook)
        self.baufuhrer_frame = ttk.Frame(self.project_notebook)
        self.mitarbeiter_frame = ttk.Frame(self.project_notebook)
        self.inventar_frame = ttk.Frame(self.project_notebook)
        
        # Add frames to notebook
        self.project_notebook.add(self.abschnitte_frame, text="Abschnitte")
        self.project_notebook.add(self.schichtzeiten_frame, text="Schichtzeiten")
        self.project_notebook.add(self.arbeitsleiter_frame, text="Arbeitsleiter")
        self.project_notebook.add(self.baufuhrer_frame, text="Bauführer")
        self.project_notebook.add(self.mitarbeiter_frame, text="Mitarbeiter")
        self.project_notebook.add(self.inventar_frame, text="Inventar")
        
        # Setup each section
        self.setup_abschnitte_section()
        self.setup_schichtzeiten_section()
        self.setup_arbeitsleiter_section()
        self.setup_baufuhrer_section()
        self.setup_mitarbeiter_section()
        self.setup_inventar_section()
    
    def create_data_table(self, parent, columns, column_widths=None):
        """Create a standard data table with scrollbar"""
        # Create a frame for the table and buttons
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Hinzufügen", 
                            command=lambda: self.show_add_dialog(parent, columns))
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(btn_frame, text="Bearbeiten", 
                             command=lambda: self.enter_edit_mode(parent))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Löschen", 
                               command=lambda: self.delete_selected_item(parent))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Edit mode buttons (initially hidden)
        edit_controls_frame = ttk.Frame(frame)
        save_btn = ttk.Button(edit_controls_frame, text="Änderungen Speichern", 
                             command=lambda: self.save_table_edits(parent))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(edit_controls_frame, text="Abbrechen", 
                               command=lambda: self.exit_edit_mode(parent))
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Filter frame above the table
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        # Dictionary to store filter entries
        filter_entries = {}
        
        # Create filter entry for each column
        for i, col in enumerate(columns):
            # Create label and entry widget for each column
            label = ttk.Label(filter_frame, text=f"{col}:")
            label.grid(row=0, column=i*2, padx=2, pady=2, sticky=tk.W)
            
            entry = ttk.Entry(filter_frame, width=10)
            entry.grid(row=0, column=i*2+1, padx=2, pady=2)
            filter_entries[col] = entry
        
        # Add apply filter button
        filter_btn = ttk.Button(filter_frame, text="Filter anwenden", 
                               command=lambda: self.apply_filters(parent, filter_entries))
        filter_btn.grid(row=0, column=len(columns)*2, padx=5, pady=2)
        
        # Add clear filters button
        clear_btn = ttk.Button(filter_frame, text="Filter löschen", 
                              command=lambda: self.clear_filters(parent, filter_entries))
        clear_btn.grid(row=0, column=len(columns)*2+1, padx=5, pady=2)
        
        # Create treeview
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Configure headings and column widths
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            # Set column width if provided
            if column_widths and i < len(column_widths):
                tree.column(col, width=column_widths[i])
            else:
                tree.column(col, width=100)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for tree and scrollbars
        tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Setup direct cell editing via double-click
        tree.bind("<Double-1>", lambda event: self.on_cell_double_click(event, tree))
        
        # Store references to components
        tree.btn_frame = btn_frame
        tree.edit_controls_frame = edit_controls_frame
        tree.filter_frame = filter_frame
        tree.filter_entries = filter_entries
        tree.is_in_edit_mode = False
        tree.all_items = []  # Store all items to support filtering
        tree.current_cell_editor = None
        
        return tree
    
    def enter_edit_mode(self, parent):
        """Enter edit mode for a table"""
        tree = self.get_tree_for_parent(parent)
        if tree:
            # Show edit control buttons
            tree.edit_controls_frame.pack(fill=tk.X, pady=5, after=tree.btn_frame)
            tree.is_in_edit_mode = True
            
            # Disable regular buttons during edit mode
            for child in tree.btn_frame.winfo_children():
                child.configure(state="disabled")
                
            # Notify user they are in edit mode
            messagebox.showinfo("Edit Mode", 
                              "Sie befinden sich jetzt im Bearbeitungsmodus.\n"
                              "Doppelklicken Sie auf ein Feld, um es zu bearbeiten.")
    
    def exit_edit_mode(self, parent):
        """Exit edit mode without saving changes"""
        tree = self.get_tree_for_parent(parent)
        if tree:
            # Cancel any ongoing edit
            if tree.current_cell_editor:
                self.cancel_cell_edit(tree)
                
            # Hide edit control buttons
            tree.edit_controls_frame.pack_forget()
            tree.is_in_edit_mode = False
            
            # Re-enable regular buttons
            for child in tree.btn_frame.winfo_children():
                child.configure(state="normal")
                
            # Refresh tree to original values
            self.refresh_table_data(parent)
    
    def save_table_edits(self, parent):
        """Save all edits made in edit mode to Supabase"""
        tree = self.get_tree_for_parent(parent)
        if tree:
            # Complete any ongoing edit
            if tree.current_cell_editor:
                self.finish_cell_edit(tree)
            
            # Update Supabase if connected
            if self.is_supabase_connected:
                try:
                    # Get all items
                    for item_id in tree.get_children():
                        values = tree.item(item_id, "values")
                        
                        # Update Supabase based on table type
                        if parent == self.abschnitte_frame:
                            self.supabase_connector.update_abschnitt(
                                values[0],  # ID
                                values[1],  # Abschnitt
                                values[2]   # Beschreibung
                            )
                        
                        elif parent == self.schichtzeiten_frame:
                            self.supabase_connector.update_schichtzeit(
                                values[0],  # ID
                                values[1],  # Schicht
                                values[2],  # Zeit von
                                values[3]   # Zeit bis
                            )
                        
                        elif parent == self.arbeitsleiter_frame:
                            self.supabase_connector.update_arbeitsleiter(
                                values[0],  # ID
                                values[1],  # Name
                                values[2],  # Telefon
                                values[3]   # Email
                            )
                        
                        elif parent == self.baufuhrer_frame:
                            self.supabase_connector.update_baufuhrer(
                                values[0],  # ID
                                values[1],  # Name
                                values[2],  # Telefon
                                values[3]   # Email
                            )
                        
                        elif parent == self.mitarbeiter_frame:
                            self.supabase_connector.update_personal(
                                values[0],  # ID
                                values[1],  # Name
                                values[2],  # Funktion
                                values[3],  # Telefon
                                values[4]   # Email
                            )
                        
                        elif parent == self.inventar_frame:
                            self.supabase_connector.update_inventar(
                                values[0],  # ID
                                values[1],  # Maschine
                                values[2],  # Firma
                                values[3]   # Type
                            )
                        
                except Exception as e:
                    messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Datenbank: {str(e)}")
            
            # Exit edit mode
            tree.edit_controls_frame.pack_forget()
            tree.is_in_edit_mode = False
            
            # Re-enable regular buttons
            for child in tree.btn_frame.winfo_children():
                child.configure(state="normal")
            
            messagebox.showinfo("Änderungen gespeichert", "Ihre Änderungen wurden gespeichert.")
            
            # Update the list of all items for filtering
            tree.all_items = []
            for item_id in tree.get_children():
                tree.all_items.append((item_id, tree.item(item_id, "values")))
            
            # Update dropdown data if connected to Supabase
            if self.is_supabase_connected:
                self.load_dropdown_data()
                self.update_dropdown_values()
    
    def on_cell_double_click(self, event, tree):
        """Handle double click on a cell"""
        if not tree.is_in_edit_mode:
            return
            
        # Get the item and column that was clicked
        region = tree.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        column = tree.identify_column(event.x)
        if not column:
            return
            
        # Get column index (remove the # symbol)
        column_index = int(column[1:]) - 1
        
        # If this is the ID column, don't allow editing
        if column_index == 0:  # ID column
            messagebox.showinfo("Information", "Die ID-Spalte kann nicht bearbeitet werden.")
            return
            
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
            
        # If we're already editing, finish the previous edit
        if tree.current_cell_editor:
            self.finish_cell_edit(tree)
            
        # Get the value and position
        current_value = tree.item(item_id, "values")[column_index]
        
        # Get cell bbox for editor positioning
        x, y, width, height = tree.bbox(item_id, column)
        
        # Create an Entry widget for editing
        entry = ttk.Entry(tree)
        entry.insert(0, current_value)
        entry.select_range(0, tk.END)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus_set()
        
        # Store reference to the editor and its target
        tree.current_cell_editor = {
            "entry": entry,
            "item_id": item_id,
            "column_index": column_index,
            "column": column
        }
        
        # Setup event handlers for the editor
        entry.bind("<Return>", lambda e: self.finish_cell_edit(tree))
        entry.bind("<Escape>", lambda e: self.cancel_cell_edit(tree))
        entry.bind("<FocusOut>", lambda e: self.finish_cell_edit(tree))
    
    def finish_cell_edit(self, tree):
        """Complete cell editing and save the value"""
        if not tree.current_cell_editor:
            return
            
        # Get the new value
        new_value = tree.current_cell_editor["entry"].get()
        
        # Get current item values
        item_id = tree.current_cell_editor["item_id"]
        col_idx = tree.current_cell_editor["column_index"]
        values = list(tree.item(item_id, "values"))
        
        # Update the value
        values[col_idx] = new_value
        
        # Update the item
        tree.item(item_id, values=values)
        
        # Remove the editor
        tree.current_cell_editor["entry"].destroy()
        tree.current_cell_editor = None
    
    def cancel_cell_edit(self, tree):
        """Cancel cell editing without saving"""
        if tree.current_cell_editor:
            tree.current_cell_editor["entry"].destroy()
            tree.current_cell_editor = None
    
    def apply_filters(self, parent, filter_entries):
        """Apply filters to the table"""
        tree = self.get_tree_for_parent(parent)
        if tree:
            # Clear current display
            for item in tree.get_children():
                tree.delete(item)
                
            # Get filter values
            filters = {}
            for column, entry in filter_entries.items():
                value = entry.get().strip().lower()
                if value:
                    filters[column] = value
            
            # If no filters, display all items
            if not filters:
                for item_id, values in tree.all_items:
                    tree.insert("", tk.END, values=values)
                return
                
            # Apply filters
            for item_id, values in tree.all_items:
                should_display = True
                
                for column, filter_value in filters.items():
                    # Get the column index
                    columns = tree["columns"]
                    if column in columns:
                        col_idx = columns.index(column)
                        cell_value = str(values[col_idx]).lower()
                        
                        # Check if filter value is in the cell value
                        if filter_value not in cell_value:
                            should_display = False
                            break
                
                if should_display:
                    tree.insert("", tk.END, values=values)
    
    def clear_filters(self, parent, filter_entries):
        """Clear all filters"""
        # Clear all filter entries
        for entry in filter_entries.values():
            entry.delete(0, tk.END)
            
        # Display all items
        self.apply_filters(parent, filter_entries)
    
    def refresh_table_data(self, parent):
        """Refresh the table data to its original state"""
        tree = self.get_tree_for_parent(parent)
        if tree:
            # Clear current display
            for item in tree.get_children():
                tree.delete(item)
                
            # Insert original items
            for _, values in tree.all_items:
                tree.insert("", tk.END, values=values)
    
    def get_tree_for_parent(self, parent):
        """Get the correct tree widget for a parent frame"""
        if parent == self.abschnitte_frame:
            return self.abschnitte_tree
        elif parent == self.schichtzeiten_frame:
            return self.schichtzeiten_tree
        elif parent == self.arbeitsleiter_frame:
            return self.arbeitsleiter_tree
        elif parent == self.baufuhrer_frame:
            return self.baufuhrer_tree
        elif parent == self.mitarbeiter_frame:
            return self.mitarbeiter_tree
        elif parent == self.inventar_frame:
            return self.inventar_tree
        return None
    
    def setup_abschnitte_section(self):
        """Set up the Abschnitte section"""
        columns = ("ID", "Abschnitt", "Beschreibung")
        widths = (50, 150, 350)
        self.abschnitte_tree = self.create_data_table(self.abschnitte_frame, columns, widths)
        
        # If connected to Supabase, get real data
        if self.is_supabase_connected:
            self.refresh_abschnitte_data()
        else:
            # Add some sample data
            for i in range(1, 4):
                self.abschnitte_tree.insert("", tk.END, values=(
                    str(uuid.uuid4()), 
                    f"Abschnitt {i}", 
                    f"Beschreibung für Abschnitt {i}"
                ))
            
            # Store all items for filtering
            self.abschnitte_tree.all_items = []
            for item_id in self.abschnitte_tree.get_children():
                self.abschnitte_tree.all_items.append((item_id, self.abschnitte_tree.item(item_id, "values")))
    
    def setup_schichtzeiten_section(self):
        """Set up the Schichtzeiten section"""
        columns = ("ID", "Schicht", "Zeit von", "Zeit bis")
        widths = (50, 150, 100, 100)
        self.schichtzeiten_tree = self.create_data_table(self.schichtzeiten_frame, columns, widths)
        
        # If connected to Supabase, get real data
        if self.is_supabase_connected:
            self.refresh_schichtzeiten_data()
        else:
            # Add some sample data
            sample_data = [
                (str(uuid.uuid4()), "Früh", "06:00", "14:00"),
                (str(uuid.uuid4()), "Spät", "14:00", "22:00"),
                (str(uuid.uuid4()), "Nacht", "22:00", "06:00")
            ]
            for item in sample_data:
                self.schichtzeiten_tree.insert("", tk.END, values=item)
            
            # Store all items for filtering
            self.schichtzeiten_tree.all_items = []
            for item_id in self.schichtzeiten_tree.get_children():
                self.schichtzeiten_tree.all_items.append((item_id, self.schichtzeiten_tree.item(item_id, "values")))
    
    def setup_arbeitsleiter_section(self):
        """Set up the Arbeitsleiter section"""
        columns = ("ID", "Name", "Telefon", "Email")
        widths = (50, 150, 150, 200)
        self.arbeitsleiter_tree = self.create_data_table(self.arbeitsleiter_frame, columns, widths)
        
        # If connected to Supabase, get real data
        if self.is_supabase_connected:
            self.refresh_arbeitsleiter_data()
        else:
            # Add some sample data
            for i in range(1, 4):
                self.arbeitsleiter_tree.insert("", tk.END, values=(
                    str(uuid.uuid4()),
                    f"Arbeitsleiter {i}", 
                    f"+49 123 456{i}", 
                    f"arbeitsleiter{i}@example.com"
                ))
            
            # Store all items for filtering
            self.arbeitsleiter_tree.all_items = []
            for item_id in self.arbeitsleiter_tree.get_children():
                self.arbeitsleiter_tree.all_items.append((item_id, self.arbeitsleiter_tree.item(item_id, "values")))
    
    def setup_baufuhrer_section(self):
        """Set up the Bauführer section"""
        columns = ("ID", "Name", "Telefon", "Email")
        widths = (50, 150, 150, 200)
        self.baufuhrer_tree = self.create_data_table(self.baufuhrer_frame, columns, widths)
        
        # If connected to Supabase, get real data
        if self.is_supabase_connected:
            self.refresh_baufuhrer_data()
        else:
            # Add some sample data
            for i in range(1, 4):
                self.baufuhrer_tree.insert("", tk.END, values=(
                    str(uuid.uuid4()),
                    f"Bauführer {i}", 
                    f"+49 234 567{i}", 
                    f"baufuhrer{i}@example.com"
                ))
            
            # Store all items for filtering
            self.baufuhrer_tree.all_items = []
            for item_id in self.baufuhrer_tree.get_children():
                self.baufuhrer_tree.all_items.append((item_id, self.baufuhrer_tree.item(item_id, "values")))
    
    def setup_mitarbeiter_section(self):
        """Set up the Mitarbeiter section"""
        columns = ("ID", "Name", "Funktion", "Telefon", "Email")
        widths = (50, 150, 150, 150, 200)
        self.mitarbeiter_tree = self.create_data_table(self.mitarbeiter_frame, columns, widths)
        
        # If connected to Supabase, get real data
        if self.is_supabase_connected:
            self.refresh_mitarbeiter_data()
        else:
            # Add some sample data
            functions = self.dropdown_data.get("function_types", 
                                             ["Bauarbeiter", "AKO", "SC", "SIWA"])
            for i in range(1, 6):
                func = functions[i % len(functions)]
                self.mitarbeiter_tree.insert("", tk.END, values=(
                    str(uuid.uuid4()),
                    f"Mitarbeiter {i}", 
                    func, 
                    f"+49 345 678{i}", 
                    f"mitarbeiter{i}@example.com"
                ))
            
            # Store all items for filtering
            self.mitarbeiter_tree.all_items = []
            for item_id in self.mitarbeiter_tree.get_children():
                self.mitarbeiter_tree.all_items.append((item_id, self.mitarbeiter_tree.item(item_id, "values")))
    
    def setup_inventar_section(self):
        """Set up the Inventar section"""
        columns = ("ID", "Maschine", "Firma", "Type")
        widths = (50, 200, 150, 100)
        self.inventar_tree = self.create_data_table(self.inventar_frame, columns, widths)
        
        # If connected to Supabase, get real data
        if self.is_supabase_connected:
            self.refresh_inventar_data()
        else:
            # Add sample data for offline mode
            firms = ["Firma A", "Firma B", "Firma C"]
            machines = ["Bagger", "Kran", "Betonmischer", "Radlader"]
            types = self.dropdown_data.get("machine_types", ["GBM", "ZW-Fahrzeug", "Diverses"])
            
            for i in range(1, 5):
                firm = firms[i % len(firms)]
                machine = machines[i-1]
                type_name = types[i % len(types)]
                self.inventar_tree.insert("", tk.END, values=(str(uuid.uuid4()), machine, firm, type_name))
            
            # Store all items for filtering
            self.inventar_tree.all_items = []
            for item_id in self.inventar_tree.get_children():
                self.inventar_tree.all_items.append((item_id, self.inventar_tree.item(item_id, "values")))
    
    def show_add_dialog(self, parent, columns):
        """Show dialog to add a new item"""
        # Create the dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Daten hinzufügen")
        dialog.geometry("400x300")
        dialog.transient(self.root)  # Make dialog modal
        dialog.grab_set()
        
        # Create a frame for the form
        form_frame = ttk.Frame(dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create entry fields for each column (except ID which is auto-generated)
        entries = []
        for i, col in enumerate(columns):
            if col == "ID":  # Skip ID field as it's auto-generated
                continue
            
            ttk.Label(form_frame, text=f"{col}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            # For the "Funktion" column in Mitarbeiter section, use a dropdown
            if parent == self.mitarbeiter_frame and col == "Funktion":
                entry = ttk.Combobox(form_frame, width=28, 
                                   values=self.dropdown_data.get("function_types", 
                                                               ["Bauarbeiter", "AKO", "SC", "SIWA"]))
            # For the "Type" column in Inventar section, use a dropdown
            elif parent == self.inventar_frame and col == "Type":
                entry = ttk.Combobox(form_frame, width=28, 
                                   values=self.dropdown_data.get("machine_types", 
                                                               ["GBM", "ZW-Fahrzeug", "Diverses"]))
            else:
                entry = ttk.Entry(form_frame, width=30)
                
            entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
            entries.append((col, entry))
        
        # Create buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(columns), column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Speichern", 
                  command=lambda: self.save_new_item(parent, entries, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Abbrechen", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_new_item(self, parent, entries, dialog):
        """Save a new item to the appropriate tree view and Supabase"""
        # Get the treeview widget based on the parent
        tree = self.get_tree_for_parent(parent)
        
        if tree:
            # Get values from entries
            values = {}
            
            # Get values from entries
            for col, entry in entries:
                values[col] = entry.get()
            
            try:
                # Save to Supabase based on section type
                if parent == self.abschnitte_frame:
                    if self.is_supabase_connected:
                        result = self.supabase_connector.add_abschnitt(
                            values["Abschnitt"], 
                            values.get("Beschreibung", "")
                        )
                        # Get the ID returned from Supabase
                        item_id = result[0]["id"]
                        all_values = (item_id, values["Abschnitt"], values.get("Beschreibung", ""))
                    else:
                        item_id = str(uuid.uuid4())
                        all_values = (item_id, values["Abschnitt"], values.get("Beschreibung", ""))
                
                elif parent == self.schichtzeiten_frame:
                    if self.is_supabase_connected:
                        result = self.supabase_connector.add_schichtzeit(
                            values["Schicht"], 
                            values["Zeit von"], 
                            values["Zeit bis"]
                        )
                        item_id = result[0]["id"]
                        all_values = (item_id, values["Schicht"], values["Zeit von"], values["Zeit bis"])
                    else:
                        item_id = str(uuid.uuid4())
                        all_values = (item_id, values["Schicht"], values["Zeit von"], values["Zeit bis"])
                
                elif parent == self.arbeitsleiter_frame:
                    if self.is_supabase_connected:
                        result = self.supabase_connector.add_arbeitsleiter(
                            values["Name"], 
                            values["Telefon"], 
                            values["Email"]
                        )
                        item_id = result[0]["id"]
                        all_values = (item_id, values["Name"], values["Telefon"], values["Email"])
                    else:
                        item_id = str(uuid.uuid4())
                        all_values = (item_id, values["Name"], values["Telefon"], values["Email"])
                
                elif parent == self.baufuhrer_frame:
                    if self.is_supabase_connected:
                        result = self.supabase_connector.add_baufuhrer(
                            values["Name"], 
                            values["Telefon"], 
                            values["Email"]
                        )
                        item_id = result[0]["id"]
                        all_values = (item_id, values["Name"], values["Telefon"], values["Email"])
                    else:
                        item_id = str(uuid.uuid4())
                        all_values = (item_id, values["Name"], values["Telefon"], values["Email"])
                
                elif parent == self.mitarbeiter_frame:
                    if self.is_supabase_connected:
                        result = self.supabase_connector.add_personal(
                            values["Name"], 
                            values["Funktion"], 
                            values["Telefon"], 
                            values["Email"]
                        )
                        item_id = result[0]["id"]
                        all_values = (item_id, values["Name"], values["Funktion"], values["Telefon"], values["Email"])
                    else:
                        item_id = str(uuid.uuid4())
                        all_values = (item_id, values["Name"], values["Funktion"], values["Telefon"], values["Email"])
                
                elif parent == self.inventar_frame:
                    if self.is_supabase_connected:
                        result = self.supabase_connector.add_inventar(
                            values["Maschine"],
                            values["Firma"],
                            values["Type"]
                        )
                        item_id = result[0]["id"]
                        all_values = (item_id, values["Maschine"], values["Firma"], values["Type"])
                    else:
                        item_id = str(uuid.uuid4())
                        all_values = (item_id, values["Maschine"], values["Firma"], values["Type"])
                
                else:
                    # Unknown parent, use default
                    item_id = str(uuid.uuid4())
                    all_values = tuple([item_id] + [values[col] for col in values])
                
                # Insert new row in tree view
                tree.insert("", tk.END, iid=item_id, values=all_values)
                
                # Add to all_items for filtering
                tree.all_items.append((item_id, all_values))
                
                # Close the dialog
                dialog.destroy()
                
                # Update dropdown data if connected to Supabase
                if self.is_supabase_connected:
                    self.load_dropdown_data()
                    self.update_dropdown_values()
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
    
    def edit_selected_item(self, parent):
        """This method is replaced by the new inline editing system"""
        pass
    
    def delete_selected_item(self, parent):
        """Delete the selected item from the treeview and Supabase"""
        tree = self.get_tree_for_parent(parent)
        
        if tree:
            # Get selected item
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Datensatz aus.")
                return
            
            # Confirm deletion
            if messagebox.askyesno("Löschen bestätigen", "Möchten Sie diesen Datensatz wirklich löschen?"):
                for item in selected:
                    # Get item ID
                    item_id = tree.item(item, "values")[0]
                    
                    # Delete from Supabase if connected
                    if self.is_supabase_connected:
                        try:
                            if parent == self.abschnitte_frame:
                                self.supabase_connector.delete_abschnitt(item_id)
                            elif parent == self.schichtzeiten_frame:
                                self.supabase_connector.delete_schichtzeit(item_id)
                            elif parent == self.arbeitsleiter_frame:
                                self.supabase_connector.delete_arbeitsleiter(item_id)
                            elif parent == self.baufuhrer_frame:
                                self.supabase_connector.delete_baufuhrer(item_id)
                            elif parent == self.mitarbeiter_frame:
                                self.supabase_connector.delete_personal(item_id)
                            elif parent == self.inventar_frame:
                                self.supabase_connector.delete_inventar(item_id)
                        except Exception as e:
                            messagebox.showerror("Fehler", f"Fehler beim Löschen aus der Datenbank: {str(e)}")
                            continue
                    
                    # Remove from all_items list for filtering
                    tree.all_items = [(id, vals) for id, vals in tree.all_items if id != item]
                    # Remove from tree
                    tree.delete(item)
                
                # Update dropdown data if connected to Supabase
                if self.is_supabase_connected:
                    self.load_dropdown_data()
                    self.update_dropdown_values()
    
    def refresh_data_from_supabase(self):
        """Refresh all data from Supabase"""
        if not self.is_supabase_connected:
            messagebox.showwarning("Keine Verbindung", "Keine Verbindung zu Supabase.")
            return
        
        try:
            # Refresh dropdown data
            self.load_dropdown_data()
            
            # Refresh project data tab
            self.refresh_all_project_data()
            
            # Refresh shifts view
            self.refresh_shifts_view()
            
            messagebox.showinfo("Daten aktualisiert", "Daten wurden erfolgreich von Supabase aktualisiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Daten: {str(e)}")
    
    def refresh_all_project_data(self):
        """Refresh all data in the project data tab"""
        self.refresh_abschnitte_data()
        self.refresh_schichtzeiten_data()
        self.refresh_arbeitsleiter_data()
        self.refresh_baufuhrer_data()
        self.refresh_mitarbeiter_data()
        self.refresh_inventar_data()
    
    def refresh_abschnitte_data(self):
        """Refresh Abschnitte data from Supabase"""
        if not self.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.abschnitte_tree.get_children():
                self.abschnitte_tree.delete(item)
            
            # Get data from Supabase
            abschnitte = self.supabase_connector.get_abschnitte()
            
            # Populate tree
            for item in abschnitte:
                # Store description or empty string if it doesn't exist
                beschreibung = item.get("beschreibung", "")
                
                self.abschnitte_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], item["abschnitt"], beschreibung
                ))
            
            # Update all_items for filtering
            self.abschnitte_tree.all_items = []
            for item_id in self.abschnitte_tree.get_children():
                self.abschnitte_tree.all_items.append((item_id, self.abschnitte_tree.item(item_id, "values")))
        
        except Exception as e:
            print(f"Error refreshing Abschnitte data: {str(e)}")
    
    def refresh_schichtzeiten_data(self):
        """Refresh Schichtzeiten data from Supabase"""
        if not self.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.schichtzeiten_tree.get_children():
                self.schichtzeiten_tree.delete(item)
            
            # Get data from Supabase
            schichtzeiten = self.supabase_connector.get_schichtzeiten()
            
            # Populate tree
            for item in schichtzeiten:
                self.schichtzeiten_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], item["schicht"], item["zeit_von"], item["zeit_bis"]
                ))
            
            # Update all_items for filtering
            self.schichtzeiten_tree.all_items = []
            for item_id in self.schichtzeiten_tree.get_children():
                self.schichtzeiten_tree.all_items.append((item_id, self.schichtzeiten_tree.item(item_id, "values")))
        
        except Exception as e:
            print(f"Error refreshing Schichtzeiten data: {str(e)}")
    
    def refresh_arbeitsleiter_data(self):
        """Refresh Arbeitsleiter data from Supabase"""
        if not self.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.arbeitsleiter_tree.get_children():
                self.arbeitsleiter_tree.delete(item)
            
            # Get data from Supabase
            arbeitsleiter = self.supabase_connector.get_arbeitsleiter()
            
            # Populate tree
            for item in arbeitsleiter:
                self.arbeitsleiter_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], item["name"], item["telefonnummer"], item["email"]
                ))
            
            # Update all_items for filtering
            self.arbeitsleiter_tree.all_items = []
            for item_id in self.arbeitsleiter_tree.get_children():
                self.arbeitsleiter_tree.all_items.append((item_id, self.arbeitsleiter_tree.item(item_id, "values")))
        
        except Exception as e:
            print(f"Error refreshing Arbeitsleiter data: {str(e)}")
    
    def refresh_baufuhrer_data(self):
        """Refresh Bauführer data from Supabase"""
        if not self.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.baufuhrer_tree.get_children():
                self.baufuhrer_tree.delete(item)
            
            # Get data from Supabase
            baufuhrer = self.supabase_connector.get_baufuhrer()
            
            # Populate tree
            for item in baufuhrer:
                self.baufuhrer_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], item["name"], item["telefonnummer"], item["email"]
                ))
            
            # Update all_items for filtering
            self.baufuhrer_tree.all_items = []
            for item_id in self.baufuhrer_tree.get_children():
                self.baufuhrer_tree.all_items.append((item_id, self.baufuhrer_tree.item(item_id, "values")))
        
        except Exception as e:
            print(f"Error refreshing Bauführer data: {str(e)}")
    
    def refresh_mitarbeiter_data(self):
        """Refresh Mitarbeiter data from Supabase"""
        if not self.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.mitarbeiter_tree.get_children():
                self.mitarbeiter_tree.delete(item)
            
            # Get data from Supabase
            personal = self.supabase_connector.get_personal()
            
            # Populate tree
            for item in personal:
                self.mitarbeiter_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], item["name"], item.get("funktion", ""), 
                    item.get("telefonnummer", ""), item.get("email", "")
                ))
            
            # Update all_items for filtering
            self.mitarbeiter_tree.all_items = []
            for item_id in self.mitarbeiter_tree.get_children():
                self.mitarbeiter_tree.all_items.append((item_id, self.mitarbeiter_tree.item(item_id, "values")))
        
        except Exception as e:
            print(f"Error refreshing Mitarbeiter data: {str(e)}")
    
    def refresh_inventar_data(self):
        """Refresh Inventar data from Supabase"""
        if not self.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.inventar_tree.get_children():
                self.inventar_tree.delete(item)
            
            # Get data from Supabase
            inventar = self.supabase_connector.get_inventar()
            
            # Populate tree
            for item in inventar:
                self.inventar_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], item["maschine"], item["firma"], item["type"]
                ))
            
            # Update all_items for filtering
            self.inventar_tree.all_items = []
            for item_id in self.inventar_tree.get_children():
                self.inventar_tree.all_items.append((item_id, self.inventar_tree.item(item_id, "values")))
        
        except Exception as e:
            print(f"Error refreshing Inventar data: {str(e)}")
    
    def refresh_shifts_view(self):
        """Refresh shifts view from Supabase"""
        if not self.is_supabase_connected:
            return
            
        try:
            # Clear current display
            for item in self.shifts_tree.get_children():
                self.shifts_tree.delete(item)
            
            # Get data from Supabase
            shifts = self.supabase_connector.get_schichtplanung()
            
            # Populate tree
            for item in shifts:
                # Format date
                datum = item.get("datum_von", "")
                if datum:
                    try:
                        # Try to parse the date if it's a string
                        if isinstance(datum, str):
                            datum = datetime.datetime.fromisoformat(datum.replace('Z', '+00:00'))
                        # Format as DD.MM.YYYY
                        datum = datum.strftime("%d.%m.%Y")
                    except Exception:
                        pass
                
                self.shifts_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"],
                    datum,
                    item.get("titel", ""),
                    item.get("schichtzeit", ""),
                    item.get("abschnitt", ""),
                    item.get("baufuhrer", ""),
                    item.get("arbeitsleiter", ""),
                    item.get("tatigkeit", "")
                ))
        
        except Exception as e:
            print(f"Error refreshing shifts data: {str(e)}")

def main():
    root = tk.Tk()
    app = SchichtplanerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 