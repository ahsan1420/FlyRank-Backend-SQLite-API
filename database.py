import sqlite3

DATABASE_NAME = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_tasks = [
            ("Learn FastAPI", False),
            ("Build CRUD API", False),
            ("Push to GitHub", True)
        ]

        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            sample_tasks
        )

    conn.commit()
    conn.close()


# Get all tasks
def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# Get one task
def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


# Insert a new task
def create_task(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, False)
    )

    conn.commit()

    task_id = cursor.lastrowid

    conn.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }
