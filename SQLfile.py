import sqlite3




def create_user_tables():
    with sqlite3.connect('User_Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            emotional_state INT,
            sleep_duration_hours INT,
            screen_time_minutes INT,
            physical_activity_minutes INT,
            hour INT,
            weekday INT,
            sunlight_hours INT,
            safety INT,
            daily_goal_progress INT,
            previous_suggestion TEXT
        )
        ''')
        conn.commit()

def View_Table(table):
    with sqlite3.connect('User_Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        for row in cursor.fetchall():
            print(", ".join(str(value) if value is not None else "NULL" for value in row))

def Insert_Values(table, values):
    try:
        with sqlite3.connect('User_Data.db') as conn:
            cursor = conn.cursor()
            if table == 'data':
                if len(values) < 1:
                    raise ValueError("Data table requires at least user")

                columns = ['user'] + [
                    col for col, val in zip([
                        'emotional_state', 'sleep_duration_hours', 'screen_time_minutes',
                        'physical_activity_minutes', 'hour', 'weekday',
                        'sunlight_hours', 'safety', 'daily_goal_progress',
                        'previous_suggestion'
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
                raise ValueError("Invalid table name. Use 'data'")

            conn.commit()
            print(f"Data inserted into {table} successfully")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def View_Table(table):
    with sqlite3.connect('User_Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        for row in cursor.fetchall():
            print(", ".join(str(value) if value is not None else "NULL" for value in row))


View_Table("data")