import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from ui.project_sections.base_section import BaseSection

class ArbeitsleiterSection(BaseSection):
    """UI component for the Arbeitsleiter section"""
    
    def __init__(self, parent, app):
        """Initialize the Arbeitsleiter section
        
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
        """Set up the UI for the Arbeitsleiter section"""
        columns = ("ID", "Name", "Telefon", "Email")
        widths = (50, 150, 150, 200)
        self.arbeitsleiter_tree = self.create_data_table(columns, widths)
    
    def populate_test_data(self):
        """Add some sample data for testing"""
        # Add some test data
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
    
    def refresh_data(self):
        """Refresh data from Supabase"""
        if not self.app.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.arbeitsleiter_tree.get_children():
                self.arbeitsleiter_tree.delete(item)
            
            # Get data from Supabase
            arbeitsleiter = self.app.supabase_connector.get_arbeitsleiter()
            
            # Populate tree
            for item in arbeitsleiter:
                self.arbeitsleiter_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], 
                    item["name"], 
                    item["telefonnummer"], 
                    item["email"]
                ))
            
            # Update all_items for filtering
            self.arbeitsleiter_tree.all_items = []
            for item_id in self.arbeitsleiter_tree.get_children():
                self.arbeitsleiter_tree.all_items.append(
                    (item_id, self.arbeitsleiter_tree.item(item_id, "values"))
                )
        
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Arbeitsleiter: {str(e)}")
    
    def show_add_dialog(self, columns):
        """Show dialog to add a new item"""
        # TODO: Implement similar to AbschnitteSection with appropriate data
        pass
    
    def save_new_item(self, entries, dialog):
        """Save a new item to the database"""
        # TODO: Implement similar to AbschnitteSection with appropriate data
        pass
    
    def save_table_edits(self):
        """Save all edits made in edit mode to Supabase"""
        # TODO: Implement similar to AbschnitteSection with appropriate data
        pass
    
    def delete_selected_item(self):
        """Delete the selected item from the treeview and Supabase"""
        # TODO: Implement similar to AbschnitteSection with appropriate data
        pass 