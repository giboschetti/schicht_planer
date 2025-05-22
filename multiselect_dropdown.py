import tkinter as tk
from tkinter import ttk

class MultiSelectDropdown:
    """A multiselect dropdown widget for tkinter"""
    
    def __init__(self, parent, width=37, values=None, placeholder="Select items..."):
        """Initialize the multiselect dropdown
        
        Args:
            parent: Parent widget
            width: Width of the entry widget
            values: List of values for the dropdown
            placeholder: Text to show when no items are selected
        """
        self.parent = parent
        self.values = values or []
        self.selected_values = []
        self.placeholder = placeholder
        
        # Create a frame to contain the widget
        self.frame = ttk.Frame(parent)
        
        # Create the entry widget to display selected items
        self.entry_var = tk.StringVar()
        self.entry_var.set(placeholder)
        
        self.entry = ttk.Entry(self.frame, textvariable=self.entry_var, width=width)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Make the entry read-only by binding to readonly events
        self.entry.bind("<Key>", lambda e: "break")
        
        # Create the dropdown button
        self.button = ttk.Button(self.frame, text="▼", width=3, 
                               command=self.show_dropdown)
        self.button.pack(side=tk.LEFT)
        
        # Create a top level for the dropdown
        self.top_level = None
        
        # Create a frame to display the selection below the dropdown
        self.selection_display = ttk.Label(parent, text="", wraplength=300, 
                                        justify=tk.LEFT, foreground="gray")
    
    def pack(self, **kwargs):
        """Pack the widget"""
        self.frame.pack(**kwargs)
        self.selection_display.pack(anchor=tk.W, pady=2)
    
    def grid(self, **kwargs):
        """Grid the widget"""
        self.frame.grid(**kwargs)
        # Calculate row for selection display (one below the current row)
        row = kwargs.get('row', 0) + 1
        # Copy all grid parameters except row
        display_kwargs = {k: v for k, v in kwargs.items() if k != 'row'}
        display_kwargs['row'] = row
        self.selection_display.grid(**display_kwargs)
    
    def show_dropdown(self):
        """Show the dropdown with checkboxes"""
        if self.top_level:
            self.top_level.destroy()
            self.top_level = None
            return
            
        # Get the position of the entry widget
        x = self.frame.winfo_rootx()
        y = self.frame.winfo_rooty() + self.frame.winfo_height()
        
        # Create a new top level window
        self.top_level = tk.Toplevel(self.parent)
        self.top_level.geometry(f"+{x}+{y}")
        self.top_level.overrideredirect(True)  # Remove window decorations
        self.top_level.grab_set()  # Make it modal
        
        # Create a frame with a scrollbar
        main_frame = ttk.Frame(self.top_level)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas and scrollbar
        canvas = tk.Canvas(main_frame, borderwidth=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create checkboxes for each value
        self.checkbox_vars = {}
        for i, value in enumerate(self.values):
            var = tk.BooleanVar(value=value in self.selected_values)
            self.checkbox_vars[value] = var
            
            checkbox = ttk.Checkbutton(scrollable_frame, text=value, variable=var,
                                     command=lambda: self.update_selected())
            checkbox.pack(anchor="w", padx=5, pady=2)
        
        # Add buttons for select all/none
        button_frame = ttk.Frame(self.top_level)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        select_all_btn = ttk.Button(button_frame, text="Alle auswählen", 
                                  command=self.select_all)
        select_all_btn.pack(side=tk.LEFT, padx=5)
        
        select_none_btn = ttk.Button(button_frame, text="Keine auswählen", 
                                   command=self.select_none)
        select_none_btn.pack(side=tk.LEFT, padx=5)
        
        done_btn = ttk.Button(button_frame, text="Fertig", 
                            command=self.close_dropdown)
        done_btn.pack(side=tk.RIGHT, padx=5)
        
        # Set focus to the top level so that we can catch focus events
        self.top_level.focus_set()
        self.top_level.bind("<FocusOut>", self.on_focus_out)
        
        # Set a minimum width based on the entry width
        self.top_level.update_idletasks()
        min_width = max(self.frame.winfo_width(), 250)
        current_width = self.top_level.winfo_width()
        if current_width < min_width:
            self.top_level.geometry(f"{min_width}x{self.top_level.winfo_height()}")
    
    def on_focus_out(self, event):
        """Handle focus lost on the dropdown"""
        # If focus is within the dropdown or its children, don't close
        if event.widget == self.top_level or event.widget.master == self.top_level:
            return
            
        # Close dropdown when focus is lost
        self.close_dropdown()
    
    def update_selected(self):
        """Update the selected values"""
        self.selected_values = [value for value, var in self.checkbox_vars.items() 
                              if var.get()]
        
        self.update_display()
    
    def update_display(self):
        """Update the display of selected items"""
        if not self.selected_values:
            self.entry_var.set(self.placeholder)
            self.selection_display.config(text="")
        else:
            if len(self.selected_values) == 1:
                self.entry_var.set(self.selected_values[0])
            else:
                self.entry_var.set(f"{len(self.selected_values)} Elemente ausgewählt")
            
            # Update the selection display below
            display_text = ", ".join(self.selected_values[:3])
            if len(self.selected_values) > 3:
                display_text += f" ... (+{len(self.selected_values) - 3} weitere)"
            
            self.selection_display.config(text=display_text)
    
    def select_all(self):
        """Select all items"""
        for var in self.checkbox_vars.values():
            var.set(True)
        self.update_selected()
    
    def select_none(self):
        """Deselect all items"""
        for var in self.checkbox_vars.values():
            var.set(False)
        self.update_selected()
    
    def close_dropdown(self):
        """Close the dropdown"""
        if self.top_level:
            self.top_level.destroy()
            self.top_level = None
    
    def set(self, values):
        """Set the selected values
        
        Args:
            values: List of values to select
        """
        self.selected_values = [v for v in values if v in self.values]
        self.update_display()
    
    def get(self):
        """Get the selected values
        
        Returns:
            List of selected values
        """
        return self.selected_values
    
    def set_values(self, values):
        """Update the dropdown values
        
        Args:
            values: List of new values for the dropdown
        """
        self.values = values
        
        # Remove any selected values that are no longer in the options
        self.selected_values = [v for v in self.selected_values if v in self.values]
        self.update_display() 