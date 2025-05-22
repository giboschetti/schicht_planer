import pandas as pd
import os

class ExcelConnector:
    def __init__(self, excel_path=None):
        """
        Initialize Excel connector for Schichtplaner
        
        Args:
            excel_path (str): Path to the Excel file with the data
        """
        self.excel_path = excel_path
        self.data = {}
        
    def set_excel_path(self, path):
        """Set the path to the Excel file"""
        if os.path.exists(path):
            self.excel_path = path
            return True
        return False
    
    def load_all_sheets(self):
        """Load all relevant sheets from Excel"""
        if not self.excel_path or not os.path.exists(self.excel_path):
            raise FileNotFoundError(f"Excel file not found at {self.excel_path}")
        
        try:
            # Load each sheet as a pandas DataFrame
            self.data['arbeitsleiter'] = pd.read_excel(self.excel_path, sheet_name='arbeitsleiter')
            self.data['baufuhrer'] = pd.read_excel(self.excel_path, sheet_name='baufuhrer')
            self.data['abschnitte'] = pd.read_excel(self.excel_path, sheet_name='abschnitte')
            self.data['schichtzeiten'] = pd.read_excel(self.excel_path, sheet_name='schichtzeiten')
            self.data['personal'] = pd.read_excel(self.excel_path, sheet_name='personal')
            
            return True
        except Exception as e:
            print(f"Error loading Excel sheets: {str(e)}")
            return False
    
    def get_arbeitsleiter_list(self):
        """Get list of Arbeitsleiter for dropdown"""
        if 'arbeitsleiter' not in self.data:
            return []
        
        # Assuming there's a 'name' column in the arbeitsleiter sheet
        if 'name' in self.data['arbeitsleiter'].columns:
            return self.data['arbeitsleiter']['name'].tolist()
        return []
    
    def get_baufuhrer_list(self):
        """Get list of Bauführer for dropdown"""
        if 'baufuhrer' not in self.data:
            return []
        
        # Assuming there's a 'name' column in the baufuhrer sheet
        if 'name' in self.data['baufuhrer'].columns:
            return self.data['baufuhrer']['name'].tolist()
        return []
    
    def get_abschnitte_list(self):
        """Get list of Abschnitte for dropdown"""
        if 'abschnitte' not in self.data:
            return []
        
        # Assuming there's a 'name' or 'bezeichnung' column in the abschnitte sheet
        if 'name' in self.data['abschnitte'].columns:
            return self.data['abschnitte']['name'].tolist()
        elif 'bezeichnung' in self.data['abschnitte'].columns:
            return self.data['abschnitte']['bezeichnung'].tolist()
        return []
    
    def get_zeit_list(self):
        """Get list of time periods (zeit) for dropdown"""
        if 'schichtzeiten' not in self.data:
            return ["Tag", "Nacht", "Spät"]  # Default values
        
        # Assuming there's a 'schicht' column in the schichtzeiten sheet
        if 'schicht' in self.data['schichtzeiten'].columns:
            return self.data['schichtzeiten']['schicht'].unique().tolist()
        return ["Tag", "Nacht", "Spät"]  # Default values
    
    def get_personal_list(self):
        """Get list of staff for dropdown"""
        if 'personal' not in self.data:
            return []
        
        # Assuming there's a 'name' column in the personal sheet
        if 'name' in self.data['personal'].columns:
            return self.data['personal']['name'].tolist()
        return []
    
    def get_dropdown_data(self):
        """Get all dropdown data as a dictionary"""
        dropdown_data = {
            "abschnitt": self.get_abschnitte_list(),
            "baufuhrer": self.get_baufuhrer_list(),
            "arbeitsleiter": self.get_arbeitsleiter_list(),
            "zeit": self.get_zeit_list(),
            "personal": self.get_personal_list()
        }
        
        # Use default values if any list is empty
        if not dropdown_data["abschnitt"]:
            dropdown_data["abschnitt"] = ["Abschnitt 1", "Abschnitt 2", "Abschnitt 3"]
        
        if not dropdown_data["baufuhrer"]:
            dropdown_data["baufuhrer"] = ["Bauführer 1", "Bauführer 2", "Bauführer 3"]
            
        if not dropdown_data["arbeitsleiter"]:
            dropdown_data["arbeitsleiter"] = ["Arbeitsleiter 1", "Arbeitsleiter 2", "Arbeitsleiter 3"]
            
        if not dropdown_data["zeit"]:
            dropdown_data["zeit"] = ["Tag", "Nacht", "Spät"]
            
        if not dropdown_data["personal"]:
            dropdown_data["personal"] = ["Mitarbeiter 1", "Mitarbeiter 2", "Mitarbeiter 3"]
            
        return dropdown_data


# Example usage
if __name__ == "__main__":
    connector = ExcelConnector("path_to_excel.xlsx")
    try:
        connector.load_all_sheets()
        data = connector.get_dropdown_data()
        print("Loaded dropdown data:")
        for key, values in data.items():
            print(f"{key}: {values[:5]}...")  # Print first 5 items
    except Exception as e:
        print(f"Error: {str(e)}") 