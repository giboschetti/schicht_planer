import os
from supabase import create_client, Client

class SupabaseConnector:
    """Connector for handling Supabase database operations"""
    
    def __init__(self):
        """Initialize the Supabase connector"""
        # Get Supabase URL and key from environment variables
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        
        # Create Supabase client
        self.supabase: Client = create_client(url, key)
        
    # --- DROPDOWN DATA METHODS ---
    
    def get_dropdown_data(self):
        """Get all dropdown data from Supabase
        
        Returns:
            dict: Dictionary with all dropdown data
        """
        # Fetch data for all dropdowns
        dropdown_data = {
            "abschnitt": self._get_abschnitt_names(),
            "baufuhrer": self._get_baufuhrer_names(),
            "arbeitsleiter": self._get_arbeitsleiter_names(),
            "zeit": self._get_schichtzeiten(),
            "personal": self._get_personal_names(),
            "logistik_personal": self._get_personnel_by_function("Logistik"),
            "ako_personal": self._get_personnel_by_function("AKO"),
            "sc_personal": self._get_personnel_by_function("SC"),
            "siwa_personal": self._get_personnel_by_function("SIWA"),
            "inventar": self._get_maschinen_names(),
            "gbm_machines": self._get_maschinen_by_type("GBM"),
            "function_types": ["Bauarbeiter", "AKO", "SC", "SIWA", "Logistik"],
            "machine_types": ["GBM", "ZW-Fahrzeug", "Diverses"],
        }
        
        return dropdown_data
    
    def _get_abschnitt_names(self):
        """Get all abschnitt names from Supabase"""
        result = self.supabase.table("abschnitte").select("abschnitt").execute()
        return [item["abschnitt"] for item in result.data]
    
    def _get_baufuhrer_names(self):
        """Get all bauführer names from Supabase"""
        result = self.supabase.table("baufuhrer").select("name").execute()
        return [item["name"] for item in result.data]
    
    def _get_arbeitsleiter_names(self):
        """Get all arbeitsleiter names from Supabase"""
        result = self.supabase.table("arbeitsleiter").select("name").execute()
        return [item["name"] for item in result.data]
    
    def _get_schichtzeiten(self):
        """Get all schichtzeiten from Supabase"""
        result = self.supabase.table("schichtzeiten").select("schicht").execute()
        return [item["schicht"] for item in result.data]
    
    def _get_personal_names(self):
        """Get all personnel names from Supabase"""
        result = self.supabase.table("personal").select("name").execute()
        return [item["name"] for item in result.data]
    
    def _get_personnel_by_function(self, function):
        """Get personnel names filtered by function"""
        result = self.supabase.table("personal").select("name").eq("funktion", function).execute()
        return [item["name"] for item in result.data]
    
    def _get_maschinen_names(self):
        """Get all machine names from Supabase"""
        result = self.supabase.table("inventar").select("maschine").execute()
        return [item["maschine"] for item in result.data]
    
    def _get_maschinen_by_type(self, type_name):
        """Get machine names filtered by type"""
        result = self.supabase.table("inventar").select("maschine").eq("type", type_name).execute()
        return [item["maschine"] for item in result.data]
    
    # --- SHIFTS METHODS ---
    
    def get_schichtplanung(self):
        """Get all shift planning data from Supabase"""
        return self.supabase.table("schichtplanung").select("*").execute().data
    
    def add_schichtplanung(self, data):
        """Add new shift planning to Supabase
        
        Args:
            data (dict): Shift planning data
            
        Returns:
            list: The inserted data
        """
        result = self.supabase.table("schichtplanung").insert(data).execute()
        return result.data
    
    def update_schichtplanung(self, id, data):
        """Update shift planning in Supabase
        
        Args:
            id (str): ID of the shift to update
            data (dict): Updated shift planning data
            
        Returns:
            list: The updated data
        """
        return self.supabase.table("schichtplanung").update(data).eq("id", id).execute().data
    
    def delete_schichtplanung(self, id):
        """Delete shift planning from Supabase
        
        Args:
            id (str): ID of the shift to delete
        """
        return self.supabase.table("schichtplanung").delete().eq("id", id).execute()
    
    # --- ABSCHNITTE METHODS ---
    
    def get_abschnitte(self):
        """Get all abschnitte from Supabase"""
        return self.supabase.table("abschnitte").select("*").execute().data
    
    def add_abschnitt(self, abschnitt, beschreibung=""):
        """Add new abschnitt to Supabase"""
        data = {"abschnitt": abschnitt, "beschreibung": beschreibung}
        result = self.supabase.table("abschnitte").insert(data).execute()
        return result.data
    
    def update_abschnitt(self, id, abschnitt, beschreibung=""):
        """Update an abschnitt in Supabase"""
        data = {"abschnitt": abschnitt, "beschreibung": beschreibung}
        return self.supabase.table("abschnitte").update(data).eq("id", id).execute().data
    
    def delete_abschnitt(self, id):
        """Delete an abschnitt from Supabase"""
        return self.supabase.table("abschnitte").delete().eq("id", id).execute()
    
    # --- SCHICHTZEITEN METHODS ---
    
    def get_schichtzeiten(self):
        """Get all schichtzeiten from Supabase"""
        return self.supabase.table("schichtzeiten").select("*").execute().data
    
    def add_schichtzeit(self, schicht, zeit_von, zeit_bis):
        """Add new schichtzeit to Supabase"""
        data = {"schicht": schicht, "zeit_von": zeit_von, "zeit_bis": zeit_bis}
        result = self.supabase.table("schichtzeiten").insert(data).execute()
        return result.data
    
    def update_schichtzeit(self, id, schicht, zeit_von, zeit_bis):
        """Update a schichtzeit in Supabase"""
        data = {"schicht": schicht, "zeit_von": zeit_von, "zeit_bis": zeit_bis}
        return self.supabase.table("schichtzeiten").update(data).eq("id", id).execute().data
    
    def delete_schichtzeit(self, id):
        """Delete a schichtzeit from Supabase"""
        return self.supabase.table("schichtzeiten").delete().eq("id", id).execute()
    
    # --- ARBEITSLEITER METHODS ---
    
    def get_arbeitsleiter(self):
        """Get all arbeitsleiter from Supabase"""
        return self.supabase.table("arbeitsleiter").select("*").execute().data
    
    def add_arbeitsleiter(self, name, telefonnummer="", email=""):
        """Add new arbeitsleiter to Supabase"""
        data = {"name": name, "telefonnummer": telefonnummer, "email": email}
        result = self.supabase.table("arbeitsleiter").insert(data).execute()
        return result.data
    
    def update_arbeitsleiter(self, id, name, telefonnummer="", email=""):
        """Update an arbeitsleiter in Supabase"""
        data = {"name": name, "telefonnummer": telefonnummer, "email": email}
        return self.supabase.table("arbeitsleiter").update(data).eq("id", id).execute().data
    
    def delete_arbeitsleiter(self, id):
        """Delete an arbeitsleiter from Supabase"""
        return self.supabase.table("arbeitsleiter").delete().eq("id", id).execute()
    
    # --- BAUFÜHRER METHODS ---
    
    def get_baufuhrer(self):
        """Get all bauführer from Supabase"""
        return self.supabase.table("baufuhrer").select("*").execute().data
    
    def add_baufuhrer(self, name, telefonnummer="", email=""):
        """Add new bauführer to Supabase"""
        data = {"name": name, "telefonnummer": telefonnummer, "email": email}
        result = self.supabase.table("baufuhrer").insert(data).execute()
        return result.data
    
    def update_baufuhrer(self, id, name, telefonnummer="", email=""):
        """Update a bauführer in Supabase"""
        data = {"name": name, "telefonnummer": telefonnummer, "email": email}
        return self.supabase.table("baufuhrer").update(data).eq("id", id).execute().data
    
    def delete_baufuhrer(self, id):
        """Delete a bauführer from Supabase"""
        return self.supabase.table("baufuhrer").delete().eq("id", id).execute()
    
    # --- PERSONAL METHODS ---
    
    def get_personal(self):
        """Get all personnel from Supabase"""
        return self.supabase.table("personal").select("*").execute().data
    
    def add_personal(self, name, funktion="", telefonnummer="", email=""):
        """Add new personnel to Supabase"""
        data = {
            "name": name, 
            "funktion": funktion, 
            "telefonnummer": telefonnummer, 
            "email": email
        }
        result = self.supabase.table("personal").insert(data).execute()
        return result.data
    
    def update_personal(self, id, name, funktion="", telefonnummer="", email=""):
        """Update personnel in Supabase"""
        data = {
            "name": name, 
            "funktion": funktion, 
            "telefonnummer": telefonnummer, 
            "email": email
        }
        return self.supabase.table("personal").update(data).eq("id", id).execute().data
    
    def delete_personal(self, id):
        """Delete personnel from Supabase"""
        return self.supabase.table("personal").delete().eq("id", id).execute()
    
    # --- INVENTAR METHODS ---
    
    def get_inventar(self):
        """Get all inventar from Supabase"""
        return self.supabase.table("inventar").select("*").execute().data
    
    def add_inventar(self, maschine, firma="", type=""):
        """Add new inventar to Supabase"""
        data = {"maschine": maschine, "firma": firma, "type": type}
        result = self.supabase.table("inventar").insert(data).execute()
        return result.data
    
    def update_inventar(self, id, maschine, firma="", type=""):
        """Update inventar in Supabase"""
        data = {"maschine": maschine, "firma": firma, "type": type}
        return self.supabase.table("inventar").update(data).eq("id", id).execute().data
    
    def delete_inventar(self, id):
        """Delete inventar from Supabase"""
        return self.supabase.table("inventar").delete().eq("id", id).execute() 