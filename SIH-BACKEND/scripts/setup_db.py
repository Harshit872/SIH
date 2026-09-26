import sqlite3

def init_plans_db():
    conn = sqlite3.connect('SIH-BACKEND/users.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS approved_plans (
            plan_id TEXT PRIMARY KEY,
            user_email TEXT,
            voyage_details TEXT,
            chosen_scenario TEXT,
            total_cost_usd REAL,
            risk_tier TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_plans_db()
