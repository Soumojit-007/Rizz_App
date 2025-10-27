import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('charmbot_history.db')

# Read all data
df = pd.read_sql_query("SELECT * FROM conversations ORDER BY timestamp DESC", conn)

# Display
print(f"\n📊 Total Conversations: {len(df)}\n")
print(df.to_string())

# Close connection
conn.close()