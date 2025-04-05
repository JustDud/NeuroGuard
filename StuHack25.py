import os
import sqlite3
os.system('cls')

connection = sqlite3.connect('User_Data.db')
cursor = connection.cursor()

def create_user_tables():

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    emotional_state TEXT,
    emotion_score REAL,
    cognitive_load TEXT,
    sleep_quality TEXT,
    sleep_duration_hours REAL,
    social_interaction INTEGER,
    physical_activity_minutes REAL,
    screen_time_minutes INTEGER,
    environment_score REAL,
    goal_progress_score REAL,
    mood_trigger_notes TEXT,
    suggestions_given TEXT,
    FOREIGN KEY (user_id) REFERENCES main(user)
)
''')
                  
def View_Table(table):
    cursor.execute(f"SELECT * FROM {table}")
    for row in cursor.fetchall():
        print(", ".join(str(value) if value is not None else "NULL" for value in row))

def Insert_Values(table, values):
    try:
        if table == 'main':
            if len(values) != 2:
                raise ValueError("Main table requires exactly 2 values (user, password)")
            cursor.execute('''
                INSERT INTO main (user, password)
                VALUES (?, ?)
            ''', values)
            
        elif table == 'data':
            if len(values) < 1:
                raise ValueError("Data table requires at least user_id")
            
            columns = ['user_id'] + [
                col for col, val in zip([
                    'emotional_state', 'emotion_score', 'cognitive_load',
                    'sleep_quality', 'sleep_duration_hours', 'social_interaction',
                    'physical_activity_minutes', 'screen_time_minutes',
                    'environment_score', 'goal_progress_score', 'mood_trigger_notes',
                    'suggestions_given'
                ], values[1:]) if val is not None
            ]
            
            placeholders = ', '.join(['?'] * len(columns))
            query = f'''
                INSERT INTO data ({', '.join(columns)})
                VALUES ({placeholders})
            '''
            
            params = [values[0]] + [val for val in values[1:] if val is not None]
            cursor.execute(query, params)
            
        else:
            raise ValueError("Invalid table name. Use 'main' or 'data'")
            
        connection.commit()
        print(f"Data inserted into {table} successfully")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        connection.rollback()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

View_Table("main")
View_Table("data")

connection.close()