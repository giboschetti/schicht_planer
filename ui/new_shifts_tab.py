import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import Calendar
import uuid
from utils.multiselect_dropdown import MultiSelectDropdown

class NewShiftsTab:
    """UI component for the 'New Shifts' tab"""
    
    def __init__(self, parent, app):
        """Initialize the New Shifts tab
        
        Args:
            parent: Parent widget (tab frame)
            app: Main application instance
        """
        self.parent = parent
        self.app = app
        
        # Dictionary to store selected dates
        self.selected_dates = set()
        
        # Set up the UI
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI for adding new shifts"""
        # Split the tab into left (calendar) and right (form) sections
        left_frame = ttk.Frame(self.parent)
        right_frame = ttk.Frame(self.parent)
        
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Calendar section (left side)
        self.setup_calendar_section(left_frame)
        
        # Form section (right side)
        self.setup_form_section(right_frame)
    
    def setup_calendar_section(self, parent):
        """Set up the calendar section
        
        Args:
            parent: Parent frame for the calendar section
        """
        calendar_frame = ttk.LabelFrame(parent, text="Kalender")
        calendar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add calendar control
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
        
        # Bind click event to handle multiple date selection
        self.cal.bind("<<CalendarSelected>>", self.on_date_click)
        
        # Bind month change event to redraw our selections
        self.cal.bind("<<CalendarMonthChanged>>", self.on_month_changed)
        
        # Button to clear calendar selection
        clear_btn = ttk.Button(calendar_frame, text="Auswahl löschen", 
                              command=self.clear_calendar_selection)
        clear_btn.pack(pady=10)
    
    def setup_form_section(self, parent):
        """Set up the form section
        
        Args:
            parent: Parent frame for the form section
        """
        # Create a scrollable canvas for the form section
        form_canvas = tk.Canvas(parent)
        form_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=form_canvas.yview)
        
        form_frame = ttk.LabelFrame(form_canvas, text="Neue Schichten hinzufügen")
        
        # Configure the canvas scroll region when the form frame changes size
        def configure_scroll_region(event):
            form_canvas.configure(scrollregion=form_canvas.bbox("all"))
        
        form_frame.bind("<Configure>", configure_scroll_region)
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw", width=parent.winfo_width()-20)
        
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
        self.zeit_combo = ttk.Combobox(form_frame, width=37, values=self.app.dropdown_data["zeit"])
        self.zeit_combo.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Abschnitt 
        ttk.Label(form_frame, text="Abschnitt:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.abschnitt_combo = ttk.Combobox(form_frame, width=37, values=self.app.dropdown_data["abschnitt"])
        self.abschnitt_combo.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Bauführer
        ttk.Label(form_frame, text="Bauführer:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.baufuhrer_combo = ttk.Combobox(form_frame, width=37, values=self.app.dropdown_data["baufuhrer"])
        self.baufuhrer_combo.grid(column=1, row=row, padx=10, pady=10)
        row += 1
        
        # Arbeitsleiter
        ttk.Label(form_frame, text="Arbeitsleiter:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        self.arbeitsleiter_combo = ttk.Combobox(form_frame, width=37, values=self.app.dropdown_data["arbeitsleiter"])
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
                                             values=self.app.dropdown_data["personal"],
                                             placeholder="Mitarbeiter auswählen...")
        self.staff_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2  # Add 2 because MultiSelectDropdown adds a display row
        
        # Logistikpersonal
        ttk.Label(form_frame, text="Logistikpersonal:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        logistik_values = self.app.dropdown_data.get("logistik_personal", [])
        self.logistik_multi = MultiSelectDropdown(form_frame, width=37, 
                                                values=logistik_values,
                                                placeholder="Logistikpersonal auswählen...")
        self.logistik_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # AKO/Arbeitsstellenkoordinator
        ttk.Label(form_frame, text="AKO/Arbeitsstellenkoordinator:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        ako_values = self.app.dropdown_data.get("ako_personal", [])
        self.ako_multi = MultiSelectDropdown(form_frame, width=37, 
                                           values=ako_values,
                                           placeholder="AKO auswählen...")
        self.ako_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # Sicherheitschef
        ttk.Label(form_frame, text="Sicherheitschef:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        sc_values = self.app.dropdown_data.get("sc_personal", [])
        self.sc_multi = MultiSelectDropdown(form_frame, width=37, 
                                          values=sc_values,
                                          placeholder="Sicherheitschef auswählen...")
        self.sc_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # SiWä
        ttk.Label(form_frame, text="SiWä:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        siwa_values = self.app.dropdown_data.get("siwa_personal", [])
        self.siwa_multi = MultiSelectDropdown(form_frame, width=37, 
                                            values=siwa_values,
                                            placeholder="SiWä auswählen...")
        self.siwa_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # Maschinen (Now a multi-select)
        ttk.Label(form_frame, text="Maschinen:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        machine_values = self.app.dropdown_data.get("inventar", [])
        self.machine_multi = MultiSelectDropdown(form_frame, width=37, 
                                               values=machine_values,
                                               placeholder="Maschinen auswählen...")
        self.machine_multi.grid(column=1, row=row, padx=10, pady=10)
        row += 2
        
        # GBM (Gleisbaumaschinen)
        ttk.Label(form_frame, text="GBM:").grid(column=0, row=row, sticky=tk.W, padx=10, pady=10)
        gbm_values = self.app.dropdown_data.get("gbm_machines", [])
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
    
    def on_month_changed(self, event=None):
        """Handle month change to reapply our selection highlights"""
        self.update_calendar_marked_dates()
        self.update_selected_dates_display()
    
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
            if self.app.is_supabase_connected:
                try:
                    # Insert shift
                    result = self.app.supabase_connector.add_schichtplanung(shift_data)
                    if result:
                        success_count += 1
                except Exception as e:
                    messagebox.showerror("Fehler", f"Fehler beim Speichern der Schicht: {str(e)}")
                    continue
            else:
                # Just show success message when not connected
                success_count += 1
                
                # Add to tree view for demonstration - pass to view shifts tab
                date_str = date.strftime("%d.%m.%Y")
                next_id = str(uuid.uuid4())
                self.app.view_shifts_ui.add_shift_to_view(
                    next_id, date_str, title, zeit, abschnitt, baufuhrer, arbeitsleiter, activity
                )
        
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
            if self.app.is_supabase_connected:
                self.app.view_shifts_ui.refresh_shifts_view()
    
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
        
    def update_dropdown_values(self, dropdown_data):
        """Update dropdown values when data is refreshed
        
        Args:
            dropdown_data (dict): Updated dropdown data
        """
        # Update Zeit dropdown
        self.zeit_combo['values'] = dropdown_data["zeit"]
        
        # Update Abschnitt dropdown
        self.abschnitt_combo['values'] = dropdown_data["abschnitt"]
        
        # Update Bauführer dropdown
        self.baufuhrer_combo['values'] = dropdown_data["baufuhrer"]
        
        # Update Arbeitsleiter dropdown
        self.arbeitsleiter_combo['values'] = dropdown_data["arbeitsleiter"]
        
        # Update multi-select dropdowns
        self.staff_multi.set_values(dropdown_data["personal"])
        self.logistik_multi.set_values(dropdown_data.get("logistik_personal", []))
        self.ako_multi.set_values(dropdown_data.get("ako_personal", []))
        self.sc_multi.set_values(dropdown_data.get("sc_personal", []))
        self.siwa_multi.set_values(dropdown_data.get("siwa_personal", []))
        self.machine_multi.set_values(dropdown_data.get("inventar", []))
        self.gbm_multi.set_values(dropdown_data.get("gbm_machines", [])) 