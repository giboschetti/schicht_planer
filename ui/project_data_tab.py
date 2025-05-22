import tkinter as tk
from tkinter import ttk

from ui.project_sections.abschnitte_section import AbschnitteSection
from ui.project_sections.schichtzeiten_section import SchichtzeitenSection
from ui.project_sections.arbeitsleiter_section import ArbeitsleiterSection
from ui.project_sections.baufuhrer_section import BaufuhrerSection
from ui.project_sections.mitarbeiter_section import MitarbeiterSection
from ui.project_sections.inventar_section import InventarSection

class ProjectDataTab:
    """UI component for the 'Project Data' tab with multiple sections"""
    
    def __init__(self, parent, app):
        """Initialize the Project Data tab
        
        Args:
            parent: Parent widget (tab frame)
            app: Main application instance
        """
        self.parent = parent
        self.app = app
        
        # Set up the UI
        self.setup_ui()
        
        # Sections
        self.sections = {}
        
        # Set up individual sections
        self.setup_sections()
    
    def setup_ui(self):
        """Set up the UI for the project data tab with 6 different sections"""
        # Create a notebook for the sections inside the project data tab
        self.project_notebook = ttk.Notebook(self.parent)
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
    
    def setup_sections(self):
        """Initialize all section objects"""
        self.sections["abschnitte"] = AbschnitteSection(self.abschnitte_frame, self.app)
        self.sections["schichtzeiten"] = SchichtzeitenSection(self.schichtzeiten_frame, self.app)
        self.sections["arbeitsleiter"] = ArbeitsleiterSection(self.arbeitsleiter_frame, self.app)
        self.sections["baufuhrer"] = BaufuhrerSection(self.baufuhrer_frame, self.app)
        self.sections["mitarbeiter"] = MitarbeiterSection(self.mitarbeiter_frame, self.app)
        self.sections["inventar"] = InventarSection(self.inventar_frame, self.app)
        
        # Load initial data for each section
        if self.app.is_supabase_connected:
            self.refresh_all_project_data()
    
    def refresh_all_project_data(self):
        """Refresh all data in the project data tab"""
        for section in self.sections.values():
            section.refresh_data()
    
    def update_dropdown_values(self, dropdown_data):
        """Update dropdown values when data is refreshed
        
        Args:
            dropdown_data (dict): Updated dropdown data
        """
        # Forward to all sections that need to update their dropdown values
        for section in self.sections.values():
            section.update_dropdown_values(dropdown_data) 