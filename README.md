# Schichtplaner

A shift planning application built with Python and Tkinter, integrated with Supabase for data storage.

## Features

- Create and manage work shifts
- View existing shifts in a table format
- Manage project data including:
  - Sections (Abschnitte)
  - Shift times (Schichtzeiten)
  - Work managers (Arbeitsleiter)
  - Construction managers (Bauführer)
  - Staff (Mitarbeiter)
  - Inventory (Inventar)
- Excel file import support
- Supabase database integration

## Requirements

- Python 3.x
- tkinter
- tkcalendar
- python-dotenv
- supabase-py
- pandas (for Excel operations)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd schichtplaner
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Supabase credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

4. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py` - Application entry point
- `app.py` - Main application class
- `connectors/` - Database and Excel connectors
- `ui/` - User interface components
  - `new_shifts_tab.py` - New shifts creation interface
  - `view_shifts_tab.py` - Shifts viewing interface
  - `project_data_tab.py` - Project data management interface
  - `project_sections/` - Individual section components

## License

[Your chosen license] 