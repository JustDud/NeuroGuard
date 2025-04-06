import random
import os

def generate_sample_data(n):
    data = []
    for _ in range(n):
        entry = {
            "sunlight_hours": random.randint(1, 12),                          # реалистичное дневное освещение
            "safety": random.randint(20, 100),                                # большинство районов хотя бы средне безопасны
            "sleep_duration_hours": round(random.uniform(3.0, 9.5), 1),       # от недосыпа до полноценного сна
            "screen_time_minutes": random.randint(120, 900),                 # от умеренного до чрезмерного
            "physical_activity_minutes": random.randint(0, 120),             # от полного покоя до активного дня
            "daily_goal_progression": random.randint(10, 100),               # от срыва до отличной продуктивности
            "hour": random.randint(0, 23),                                   # текущий час
            "weekday": random.randint(0, 6),
            "mental_state": None
        }
        data.append(entry)
    return data



def inject_mental_state(data, mental_states):
    for entry, state in zip(data, mental_states):
        entry["mental_state"] = state


DATA_FILE = "generated_sample_data.json"

def generate_and_append_data(n):
    import json

    # Load existing data
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

    # Generate new data
    new_samples = generate_sample_data(n)
    for entry in new_samples:
        entry["mental_state"] = None

    data.extend(new_samples)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Added {n} new samples. Total now: {len(data)}")


def assign_mental_states(states, start_index=100):
    import json

    if not os.path.exists(DATA_FILE):
        print("Data file does not exist.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    for i, state in enumerate(states):
        idx = start_index + i
        if idx < len(data):
            data[idx]["mental_state"] = state
        else:
            print(f"⚠️ Index {idx} is out of range. Skipping.")

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Assigned {len(states)} mental states starting from index {start_index}.")


if __name__ == "__main__":
    import json

    # Load existing data
    existing_samples = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            existing_samples = json.load(f)

    # Generate new samples and append
    generate_and_append_data(1000)

    # Assign mental states
    # mental_states = [35, 82, 55, 42, 60, 48, 64, 52, 30, 28, 45, 25, 20, 68, 33, 22, 40, 27, 73, 26, 39, 70, 57, 42, 18, 44, 38, 60, 54, 65, 28, 36, 32, 67, 30, 59, 45, 20, 38, 48, 50, 52, 34, 28, 64, 22, 30, 70, 33, 65, 30, 58, 55, 45, 50, 25, 36, 41, 72, 33, 27, 70, 53, 42, 39, 30, 44, 50, 68, 63, 46, 40, 42, 20, 35, 60, 30, 26, 33, 45, 65, 38, 31, 28, 64, 40, 25, 20, 15, 37, 40, 33, 62, 27, 24, 30, 50, 42, 48, 65]

    # assign_mental_states(mental_states)