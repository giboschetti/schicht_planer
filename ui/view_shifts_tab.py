import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import datetime
from ui.project_sections.base_section import BaseSection

class ViewShiftsTab(BaseSection):
    """UI component for the 'View Shifts' tab"""
    
    def __init__(self, parent, app):
        """Initialize the View Shifts tab
        
        Args:
            parent: Parent widget (tab frame)
            app: Main application instance
        """
        super().__init__(parent, app)
        
        # Set up the UI
        self.setup_ui()
        
        # Load initial data
        if self.app.is_supabase_connected:
            self.refresh_data()
        else:
            messagebox.showwarning("No Connection", "Not connected to database. Please check your connection settings.")
    
    def setup_ui(self):
        """Set up the UI components"""
        # Define columns and their widths
        columns = [
            'id', 'datum', 'titel', 'zeit', 'abschnitt', 'baufuhrer', 'arbeitsleiter',
            'tatigkeit', 'baugruppe', 'ako', 'sc_1', 'siwa_1', 'logistikpersonal',
            'gleisbaumaschine', 'diverse_maschinen', 'kommentare'
        ]
        
        column_widths = [
            60,   # id
            100,  # datum
            150,  # titel
            100,  # zeit
            100,  # abschnitt
            150,  # baufuhrer
            150,  # arbeitsleiter
            200,  # tatigkeit
            150,  # baugruppe
            100,  # ako
            100,  # sc_1
            100,  # siwa_1
            150,  # logistikpersonal
            200,  # gleisbaumaschine
            200,  # diverse_maschinen
            200   # kommentare
        ]
        
        # Create the tree using BaseSection's method
        self.shifts_tree = self.create_data_table(columns, column_widths)
        
        # Store reference to tree
        self.tree = self.shifts_tree
    
    def refresh_data(self):
        """Refresh data from Supabase"""
        if not self.app.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.shifts_tree.get_children():
                self.shifts_tree.delete(item)
            
            # Initialize all_items if it doesn't exist
            if not hasattr(self.shifts_tree, 'all_items'):
                self.shifts_tree.all_items = []
            
            # Get data from Supabase
            shifts = self.app.supabase_connector.get_schichtplanung()
            
            # Ensure shifts is not None and is iterable
            if shifts is None:
                shifts = []
            
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
                
                # Handle array/list values (convert to string)
                baufuhrer = item.get("baufuhrer", "")
                if isinstance(baufuhrer, list) and baufuhrer:
                    baufuhrer = ", ".join(baufuhrer)
                
                arbeitsleiter = item.get("arbeitsleiter", "")
                if isinstance(arbeitsleiter, list) and arbeitsleiter:
                    arbeitsleiter = ", ".join(arbeitsleiter)
                
                gleisbaumaschine = item.get("gleisbaumaschine", "")
                if isinstance(gleisbaumaschine, list) and gleisbaumaschine:
                    gleisbaumaschine = ", ".join(gleisbaumaschine)
                
                diverse_maschinen = item.get("diverse_maschinen", "")
                if isinstance(diverse_maschinen, list) and diverse_maschinen:
                    diverse_maschinen = ", ".join(diverse_maschinen)
                
                values = (
                    item.get("id", str(uuid.uuid4())),  # Ensure we always have an ID
                    datum,
                    item.get("titel", ""),
                    item.get("schichtzeit", ""),
                    item.get("abschnitt", ""),
                    baufuhrer,
                    arbeitsleiter,
                    item.get("tatigkeit", ""),
                    item.get("baugruppe", ""),
                    item.get("ako", ""),
                    item.get("sc_1", ""),
                    item.get("siwa_1", ""),
                    item.get("logistikpersonal", ""),
                    gleisbaumaschine,
                    diverse_maschinen,
                    item.get("kommentare", "")
                )
                
                try:
                    self.shifts_tree.insert("", tk.END, iid=values[0], values=values)
                except tk.TclError as e:
                    print(f"Error inserting item: {e}")
                    continue
            
            # Update all_items for filtering
            self.shifts_tree.all_items = []
            for item_id in self.shifts_tree.get_children():
                self.shifts_tree.all_items.append(
                    (item_id, self.shifts_tree.item(item_id, "values"))
                )
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load shifts data from database: {str(e)}")
            raise  # Re-raise the exception for debugging
    
    def save_table_edits(self):
        """Save all edits made in edit mode to Supabase"""
        if not self.app.is_supabase_connected:
            messagebox.showerror("Error", "Not connected to database")
            return
        
        try:
            for item_id in self.shifts_tree.get_children():
                values = self.shifts_tree.item(item_id)['values']
                
                # Convert date from DD.MM.YYYY to YYYY-MM-DD
                date_str = values[1]  # Get date in DD.MM.YYYY format
                try:
                    # Parse the German format date
                    date_obj = datetime.datetime.strptime(date_str, "%d.%m.%Y")
                    # Convert to ISO format
                    iso_date = date_obj.strftime("%Y-%m-%d")
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid date format: {date_str}. Please use DD.MM.YYYY format.")
                    return
                
                # Convert string lists back to arrays
                baufuhrer = [x.strip() for x in values[5].split(",")] if values[5] else []
                arbeitsleiter = [x.strip() for x in values[6].split(",")] if values[6] else []
                gleisbaumaschine = [x.strip() for x in values[13].split(",")] if values[13] else []
                diverse_maschinen = [x.strip() for x in values[14].split(",")] if values[14] else []
                
                # Convert values to dictionary
                update_data = {
                    'datum_von': iso_date,  # Use ISO format date
                    'titel': values[2],
                    'schichtzeit': values[3],  # zeit
                    'abschnitt': values[4],
                    'baufuhrer': baufuhrer,
                    'arbeitsleiter': arbeitsleiter,
                    'tatigkeit': values[7],
                    'baugruppe': values[8],
                    'ako': values[9],
                    'sc_1': values[10],
                    'siwa_1': values[11],
                    'logistikpersonal': values[12],
                    'gleisbaumaschine': gleisbaumaschine,
                    'diverse_maschinen': diverse_maschinen,
                    'kommentare': values[15]
                }
                
                # Update in Supabase
                self.app.supabase_connector.update_schichtplanung(values[0], update_data)
            
            messagebox.showinfo("Success", "Changes saved successfully")
            self.exit_edit_mode()
            self.refresh_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
    
    def show_add_dialog(self, columns):
        """Show dialog to add a new item - not implemented for shifts view"""
        messagebox.showinfo("Information", "Please use the 'New Shifts' tab to add new shifts.")
    
    def delete_selected_item(self):
        """Delete the selected item from the treeview and Supabase"""
        selected_items = self.shifts_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select items to delete")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected items?"):
            return
        
        if not self.app.is_supabase_connected:
            messagebox.showerror("Error", "Not connected to database")
            return
        
        try:
            for item in selected_items:
                item_id = self.shifts_tree.item(item)['values'][0]
                self.app.supabase_connector.delete_schichtplanung(item_id)
                self.shifts_tree.delete(item)
            
            messagebox.showinfo("Success", "Items deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete items: {str(e)}")
    
    def add_shift_to_view(self, shift_id, datum, titel, zeit, abschnitt, baufuhrer, arbeitsleiter, tatigkeit,
                         baugruppe="", ako="", sc_1="", siwa_1="", logistikpersonal="", 
                         gleisbaumaschine="", diverse_maschinen="", kommentare=""):
        """Add a single shift to the view (used when adding shifts without Supabase)
        
        Args:
            shift_id (str): Unique identifier for the shift
            datum (str): Date in DD.MM.YYYY format
            titel (str): Title of the shift
            zeit (str): Time of the shift
            abschnitt (str): Section
            baufuhrer (str): Construction manager(s)
            arbeitsleiter (str): Work manager(s)
            tatigkeit (str): Activity description
            baugruppe (str, optional): Construction group
            ako (str, optional): AKO value
            sc_1 (str, optional): SC 1 value
            siwa_1 (str, optional): SIWA 1 value
            logistikpersonal (str, optional): Logistics personnel
            gleisbaumaschine (str, optional): Track construction machine
            diverse_maschinen (str, optional): Various machines
            kommentare (str, optional): Comments
        """
        values = (
            shift_id, datum, titel, zeit, abschnitt, baufuhrer, arbeitsleiter, tatigkeit,
            baugruppe, ako, sc_1, siwa_1, logistikpersonal, gleisbaumaschine,
            diverse_maschinen, kommentare
        )
        
        # Insert into tree
        self.shifts_tree.insert("", tk.END, iid=shift_id, values=values)
        
        # Add to all_items for filtering
        self.shifts_tree.all_items.append((shift_id, values))
    
    def get_options_for_column(self, column):
        """Get available options for a column from related tables"""
        if not self.app.is_supabase_connected:
            return []
            
        try:
            if column == 'baufuhrer':
                baufuhrer = self.app.supabase_connector.get_baufuhrer()
                return [item['name'] for item in baufuhrer] if baufuhrer else []
            elif column == 'arbeitsleiter':
                arbeitsleiter = self.app.supabase_connector.get_arbeitsleiter()
                return [item['name'] for item in arbeitsleiter] if arbeitsleiter else []
            elif column == 'baugruppe':
                baugruppen = self.app.supabase_connector.get_baugruppen()
                return [item['name'] for item in baugruppen] if baugruppen else []
            elif column == 'gleisbaumaschine':
                maschinen = self.app.supabase_connector.get_inventar()
                return [item['maschine'] for item in maschinen if item.get('type') == 'GBM'] if maschinen else []
            elif column == 'diverse_maschinen':
                maschinen = self.app.supabase_connector.get_inventar()
                return [item['maschine'] for item in maschinen if item.get('type') == 'Diverses'] if maschinen else []
        except Exception as e:
            print(f"Error getting options for {column}: {str(e)}")
            return []
        
        return []
    
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
            
        # Get column index and name
        column_index = int(column[1:]) - 1
        column_name = tree.heading(column)['text']
        
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
        
        # Get the current value
        current_values = tree.item(item_id)['values']
        current_value = str(current_values[column_index]) if current_values[column_index] is not None else ""
        
        # Get cell bbox for editor positioning
        x, y, width, height = tree.bbox(item_id, column)
        
        # Check if this is a multi-select field
        if column_name in ['baufuhrer', 'arbeitsleiter', 'baugruppe', 'gleisbaumaschine', 'diverse_maschinen']:
            # Get available options
            options = self.get_options_for_column(column_name)
            
            # Create a toplevel window for the listbox
            dialog = tk.Toplevel(tree)
            dialog.title(f"Bearbeiten: {column_name}")
            dialog.transient(tree)
            dialog.grab_set()
            
            # Create frame for listbox and scrollbar
            frame = ttk.Frame(dialog, padding="10")
            frame.pack(fill=tk.BOTH, expand=True)
            
            # Add label
            ttk.Label(frame, text=f"Werte auswählen:").pack(anchor=tk.W)
            
            # Create listbox with scrollbar
            list_frame = ttk.Frame(frame)
            list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
            
            listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, width=40, height=10)
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
            listbox.configure(yscrollcommand=scrollbar.set)
            
            # Pack listbox and scrollbar
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate listbox and select current values
            current_values = [v.strip() for v in current_value.split(",")] if current_value else []
            for option in options:
                listbox.insert(tk.END, option)
                if option in current_values:
                    listbox.select_set(listbox.size() - 1)
            
            # Button frame
            button_frame = ttk.Frame(frame)
            button_frame.pack(fill=tk.X, pady=(10, 0))
            
            def save():
                selections = [listbox.get(i) for i in listbox.curselection()]
                new_value = ", ".join(selections)
                
                # Update the tree
                values = list(tree.item(item_id)['values'])
                values[column_index] = new_value
                tree.item(item_id, values=values)
                
                dialog.destroy()
            
            def cancel():
                dialog.destroy()
            
            # Add OK and Cancel buttons
            ttk.Button(button_frame, text="OK", command=save, width=10).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(button_frame, text="Abbrechen", command=cancel, width=10).pack(side=tk.LEFT)
            
            # Center dialog relative to parent window
            dialog.geometry(f"+{tree.winfo_rootx() + 50}+{tree.winfo_rooty() + 50}")
            
        else:
            # For regular fields, create an Entry widget
            entry = ttk.Entry(tree)
            entry.insert(0, current_value)
            
            # Position and show the entry widget
            entry.place(x=x, y=y, width=width, height=height)
            entry.focus_set()
            
            # Store reference to current editor
            tree.current_cell_editor = {
                'widget': entry,
                'item_id': item_id,
                'column': column,
                'column_index': column_index
            }
            
            # Bind events
            entry.bind('<Return>', lambda e: self.finish_cell_edit(tree))
            entry.bind('<Escape>', lambda e: self.cancel_cell_edit(tree))
            entry.bind('<FocusOut>', lambda e: self.finish_cell_edit(tree))