import pandas as pd
import os

# Get the current directory and file path
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "Schichtplaner.xlsm")

print(f"Analyzing file: {file_path}")

try:
    # Load the Excel workbook
    excel_file = pd.ExcelFile(file_path)
    
    # List all sheet names
    print("\nSheets in workbook:", excel_file.sheet_names)
    
    # Process each sheet
    for sheet_name in excel_file.sheet_names:
        print(f"\n{'='*50}")
        print(f"Sheet: {sheet_name}")
        
        try:
            # Load sheet into DataFrame
            df = excel_file.parse(sheet_name)
            
            # Print column information
            print(f"\nColumns ({len(df.columns)}):")
            for col in df.columns:
                print(f"  - {col}")
            
            # Print row count and preview
            print(f"\nTotal rows: {len(df)}")
            if not df.empty:
                print("\nPreview (first 3 rows):")
                print(df.head(3).to_string())
            else:
                print("Sheet is empty")
                
        except Exception as e:
            print(f"Error processing sheet '{sheet_name}': {str(e)}")
    
except Exception as e:
    print(f"Error opening Excel file: {str(e)}")