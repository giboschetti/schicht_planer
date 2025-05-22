import os
import uuid
import json
import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

class SupabaseConnector:
    def __init__(self):
        """Initialize Supabase connector"""
        # Load environment variables
        load_dotenv()
        
        # Initialize Supabase client
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL and Key must be set in environment variables")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    def generate_uuid(self):
        """Generate a new UUID"""
        return str(uuid.uuid4())
    
    # Abschnitte methods
    def get_abschnitte(self):
        """Get all Abschnitte"""
        response = self.supabase.table("abschnitte").select("*").execute()
        return response.data
    
    def add_abschnitt(self, abschnitt, beschreibung):
        """Add a new Abschnitt"""
        data = {
            "id": self.generate_uuid(),
            "abschnitt": abschnitt,
            "beschreibung": beschreibung,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "uploaded": True
        }
        response = self.supabase.table("abschnitte").insert(data).execute()
        return response.data
    
    def update_abschnitt(self, id, abschnitt, beschreibung):
        """Update an existing Abschnitt"""
        data = {
            "abschnitt": abschnitt,
            "beschreibung": beschreibung,
            "updated_at": datetime.datetime.now().isoformat()
        }
        response = self.supabase.table("abschnitte").update(data).eq("id", id).execute()
        return response.data
    
    def delete_abschnitt(self, id):
        """Delete an Abschnitt"""
        response = self.supabase.table("abschnitte").delete().eq("id", id).execute()
        return response.data
    
    # Schichtzeiten methods
    def get_schichtzeiten(self):
        """Get all Schichtzeiten"""
        response = self.supabase.table("schichtzeiten").select("*").execute()
        return response.data
    
    def add_schichtzeit(self, schicht, zeit_von, zeit_bis):
        """Add a new Schichtzeit"""
        data = {
            "id": self.generate_uuid(),
            "schicht": schicht,
            "zeit_von": zeit_von,
            "zeit_bis": zeit_bis,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "uploaded": True
        }
        response = self.supabase.table("schichtzeiten").insert(data).execute()
        return response.data
    
    def update_schichtzeit(self, id, schicht, zeit_von, zeit_bis):
        """Update an existing Schichtzeit"""
        data = {
            "schicht": schicht,
            "zeit_von": zeit_von,
            "zeit_bis": zeit_bis,
            "updated_at": datetime.datetime.now().isoformat()
        }
        response = self.supabase.table("schichtzeiten").update(data).eq("id", id).execute()
        return response.data
    
    def delete_schichtzeit(self, id):
        """Delete a Schichtzeit"""
        response = self.supabase.table("schichtzeiten").delete().eq("id", id).execute()
        return response.data
    
    # Arbeitsleiter methods
    def get_arbeitsleiter(self):
        """Get all Arbeitsleiter"""
        response = self.supabase.table("arbeitsleiter").select("*").execute()
        return response.data
    
    def add_arbeitsleiter(self, name, telefonnummer, email):
        """Add a new Arbeitsleiter"""
        data = {
            "id": self.generate_uuid(),
            "name": name,
            "telefonnummer": telefonnummer,
            "email": email
        }
        response = self.supabase.table("arbeitsleiter").insert(data).execute()
        return response.data
    
    def update_arbeitsleiter(self, id, name, telefonnummer, email):
        """Update an existing Arbeitsleiter"""
        data = {
            "name": name,
            "telefonnummer": telefonnummer,
            "email": email
        }
        response = self.supabase.table("arbeitsleiter").update(data).eq("id", id).execute()
        return response.data
    
    def delete_arbeitsleiter(self, id):
        """Delete an Arbeitsleiter"""
        response = self.supabase.table("arbeitsleiter").delete().eq("id", id).execute()
        return response.data
    
    # Bauführer methods
    def get_baufuhrer(self):
        """Get all Bauführer"""
        response = self.supabase.table("baufuhrer").select("*").execute()
        return response.data
    
    def add_baufuhrer(self, name, telefonnummer, email):
        """Add a new Bauführer"""
        data = {
            "id": self.generate_uuid(),
            "name": name,
            "telefonnummer": telefonnummer,
            "email": email
        }
        response = self.supabase.table("baufuhrer").insert(data).execute()
        return response.data
    
    def update_baufuhrer(self, id, name, telefonnummer, email):
        """Update an existing Bauführer"""
        data = {
            "name": name,
            "telefonnummer": telefonnummer,
            "email": email
        }
        response = self.supabase.table("baufuhrer").update(data).eq("id", id).execute()
        return response.data
    
    def delete_baufuhrer(self, id):
        """Delete a Bauführer"""
        response = self.supabase.table("baufuhrer").delete().eq("id", id).execute()
        return response.data
    
    # Personal methods
    def get_personal(self):
        """Get all Personal"""
        response = self.supabase.table("personal").select("*").execute()
        return response.data
    
    def add_personal(self, name, funktion, telefonnummer, email):
        """Add a new Personal"""
        data = {
            "id": self.generate_uuid(),
            "name": name,
            "funktion": funktion,
            "telefonnummer": telefonnummer,
            "email": email
        }
        response = self.supabase.table("personal").insert(data).execute()
        return response.data
    
    def update_personal(self, id, name, funktion, telefonnummer, email):
        """Update an existing Personal"""
        data = {
            "name": name,
            "funktion": funktion,
            "telefonnummer": telefonnummer,
            "email": email
        }
        response = self.supabase.table("personal").update(data).eq("id", id).execute()
        return response.data
    
    def delete_personal(self, id):
        """Delete a Personal"""
        response = self.supabase.table("personal").delete().eq("id", id).execute()
        return response.data
    
    # Schichtplanung methods
    def get_schichtplanung(self):
        """Get all Schichtplanung entries"""
        response = self.supabase.table("schichtplanung").select("*").execute()
        return response.data
    
    def add_schichtplanung(self, data):
        """Add a new Schichtplanung entry"""
        # Ensure required fields
        if "titel" not in data or "datum_von" not in data:
            raise ValueError("Titel and Datum Von are required")
        
        # Add required fields
        data["id"] = self.generate_uuid()
        
        response = self.supabase.table("schichtplanung").insert(data).execute()
        return response.data
    
    def update_schichtplanung(self, id, data):
        """Update an existing Schichtplanung entry"""
        response = self.supabase.table("schichtplanung").update(data).eq("id", id).execute()
        return response.data
    
    def delete_schichtplanung(self, id):
        """Delete a Schichtplanung entry"""
        response = self.supabase.table("schichtplanung").delete().eq("id", id).execute()
        return response.data
    
    # Inventar methods
    def get_inventar(self):
        """Get all Inventar items"""
        try:
            response = self.supabase.table("inventar").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error getting inventar: {str(e)}")
            return []
    
    def get_inventar_by_type(self, type_name):
        """Get Inventar items filtered by type"""
        try:
            response = self.supabase.table("inventar").select("*").eq("type", type_name).execute()
            return response.data
        except Exception as e:
            print(f"Error getting inventar by type: {str(e)}")
            return []
    
    def add_inventar(self, maschine, firma, type_name):
        """Add a new Inventar item"""
        data = {
            "id": self.generate_uuid(),
            "maschine": maschine,
            "firma": firma,
            "type": type_name,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat()
        }
        response = self.supabase.table("inventar").insert(data).execute()
        return response.data
    
    def update_inventar(self, id, maschine, firma, type_name):
        """Update an existing Inventar item"""
        data = {
            "maschine": maschine,
            "firma": firma,
            "type": type_name,
            "updated_at": datetime.datetime.now().isoformat()
        }
        response = self.supabase.table("inventar").update(data).eq("id", id).execute()
        return response.data
    
    def delete_inventar(self, id):
        """Delete an Inventar item"""
        response = self.supabase.table("inventar").delete().eq("id", id).execute()
        return response.data
    
    # Specialized personnel getters
    def get_personal_by_function(self, function_name):
        """Get personal filtered by function"""
        try:
            response = self.supabase.table("personal").select("*").eq("funktion", function_name).execute()
            return response.data
        except Exception as e:
            print(f"Error getting personal by function: {str(e)}")
            return []
    
    def get_personal_by_functions(self, function_names):
        """Get personal filtered by multiple functions"""
        if not function_names:
            return []
        
        try:
            if len(function_names) == 1:
                return self.get_personal_by_function(function_names[0])
                
            # With multiple functions, we need to build a query with OR conditions
            query = self.supabase.table("personal").select("*")
            
            # Build a filter string with OR conditions
            filter_str = f"funktion.eq.{function_names[0]}"
            for func in function_names[1:]:
                filter_str += f",funktion.eq.{func}"
                
            response = query.or_(filter_str).execute()
            return response.data
        except Exception as e:
            print(f"Error getting personal by functions: {str(e)}")
            return []
    
    # General get dropdown data method
    def get_dropdown_data(self):
        """Get all dropdown data for the application"""
        
        # Get basic data
        abschnitte = self.get_abschnitte()
        baufuhrer = self.get_baufuhrer()
        arbeitsleiter = self.get_arbeitsleiter()
        schichtzeiten = self.get_schichtzeiten()
        personal = self.get_personal()
        
        # Get specialized data
        inventar = self.get_inventar()
        gbm_machines = self.get_inventar_by_type("GBM")
        zw_machines = self.get_inventar_by_type("ZW-Fahrzeug")
        diverse_machines = self.get_inventar_by_type("Diverses")
        
        # Get personnel by function types
        logistik_personal = self.get_personal_by_functions(["Lokfuhrer", "Begleiter"])
        ako_personal = self.get_personal_by_function("AKO")
        siwa_personal = self.get_personal_by_function("SIWA")
        sc_personal = self.get_personal_by_function("SC")
        
        # Function categories for the UI
        function_types = [
            "Bauarbeiter", "AKO", "SC", "SIWA", "Lokfuhrer", "Begleiter", 
            "GBM Maschinenfuhrer", "Maschinist ZW-Fahrzeug", "Maschinist", "Schweisser"
        ]
        
        machine_types = ["GBM", "ZW-Fahrzeug", "Diverses"]
        
        # Format for dropdown use
        dropdown_data = {
            "abschnitt": [item["abschnitt"] for item in abschnitte],
            "baufuhrer": [item["name"] for item in baufuhrer],
            "arbeitsleiter": [item["name"] for item in arbeitsleiter],
            "zeit": [item["schicht"] for item in schichtzeiten],
            "personal": [item["name"] for item in personal],
            "inventar": [item["maschine"] for item in inventar],
            "gbm_machines": [item["maschine"] for item in gbm_machines],
            "zw_machines": [item["maschine"] for item in zw_machines],
            "diverse_machines": [item["maschine"] for item in diverse_machines],
            "logistik_personal": [item["name"] for item in logistik_personal],
            "ako_personal": [item["name"] for item in ako_personal],
            "siwa_personal": [item["name"] for item in siwa_personal],
            "sc_personal": [item["name"] for item in sc_personal],
            "function_types": function_types,
            "machine_types": machine_types
        }
        
        return dropdown_data


# Example usage
if __name__ == "__main__":
    supabase = SupabaseConnector()
    if supabase.supabase:
        print("Connected to Supabase")
        
        # Get dropdown data
        dropdowns = supabase.get_dropdown_data()
        print("Dropdown data:")
        for key, values in dropdowns.items():
            print(f"{key}: {values[:5] if values else []}")
        
        # Example inserting a shift
        new_shift = {
            "titel": "Test Shift",
            "datum_von": datetime.datetime.now().isoformat(),
            "zeit": "Tag",
            "abschnitt": "Test Section"
        }
        result = supabase.add_schichtplanung(new_shift)
        if result:
            print(f"Inserted shift with ID: {result['id']}")
    else:
        print("Not connected to Supabase. Check credentials.") 