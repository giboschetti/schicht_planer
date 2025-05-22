import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from ui.project_sections.base_section import BaseSection

class AbschnitteSection(BaseSection):
    """UI component for the Abschnitte section"""
    
    def __init__(self, parent, app):
        """Initialize the Abschnitte section
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent, app)
        
        # Set up the UI
        self.setup_ui()
        
        # Load initial data
        if self.app.is_supabase_connected:
            self.refresh_data()
        else:
            # Add some test data if not connected
            self.populate_test_data()
    
    def setup_ui(self):
        """Set up the UI for the Abschnitte section"""
        columns = ("ID", "Abschnitt", "Beschreibung")
        widths = (50, 150, 350)
        self.abschnitte_tree = self.create_data_table(columns, widths)
    
    def populate_test_data(self):
        """Add some sample data for testing"""
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
    
    def refresh_data(self):
        """Refresh data from Supabase"""
        if not self.app.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.abschnitte_tree.get_children():
                self.abschnitte_tree.delete(item)
            
            # Get data from Supabase
            abschnitte = self.app.supabase_connector.get_abschnitte()
            
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
                self.abschnitte_tree.all_items.append(
                    (item_id, self.abschnitte_tree.item(item_id, "values"))
                )
        
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Abschnitte: {str(e)}")
    
    def show_add_dialog(self, columns):
        """Show dialog to add a new item
        
        Args:
            columns: List of column names
        """
        # Create the dialog
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Abschnitt hinzufügen")
        dialog.geometry("400x200")
        dialog.transient(self.app.root)  # Make dialog modal
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
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
            entries.append((col, entry))
        
        # Create buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(columns), column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Speichern", 
                  command=lambda: self.save_new_item(entries, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Abbrechen", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_new_item(self, entries, dialog):
        """Save a new item to the database
        
        Args:
            entries: List of (column, entry) tuples
            dialog: Dialog window to close after saving
        """
        # Get values from entries
        values = {}
        for col, entry in entries:
            values[col] = entry.get()
        
        try:
            # Save to Supabase if connected
            if self.app.is_supabase_connected:
                result = self.app.supabase_connector.add_abschnitt(
                    values["Abschnitt"], 
                    values.get("Beschreibung", "")
                )
                # Get the ID returned from Supabase
                item_id = result[0]["id"]
                all_values = (item_id, values["Abschnitt"], values.get("Beschreibung", ""))
            else:
                item_id = str(uuid.uuid4())
                all_values = (item_id, values["Abschnitt"], values.get("Beschreibung", ""))
            
            # Insert into tree
            self.abschnitte_tree.insert("", tk.END, iid=item_id, values=all_values)
            
            # Add to all_items for filtering
            self.abschnitte_tree.all_items.append((item_id, all_values))
            
            # Close the dialog
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
    
    def save_table_edits(self):
        """Save all edits made in edit mode to Supabase"""
        if not self.abschnitte_tree:
            return
            
        # Complete any ongoing edit
        if self.abschnitte_tree.current_cell_editor:
            self.finish_cell_edit(self.abschnitte_tree)
        
        # Update Supabase if connected
        if self.app.is_supabase_connected:
            try:
                # Get all items
                for item_id in self.abschnitte_tree.get_children():
                    values = self.abschnitte_tree.item(item_id, "values")
                    
                    # Update Supabase
                    self.app.supabase_connector.update_abschnitt(
                        values[0],  # ID
                        values[1],  # Abschnitt
                        values[2]   # Beschreibung
                    )
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Abschnitte: {str(e)}")
        
        # Exit edit mode
        self.abschnitte_tree.edit_controls_frame.pack_forget()
        self.abschnitte_tree.is_in_edit_mode = False
        
        # Re-enable regular buttons
        for child in self.abschnitte_tree.btn_frame.winfo_children():
            child.configure(state="normal")
        
        messagebox.showinfo("Änderungen gespeichert", "Ihre Änderungen wurden gespeichert.")
        
        # Update the list of all items for filtering
        self.abschnitte_tree.all_items = []
        for item_id in self.abschnitte_tree.get_children():
            self.abschnitte_tree.all_items.append(
                (item_id, self.abschnitte_tree.item(item_id, "values"))
            )
        
        # Update dropdown data if connected to Supabase
        if self.app.is_supabase_connected:
            self.app.load_dropdown_data()
            self.app.update_dropdown_values()
    
    def delete_selected_item(self):
        """Delete the selected item from the treeview and Supabase"""
        # Get selected item
        selected = self.abschnitte_tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Datensatz aus.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Löschen bestätigen", "Möchten Sie diesen Datensatz wirklich löschen?"):
            for item in selected:
                # Get item ID
                item_id = self.abschnitte_tree.item(item, "values")[0]
                
                # Delete from Supabase if connected
                if self.app.is_supabase_connected:
                    try:
                        self.app.supabase_connector.delete_abschnitt(item_id)
                    except Exception as e:
                        messagebox.showerror("Fehler", f"Fehler beim Löschen aus der Datenbank: {str(e)}")
                        continue
                
                # Remove from all_items list for filtering
                self.abschnitte_tree.all_items = [
                    (id, vals) for id, vals in self.abschnitte_tree.all_items 
                    if id != item
                ]
                
                # Remove from tree
                self.abschnitte_tree.delete(item)
            
            # Update dropdown data if connected to Supabase
            if self.app.is_supabase_connected:
                self.app.load_dropdown_data()
                self.app.update_dropdown_values() 