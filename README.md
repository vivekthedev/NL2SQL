# NL2SQL: An easy to use talk to your DB tool

A Streamlit-based web application that allows users to upload SQLite database files and execute SQL using natural language.

![SQLite Query Tool Screenshot](https://i.imgur.com/5tVVJRM.png)

## Features

- **File Upload**: Upload any SQLite database file (.db, .sqlite, .sqlite3)
- **Database Inspection**: View tables and schema details of the uploaded database
- **SQL Query Execution**: Execute custom SQL queries against the database
- **Results Display**: View query results in a scrollable table with support for wide tables
- **Export Functionality**: Download query results as CSV files

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/NL2SQL.git
cd NL2SQL
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Use the app:
   - Upload a SQLite database file using the sidebar uploader
   - Click "Inspect Database Structure" to view tables and schemas
   - Enter SQL queries in the text area
   - Click "Execute Query" to run the query and see results
   - Download results as CSV if needed

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **sqlite3**: SQLite database interface
- **pandantic_ai**: Agent to process natural language

## License

This project is licensed under the MIT License - see the LICENSE file for details.
