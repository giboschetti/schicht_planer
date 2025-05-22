import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from ui.project_sections.base_section import BaseSection

class SchichtzeitenSection(BaseSection):
    """UI component for the Schichtzeiten section"""
    
    def __init__(self, parent, app):
        """Initialize the Schichtzeiten section
        
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
        """Set up the UI for the Schichtzeiten section"""
        columns = ("ID", "Schicht", "Zeit von", "Zeit bis")
        widths = (50, 150, 100, 100)
        self.schichtzeiten_tree = self.create_data_table(columns, widths)
    
    def populate_test_data(self):
        """Add some sample data for testing"""
        # TODO: Implement similar to AbschnitteSection with appropriate data
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
    
    def refresh_data(self):
        """Refresh data from Supabase"""
        if not self.app.is_supabase_connected:
            return
        
        try:
            # Clear current display
            for item in self.schichtzeiten_tree.get_children():
                self.schichtzeiten_tree.delete(item)
            
            # Get data from Supabase
            schichtzeiten = self.app.supabase_connector.get_schichtzeiten()
            
            # Populate tree
            for item in schichtzeiten:
                self.schichtzeiten_tree.insert("", tk.END, iid=item["id"], values=(
                    item["id"], 
                    item["schicht"], 
                    item["zeit_von"], 
                    item["zeit_bis"]
                ))
            
            # Update all_items for filtering
            self.schichtzeiten_tree.all_items = []
            for item_id in self.schichtzeiten_tree.get_children():
                self.schichtzeiten_tree.all_items.append(
                    (item_id, self.schichtzeiten_tree.item(item_id, "values"))
                )
        
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Schichtzeiten: {str(e)}")
    
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