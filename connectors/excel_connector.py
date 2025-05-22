import pandas as pd
import os

class ExcelConnector:
    """Connector for handling Excel file operations"""
    
    def __init__(self):
        """Initialize the Excel connector"""
        self.excel_path = None
        self.sheets = {}
        
    def set_excel_path(self, path):
        """Set the path to the Excel file
        
        Args:
            path (str): Path to Excel file
            
        Returns:
            bool: True if file exists, False otherwise
        """
        if os.path.exists(path):
            self.excel_path = path
            return True
        return False
    
    def load_all_sheets(self):
        """Load all sheets from the Excel file
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if not self.excel_path:
            return False
            
        try:
            # Load Excel file with pandas
            xls = pd.ExcelFile(self.excel_path)
            
            # Load all sheets into dictionary
            for sheet_name in xls.sheet_names:
                self.sheets[sheet_name] = pd.read_excel(xls, sheet_name)
                
            return True
        except Exception as e:
            print(f"Error loading Excel sheets: {str(e)}")
            return False
            
    def get_dropdown_data(self):
        """Extract dropdown data from Excel sheets
        
        Returns:
            dict: Dictionary with dropdown data for UI components
        """
        dropdown_data = {
            "abschnitt": [],
            "baufuhrer": [],
            "arbeitsleiter": [],
            "zeit": [],
            "personal": [],
            "logistik_personal": [],
            "ako_personal": [],
            "sc_personal": [],
            "siwa_personal": [],
            "inventar": [],
            "gbm_machines": [],
        }
        
        # This is a placeholder - in a real implementation, you would extract
        # the data from the appropriate sheets
        
        # Example (assuming sheets have certain structure):
        if "Abschnitte" in self.sheets:
            dropdown_data["abschnitt"] = self.sheets["Abschnitte"]["Abschnitt"].tolist()
            
        if "Personal" in self.sheets:
            personal_df = self.sheets["Personal"]
            
            # Extract personnel based on type/function
            dropdown_data["personal"] = personal_df["Name"].tolist()
            
            # Filter by function if that column exists
            if "Funktion" in personal_df.columns:
                dropdown_data["logistik_personal"] = personal_df[personal_df["Funktion"] == "Logistik"]["Name"].tolist()
                dropdown_data["ako_personal"] = personal_df[personal_df["Funktion"] == "AKO"]["Name"].tolist()
                dropdown_data["sc_personal"] = personal_df[personal_df["Funktion"] == "SC"]["Name"].tolist()
                dropdown_data["siwa_personal"] = personal_df[personal_df["Funktion"] == "SIWA"]["Name"].tolist()
        
        if "Bauführer" in self.sheets:
            dropdown_data["baufuhrer"] = self.sheets["Bauführer"]["Name"].tolist()
            
        if "Arbeitsleiter" in self.sheets:
            dropdown_data["arbeitsleiter"] = self.sheets["Arbeitsleiter"]["Name"].tolist()
            
        if "Schichtzeiten" in self.sheets:
            dropdown_data["zeit"] = self.sheets["Schichtzeiten"]["Schicht"].tolist()
            
        if "Inventar" in self.sheets:
            inventar_df = self.sheets["Inventar"]
            dropdown_data["inventar"] = inventar_df["Maschine"].tolist()
            
            # Filter by type if that column exists
            if "Type" in inventar_df.columns:
                dropdown_data["gbm_machines"] = inventar_df[inventar_df["Type"] == "GBM"]["Maschine"].tolist()
        
        # If no data was loaded from Excel, return some sample data
        if not any(dropdown_data.values()):
            dropdown_data = {
                "abschnitt": ["Abschnitt 1", "Abschnitt 2", "Abschnitt 3"],
                "baufuhrer": ["Bauführer 1", "Bauführer 2", "Bauführer 3"],
                "arbeitsleiter": ["Arbeitsleiter 1", "Arbeitsleiter 2", "Arbeitsleiter 3"],
                "zeit": ["Tag", "Nacht", "Spät"],
                "personal": ["Mitarbeiter 1", "Mitarbeiter 2", "Mitarbeiter 3"],
                "logistik_personal": ["Logistik 1", "Logistik 2"],
                "ako_personal": ["AKO 1", "AKO 2"],
                "sc_personal": ["SC 1", "SC 2"],
                "siwa_personal": ["SIWA 1", "SIWA 2"],
                "inventar": ["Maschine 1", "Maschine 2", "Maschine 3"],
                "gbm_machines": ["GBM 1", "GBM 2"],
            }
            
        return dropdown_data 