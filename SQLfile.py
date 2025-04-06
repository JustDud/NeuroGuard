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

def get_latest_user_data():
    with sqlite3.connect("User_Data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        # Map row to expected dictionary keys for get_mental_state
        return {
            "sleep_duration_hours": float(row[3]) if row[3] is not None else 0,
            "screen_time_minutes": int(row[4]) if row[4] is not None else 0,
            "physical_activity_minutes": int(row[5]) if row[5] is not None else 0,
            "hour": int(row[6]) if row[6] is not None else 0,
            "weekday": int(row[7]) if row[7] is not None else 0,
            "sunlight_hours": int(row[8]) if row[8] is not None else 0,
            "safety": int(row[9]) if row[9] is not None else 0,
            "daily_goal_progression": int(row[10]) if row[10] is not None else 0
        }


# create_user_tables()
# View_Table("data")