import tkinter as tk
from tkinter import ttk, messagebox

class BaseSection:
    """Base class for all project data sections"""
    
    def __init__(self, parent, app):
        """Initialize the base section
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        self.parent = parent
        self.app = app
        self.tree = None
        
    def create_data_table(self, columns, column_widths=None):
        """Create a standard data table with scrollbar
        
        Args:
            columns: List of column names
            column_widths: Optional list of column widths
        
        Returns:
            ttk.Treeview: The created treeview widget
        """
        # Create a frame for the table and buttons
        frame = ttk.Frame(self.parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Hinzufügen", 
                            command=lambda: self.show_add_dialog(columns))
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(btn_frame, text="Bearbeiten", 
                             command=self.enter_edit_mode)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Löschen", 
                               command=self.delete_selected_item)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Edit mode buttons (initially hidden)
        edit_controls_frame = ttk.Frame(frame)
        save_btn = ttk.Button(edit_controls_frame, text="Änderungen Speichern", 
                             command=self.save_table_edits)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(edit_controls_frame, text="Abbrechen", 
                               command=self.exit_edit_mode)
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
                               command=lambda: self.apply_filters(filter_entries))
        filter_btn.grid(row=0, column=len(columns)*2, padx=5, pady=2)
        
        # Add clear filters button
        clear_btn = ttk.Button(filter_frame, text="Filter löschen", 
                              command=lambda: self.clear_filters(filter_entries))
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
        tree.bind("<Double-1>", lambda event, t=tree: self.on_cell_double_click(event, t))
        
        # Store references to components
        tree.btn_frame = btn_frame
        tree.edit_controls_frame = edit_controls_frame
        tree.filter_frame = filter_frame
        tree.filter_entries = filter_entries
        tree.is_in_edit_mode = False
        tree.all_items = []  # Store all items to support filtering
        tree.current_cell_editor = None
        
        self.tree = tree
        return tree
    
    def enter_edit_mode(self):
        """Enter edit mode for the table"""
        if self.tree:
            # Show edit control buttons
            self.tree.edit_controls_frame.pack(fill=tk.X, pady=5, after=self.tree.btn_frame)
            self.tree.is_in_edit_mode = True
            
            # Disable regular buttons during edit mode
            for child in self.tree.btn_frame.winfo_children():
                child.configure(state="disabled")
                
            # Notify user they are in edit mode
            messagebox.showinfo("Edit Mode", 
                              "Sie befinden sich jetzt im Bearbeitungsmodus.\n"
                              "Doppelklicken Sie auf ein Feld, um es zu bearbeiten.")
    
    def exit_edit_mode(self):
        """Exit edit mode without saving changes"""
        if self.tree:
            # Cancel any ongoing edit
            if self.tree.current_cell_editor:
                self.cancel_cell_edit(self.tree)
                
            # Hide edit control buttons
            self.tree.edit_controls_frame.pack_forget()
            self.tree.is_in_edit_mode = False
            
            # Re-enable regular buttons
            for child in self.tree.btn_frame.winfo_children():
                child.configure(state="normal")
                
            # Refresh tree to original values
            self.refresh_table_data()
    
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
        entry.bind("<Return>", lambda e, t=tree: self.finish_cell_edit(t))
        entry.bind("<Escape>", lambda e, t=tree: self.cancel_cell_edit(t))
        entry.bind("<FocusOut>", lambda e, t=tree: self.finish_cell_edit(t))
    
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
    
    def save_table_edits(self):
        """Save all edits made in edit mode - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement save_table_edits")
    
    def show_add_dialog(self, columns):
        """Show dialog to add a new item - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement show_add_dialog")
    
    def delete_selected_item(self):
        """Delete the selected item - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement delete_selected_item")
    
    def apply_filters(self, filter_entries):
        """Apply filters to the table"""
        if self.tree:
            # Clear current display
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Get filter values
            filters = {}
            for column, entry in filter_entries.items():
                value = entry.get().strip().lower()
                if value:
                    filters[column] = value
            
            # If no filters, display all items
            if not filters:
                for item_id, values in self.tree.all_items:
                    self.tree.insert("", tk.END, values=values)
                return
                
            # Apply filters
            for item_id, values in self.tree.all_items:
                should_display = True
                
                for column, filter_value in filters.items():
                    # Get the column index
                    columns = self.tree["columns"]
                    if column in columns:
                        col_idx = columns.index(column)
                        cell_value = str(values[col_idx]).lower()
                        
                        # Check if filter value is in the cell value
                        if filter_value not in cell_value:
                            should_display = False
                            break
                
                if should_display:
                    self.tree.insert("", tk.END, values=values)
    
    def clear_filters(self, filter_entries):
        """Clear all filters"""
        # Clear all filter entries
        for entry in filter_entries.values():
            entry.delete(0, tk.END)
            
        # Display all items
        self.apply_filters(filter_entries)
    
    def refresh_table_data(self):
        """Refresh the table data to its original state"""
        if self.tree:
            # Clear current display
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Insert original items
            for _, values in self.tree.all_items:
                self.tree.insert("", tk.END, values=values)
    
    def refresh_data(self):
        """Refresh data from the data source - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement refresh_data")
    
    def update_dropdown_values(self, dropdown_data):
        """Update dropdown values when data is refreshed - to be implemented by subclasses that need it"""
        pass  # Default implementation does nothing 