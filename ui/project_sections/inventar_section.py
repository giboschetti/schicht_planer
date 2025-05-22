import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from ui.project_sections.base_section import BaseSection

class InventarSection(BaseSection):
    """UI component for the Inventar section"""
    
    def __init__(self, parent, app):
        """Initialize the Inventar section
        
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
        """Set up the UI for the Inventar section"""
        columns = ("ID", "Maschine", "Firma", "Type")
        widths = (50, 200, 150, 100)
        self.inventar_tree = self.create_data_table(columns, widths)
    
    def populate_test_data(self):
        """Add some sample data for testing"""
        firms = ["Firma A", "Firma B", "Firma C"]
        machines = ["Bagger", "Kran", "Betonmischer", "Radlader"]
        types = self.app.dropdown_data.get("machine_types", ["GBM", "ZW-Fahrzeug", "Diverses"])
        
        for i in range(1, 5):
            firm = firms[i % len(firms)]
            machine = machines[i-1]
            type_name = types[i % len(types)]
            self.inventar_tree.insert("", tk.END, values=(
                str(uuid.uuid4()), 
                machine, 
                firm, 
                type_name
            ))
        
        # Store all items for filtering
        self.inventar_tree.all_items = []
        for item_id in self.inventar_tree.get_children():
            self.inventar_tree.all_items.append((item_id, self.inventar_tree.item(item_id, "values")))
    
    def refresh_data(self):
        """Refresh data from Supabase"""
        if not self.app.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.inventar_tree.get_children():
                self.inventar_tree.delete(item)
            
            # Get data from Supabase
            inventar = self.app.supabase_connector.get_inventar()
            
            # Populate tree
            for item in inventar:
                self.inventar_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], 
                    item["maschine"], 
                    item["firma"], 
                    item["type"]
                ))
            
            # Update all_items for filtering
            self.inventar_tree.all_items = []
            for item_id in self.inventar_tree.get_children():
                self.inventar_tree.all_items.append(
                    (item_id, self.inventar_tree.item(item_id, "values"))
                )
        
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren des Inventars: {str(e)}")
    
    def show_add_dialog(self, columns):
        """Show dialog to add a new item
        
        Args:
            columns: List of column names
        """
        # Create the dialog
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Inventar hinzufügen")
        dialog.geometry("400x250")
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
            
            # For the "Type" column, use a dropdown
            if col == "Type":
                entry = ttk.Combobox(form_frame, width=28, 
                                   values=self.app.dropdown_data.get("machine_types", 
                                                                   ["GBM", "ZW-Fahrzeug", "Diverses"]))
            else:
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
                result = self.app.supabase_connector.add_inventar(
                    values["Maschine"],
                    values["Firma"],
                    values["Type"]
                )
                # Get the ID returned from Supabase
                item_id = result[0]["id"]
                all_values = (item_id, values["Maschine"], values["Firma"], values["Type"])
            else:
                item_id = str(uuid.uuid4())
                all_values = (item_id, values["Maschine"], values["Firma"], values["Type"])
            
            # Insert into tree
            self.inventar_tree.insert("", tk.END, iid=item_id, values=all_values)
            
            # Add to all_items for filtering
            self.inventar_tree.all_items.append((item_id, all_values))
            
            # Close the dialog
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
    
    def save_table_edits(self):
        """Save all edits made in edit mode to Supabase"""
        if self.inventar_tree:
            # Complete any ongoing edit
            if self.inventar_tree.current_cell_editor:
                self.finish_cell_edit(self.inventar_tree)
            
            # Update Supabase if connected
            if self.app.is_supabase_connected:
                try:
                    # Get all items
                    for item_id in self.inventar_tree.get_children():
                        values = self.inventar_tree.item(item_id, "values")
                        
                        # Update Supabase
                        self.app.supabase_connector.update_inventar(
                            values[0],  # ID
                            values[1],  # Maschine
                            values[2],  # Firma
                            values[3]   # Type
                        )
                        
                except Exception as e:
                    messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Datenbank: {str(e)}")
                    return
            
            # Exit edit mode
            self.inventar_tree.edit_controls_frame.pack_forget()
            self.inventar_tree.is_in_edit_mode = False
            
            # Re-enable regular buttons
            for child in self.inventar_tree.btn_frame.winfo_children():
                child.configure(state="normal")
            
            messagebox.showinfo("Änderungen gespeichert", "Ihre Änderungen wurden gespeichert.")
            
            # Update the list of all items for filtering
            self.inventar_tree.all_items = []
            for item_id in self.inventar_tree.get_children():
                self.inventar_tree.all_items.append(
                    (item_id, self.inventar_tree.item(item_id, "values"))
                )
            
            # Update dropdown data if connected to Supabase
            if self.app.is_supabase_connected:
                self.app.load_dropdown_data()
                self.app.update_dropdown_values()
    
    def delete_selected_item(self):
        """Delete the selected item from the treeview and Supabase"""
        # Get selected item
        selected = self.inventar_tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Datensatz aus.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Löschen bestätigen", "Möchten Sie diesen Datensatz wirklich löschen?"):
            for item in selected:
                # Get item ID
                item_id = self.inventar_tree.item(item, "values")[0]
                
                # Delete from Supabase if connected
                if self.app.is_supabase_connected:
                    try:
                        self.app.supabase_connector.delete_inventar(item_id)
                    except Exception as e:
                        messagebox.showerror("Fehler", f"Fehler beim Löschen aus der Datenbank: {str(e)}")
                        continue
                
                # Remove from all_items list for filtering
                self.inventar_tree.all_items = [
                    (id, vals) for id, vals in self.inventar_tree.all_items 
                    if id != item
                ]
                
                # Remove from tree
                self.inventar_tree.delete(item)
            
            # Update dropdown data if connected to Supabase
            if self.app.is_supabase_connected:
                self.app.load_dropdown_data()
                self.app.update_dropdown_values() 