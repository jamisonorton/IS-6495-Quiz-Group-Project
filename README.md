# Quiz Database Python Project

This project is a command-line quiz application backed by a SQLite database.

## How to run the project

Follow these steps in order to run the project smoothly.

### 1. Create and activate a Python 3 virtual environment

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install the project dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the database and tables

Run the setup script:

```bash
python db_setup.py
```

This creates the database tables and also creates the default admin account.

### 4. Import quiz questions from the CSV file

Run:

```bash
python import_questions.py
```

This reads `questions.csv` and populates the `Questions` table.

### 5. Start the quiz application

Run:

```bash
python quiz_app.py
```

Use this script to test the program.

## Recommended run order

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python db_setup.py
python import_questions.py
python quiz_app.py
```

## Notes

- Run `db_setup.py` before `import_questions.py`.
- Run `import_questions.py` before `quiz_app.py`.
- The default admin username is `admin` and the default password is `admin123`.
