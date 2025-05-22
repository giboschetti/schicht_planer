import tkinter as tk
from tkinter import ttk

class MultiSelectDropdown:
    """A custom dropdown that allows selecting multiple values"""
    
    def __init__(self, parent, width=20, values=None, placeholder="Select...", callback=None):
        """Initialize the multiselect dropdown
        
        Args:
            parent: The parent widget
            width (int): Width of the dropdown
            values (list): List of values to show in the dropdown
            placeholder (str): Text to show when nothing is selected
            callback (function): Optional callback when selection changes
        """
        # Store parameters
        self.parent = parent
        self.values = values or []
        self.placeholder = placeholder
        self.callback = callback
        
        # Create a frame for our dropdown
        self.frame = ttk.Frame(parent)
        
        # Create the combobox
        self.combo = ttk.Combobox(self.frame, width=width, values=values)
        self.combo.set(placeholder)
        self.combo.grid(row=0, column=0, padx=0, pady=0, sticky=tk.W)
        
        # Bind selection event
        self.combo.bind("<<ComboboxSelected>>", self._on_select)
        
        # Create a label to display selected items
        self.display_label = ttk.Label(self.frame, text="", width=width)
        self.display_label.grid(row=1, column=0, padx=0, pady=0, sticky=tk.W)
        
        # Selected items storage
        self.selected_items = []
        
    def grid(self, **kwargs):
        """Grid layout manager for the frame"""
        self.frame.grid(**kwargs)
        
    def pack(self, **kwargs):
        """Pack layout manager for the frame"""
        self.frame.pack(**kwargs)
        
    def place(self, **kwargs):
        """Place layout manager for the frame"""
        self.frame.place(**kwargs)
        
    def _on_select(self, event=None):
        """Handle selection from the dropdown"""
        selected = self.combo.get()
        
        # Check if the item is already selected
        if selected in self.selected_items:
            # Remove it from the selection
            self.selected_items.remove(selected)
        else:
            # Add it to the selection if it's not the placeholder
            if selected != self.placeholder:
                self.selected_items.append(selected)
        
        # Update the display
        self._update_display()
        
        # Reset the combobox to placeholder
        self.combo.set(self.placeholder)
        
        # Call the callback if provided
        if self.callback:
            self.callback(self.selected_items)
            
    def _update_display(self):
        """Update the display label with selected items"""
        if not self.selected_items:
            self.display_label.config(text="")
            return
            
        # Use a shortened version if too many items are selected
        if len(self.selected_items) > 2:
            display_text = f"{len(self.selected_items)} ausgewählt"
        else:
            display_text = ", ".join(self.selected_items)
            
        # Truncate if too long
        max_length = self.combo.cget("width") * 2  # Rough estimate of visible chars
        if len(display_text) > max_length:
            display_text = display_text[:max_length-3] + "..."
            
        self.display_label.config(text=display_text)
        
    def get(self):
        """Get the currently selected items
        
        Returns:
            list: List of selected items
        """
        return self.selected_items[:]  # Return a copy
        
    def set(self, items):
        """Set the selected items
        
        Args:
            items (list): List of items to select
        """
        # Validate items are in values
        valid_items = [item for item in items if item in self.values]
        
        self.selected_items = valid_items
        self._update_display()
        
        # Call the callback if provided
        if self.callback:
            self.callback(self.selected_items)
    
    def set_values(self, values):
        """Set the available values in the dropdown
        
        Args:
            values (list): List of values to show in the dropdown
        """
        self.values = values or []
        self.combo.config(values=self.values)
        
        # Remove any selected items that are no longer in values
        self.selected_items = [item for item in self.selected_items if item in self.values]
        self._update_display()
    
    def select_none(self):
        """Clear all selections"""
        self.selected_items = []
        self._update_display()
        self.combo.set(self.placeholder)
        
        # Call the callback if provided
        if self.callback:
            self.callback(self.selected_items) 